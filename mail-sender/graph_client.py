"""Microsoft Graph client for app-only (client credentials) mail sending.

Token handling per the build spec: acquire via the v2.0 client-credentials
grant, cache in memory, refresh when within 5 minutes of expiry. Never
request a new token per send.

Error mapping (spec 3.6):
  - Graph 401  -> drop cached token, retry once, then GraphError("token_error")
  - Graph 403  -> GraphError("permission_error") with propagation hint
  - Graph 429  -> honor Retry-After once, then GraphError("rate_limited")
  - Graph 5xx  -> one retry with short backoff, then GraphError("graph_unavailable")
"""

from __future__ import annotations

import threading
import time

import httpx

TOKEN_URL = "https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token"
SENDMAIL_URL = "https://graph.microsoft.com/v1.0/users/{upn}/sendMail"
SCOPE = "https://graph.microsoft.com/.default"

# Refresh when the cached token is within this many seconds of expiry.
EXPIRY_MARGIN = 5 * 60


class GraphError(Exception):
    def __init__(self, code: str, detail: str = ""):
        self.code = code
        self.detail = detail
        super().__init__(f"{code}: {detail}")


class GraphMailClient:
    def __init__(self, tenant_id: str, client_id: str, client_secret: str,
                 from_upn: str, timeout: float = 30.0):
        self._tenant_id = tenant_id
        self._client_id = client_id
        self._client_secret = client_secret
        self._from_upn = from_upn
        self._timeout = timeout
        self._token: str | None = None
        self._token_expires_at: float = 0.0
        self._lock = threading.Lock()

    # -- token ---------------------------------------------------------------

    def _get_token(self, force: bool = False) -> str:
        with self._lock:
            if (not force and self._token
                    and time.monotonic() < self._token_expires_at - EXPIRY_MARGIN):
                return self._token
            resp = httpx.post(
                TOKEN_URL.format(tenant=self._tenant_id),
                data={
                    "grant_type": "client_credentials",
                    "client_id": self._client_id,
                    "client_secret": self._client_secret,
                    "scope": SCOPE,
                },
                timeout=self._timeout,
            )
            if resp.status_code != 200:
                raise GraphError("token_error",
                                 f"token endpoint returned {resp.status_code}")
            payload = resp.json()
            self._token = payload["access_token"]
            self._token_expires_at = time.monotonic() + int(payload.get("expires_in", 3600))
            return self._token

    # -- send ----------------------------------------------------------------

    @staticmethod
    def _recipients(addresses: list[str]) -> list[dict]:
        return [{"emailAddress": {"address": a}} for a in addresses]

    def send_mail(self, *, to: list[str], cc: list[str], bcc: list[str],
                  subject: str, body: str, body_type: str,
                  reply_to: str | None, save_to_sent: bool) -> None:
        message: dict = {
            "subject": subject,
            "body": {
                "contentType": "HTML" if body_type == "html" else "Text",
                "content": body,
            },
            "toRecipients": self._recipients(to),
            "ccRecipients": self._recipients(cc),
            "bccRecipients": self._recipients(bcc),
        }
        if reply_to:
            message["replyTo"] = self._recipients([reply_to])
        payload = {"message": message, "saveToSentItems": save_to_sent}

        self._post_with_retries(payload)

    def _post_with_retries(self, payload: dict) -> None:
        url = SENDMAIL_URL.format(upn=self._from_upn)
        token = self._get_token()
        retried_auth = False
        retried_throttle = False
        retried_5xx = False

        while True:
            resp = httpx.post(
                url,
                json=payload,
                headers={"Authorization": f"Bearer {token}"},
                timeout=self._timeout,
            )
            if resp.status_code == 202:
                return
            if resp.status_code == 401:
                if retried_auth:
                    raise GraphError("token_error", "Graph rejected token twice")
                retried_auth = True
                token = self._get_token(force=True)
                continue
            if resp.status_code == 403:
                raise GraphError(
                    "permission_error",
                    "Graph returned 403 ErrorAccessDenied. Check admin consent "
                    "and application access policy propagation.")
            if resp.status_code == 429:
                if retried_throttle:
                    raise GraphError("rate_limited", "Graph throttled twice")
                retried_throttle = True
                time.sleep(min(float(resp.headers.get("Retry-After", 5)), 60))
                continue
            if resp.status_code >= 500:
                if retried_5xx:
                    raise GraphError("graph_unavailable",
                                     f"Graph returned {resp.status_code} twice")
                retried_5xx = True
                time.sleep(2)
                continue
            raise GraphError("graph_error",
                             f"unexpected Graph status {resp.status_code}: {resp.text[:300]}")
