"""ZC Mail Sender — authenticated send-email endpoint backed by Microsoft Graph.

POST /api/v1/email/send

The FROM address is fixed server-side to ZC_MAIL_FROM. It is never a request
parameter — hard rule per the build spec.

Config (environment variables only; see .env.example):
  ZC_MAIL_TENANT_ID      Entra tenant ID
  ZC_MAIL_CLIENT_ID      app registration client ID
  ZC_MAIL_CLIENT_SECRET  client secret (never in the repo)
  ZC_MAIL_FROM           sending mailbox UPN
  ZC_MAIL_API_KEYS       caller keys, "keyid1:secret1,keyid2:secret2"
  ZC_MAIL_HOURLY_CAP     max sends per rolling hour (default 50)
  ZC_MAIL_RECIPIENT_CAP  max combined to+cc+bcc per request (default 20)
  ZC_MAIL_STATE_FILE     file-backed hourly counter (default ./mail-sender-state.json)
  AUDIT_FULL             "1" to also log message bodies (default off)
"""

from __future__ import annotations

import hmac
import json
import logging
import os
import re
import threading
import time
from datetime import datetime, timezone

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel, Field, field_validator

from graph_client import GraphError, GraphMailClient

log = logging.getLogger("zc_mail_sender")
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(name)s %(message)s")

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _env(name: str, default: str | None = None) -> str:
    val = os.environ.get(name, default)
    if val is None:
        raise RuntimeError(f"missing required environment variable {name}")
    return val


def load_api_keys() -> dict[str, str]:
    """Parse ZC_MAIL_API_KEYS ("keyid:secret,keyid2:secret2") -> {keyid: secret}."""
    keys: dict[str, str] = {}
    for pair in _env("ZC_MAIL_API_KEYS").split(","):
        pair = pair.strip()
        if not pair:
            continue
        key_id, _, secret = pair.partition(":")
        if not key_id or not secret:
            raise RuntimeError("ZC_MAIL_API_KEYS entries must be keyid:secret")
        keys[key_id] = secret
    if not keys:
        raise RuntimeError("ZC_MAIL_API_KEYS defined no keys")
    return keys


class HourlyCounter:
    """Rolling-hour send counter, file-backed so it survives restarts."""

    def __init__(self, path: str, cap: int):
        self._path = path
        self._cap = cap
        self._lock = threading.Lock()

    def _load(self) -> list[float]:
        try:
            with open(self._path) as f:
                stamps = json.load(f)
        except (OSError, ValueError):
            stamps = []
        cutoff = time.time() - 3600
        return [s for s in stamps if isinstance(s, (int, float)) and s > cutoff]

    def try_acquire(self) -> bool:
        with self._lock:
            stamps = self._load()
            if len(stamps) >= self._cap:
                return False
            stamps.append(time.time())
            tmp = self._path + ".tmp"
            with open(tmp, "w") as f:
                json.dump(stamps, f)
            os.replace(tmp, self._path)
            return True


class SendRequest(BaseModel, extra="forbid"):
    # extra="forbid" rejects unsupported fields — notably attachments (v1 has none).
    to: list[str] = Field(default_factory=list)
    cc: list[str] = Field(default_factory=list)
    bcc: list[str] = Field(default_factory=list)
    subject: str = Field(min_length=1, max_length=255)
    body: str = Field(min_length=1)
    body_type: str = "text"
    reply_to: str | None = None
    save_to_sent: bool = True

    @field_validator("body_type")
    @classmethod
    def _body_type(cls, v: str) -> str:
        if v not in ("text", "html"):
            raise ValueError("body_type must be 'text' or 'html'")
        return v

    @field_validator("to", "cc", "bcc")
    @classmethod
    def _addresses(cls, v: list[str]) -> list[str]:
        for addr in v:
            if not EMAIL_RE.match(addr):
                raise ValueError(f"invalid email address: {addr}")
        return v

    @field_validator("reply_to")
    @classmethod
    def _reply_to(cls, v: str | None) -> str | None:
        if v is not None and not EMAIL_RE.match(v):
            raise ValueError(f"invalid email address: {v}")
        return v


def create_app() -> FastAPI:
    api_keys = load_api_keys()
    recipient_cap = int(os.environ.get("ZC_MAIL_RECIPIENT_CAP", "20"))
    hourly_cap = int(os.environ.get("ZC_MAIL_HOURLY_CAP", "50"))
    audit_full = os.environ.get("AUDIT_FULL") == "1"
    counter = HourlyCounter(
        os.environ.get("ZC_MAIL_STATE_FILE", "./mail-sender-state.json"), hourly_cap)
    graph = GraphMailClient(
        tenant_id=_env("ZC_MAIL_TENANT_ID"),
        client_id=_env("ZC_MAIL_CLIENT_ID"),
        client_secret=_env("ZC_MAIL_CLIENT_SECRET"),
        from_upn=_env("ZC_MAIL_FROM"),
    )

    app = FastAPI(title="ZC Mail Sender", version="1.0")
    app.state.graph = graph

    def require_api_key(x_api_key: str = Header(default="")) -> str:
        # Key format on the wire: "keyid:secret" in the X-API-Key header.
        key_id, _, secret = x_api_key.partition(":")
        expected = api_keys.get(key_id)
        if not expected or not hmac.compare_digest(secret, expected):
            raise HTTPException(status_code=401, detail="invalid or missing API key")
        return key_id

    @app.get("/api/v1/email/health")
    def health() -> dict:
        return {"status": "ok"}

    @app.post("/api/v1/email/send")
    def send(req: SendRequest, key_id: str = Depends(require_api_key)) -> dict:
        recipients = req.to + req.cc + req.bcc
        if not recipients:
            raise HTTPException(status_code=400,
                                detail="at least one recipient required across to/cc/bcc")
        if len(recipients) > recipient_cap:
            raise HTTPException(
                status_code=400,
                detail=f"recipient count {len(recipients)} exceeds cap {recipient_cap}")
        if not counter.try_acquire():
            raise HTTPException(
                status_code=429,
                detail=f"hourly send cap of {hourly_cap} reached; retry later")

        try:
            app.state.graph.send_mail(
                to=req.to, cc=req.cc, bcc=req.bcc,
                subject=req.subject, body=req.body, body_type=req.body_type,
                reply_to=req.reply_to, save_to_sent=req.save_to_sent)
        except GraphError as e:
            log.error("send failed key=%s error=%s detail=%s", key_id, e.code, e.detail)
            status = 429 if e.code == "rate_limited" else 502
            raise HTTPException(status_code=status,
                                detail={"error": e.code, "message": e.detail})

        log.info("sent key=%s recipients=%s subject=%r", key_id, recipients, req.subject)
        if audit_full:
            log.info("body key=%s %r", key_id, req.body)
        return {
            "status": "sent",
            "recipients": len(recipients),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    return app


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(create_app(), host="127.0.0.1",
                port=int(os.environ.get("ZC_MAIL_PORT", "8321")))
