# ZC Mail Sender

Send email as `ahall@zombiecomponents.com` through Microsoft Graph from an
authenticated API call, so Claude sessions (and anything else with an API key)
can do outbound mail without depending on the Anthropic-hosted Microsoft 365
connector's write scopes.

App-only (client-credentials) daemon flow: no interactive login, no refresh
tokens, survives restarts. Safety comes from an Exchange **application access
policy** that restricts the app to the one mailbox — do not skip that step.

## One-time Entra setup (portal, ~10 minutes)

1. **App registration** — entra.microsoft.com → App registrations → New
   registration. Name `ZC Mail Sender`, single tenant, no redirect URI.
2. **Permission** — API permissions → Add a permission → Microsoft Graph →
   **Application permissions** → `Mail.Send`. Remove the default delegated
   `User.Read` if you like. Click **Grant admin consent** for
   zombiecomponents.com.
3. **Secret** — Certificates & secrets → New client secret, 24 months. Copy
   the value immediately (shown once). Set a calendar reminder to rotate
   before expiry.
4. Record tenant ID, client ID, and the secret — they go into server
   environment variables only (see `.env.example`). Never into the repo,
   never into chat.

## Restrict the app to the one mailbox (required)

Application `Mail.Send` can send as **any** mailbox in the tenant by default.
Scope it before first use:

```powershell
Connect-ExchangeOnline

New-DistributionGroup -Name "ZC-MailSender-Scope" -Type Security -Members ahall@zombiecomponents.com

New-ApplicationAccessPolicy -AppId <CLIENT_ID> `
  -PolicyScopeGroupId ZC-MailSender-Scope@zombiecomponents.com `
  -AccessRight RestrictAccess `
  -Description "Limit ZC Mail Sender app to the ahall mailbox only"

# First should return Granted, second Denied
Test-ApplicationAccessPolicy -Identity ahall@zombiecomponents.com -AppId <CLIENT_ID>
Test-ApplicationAccessPolicy -Identity <any-other-mailbox> -AppId <CLIENT_ID>
```

Policy propagation can take 30–60 minutes; do this early.

## Run the server

```bash
cd mail-sender
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
cp .env.example .env   # fill in real values, keep out of git
set -a; source .env; set +a
.venv/bin/python app.py            # serves on 127.0.0.1:$ZC_MAIL_PORT (default 8321)
```

Put it behind whatever TLS-terminating reverse proxy the server already uses;
the app itself binds localhost only.

Run the tests (no network or secrets needed):

```bash
.venv/bin/pip install pytest
.venv/bin/python -m pytest tests/ -q
```

## API

**POST** `/api/v1/email/send` — header `X-API-Key: <keyid>:<secret>`

```json
{
  "to": ["sales@example.com"],
  "cc": [],
  "bcc": [],
  "subject": "string, 255 char max",
  "body": "string",
  "body_type": "text",
  "reply_to": null,
  "save_to_sent": true
}
```

- `body_type`: `"text"` or `"html"`.
- At least one recipient across `to`/`cc`/`bcc`; combined cap 20
  (`ZC_MAIL_RECIPIENT_CAP`).
- The FROM address is hardcoded server-side to `ZC_MAIL_FROM`
  (ahall@zombiecomponents.com). It is never a request parameter — requests
  containing any unknown field (including attachments, which are out of scope
  for v1) are rejected.

Success response:

```json
{ "status": "sent", "recipients": 1, "timestamp": "2026-08-11T00:00:00+00:00" }
```

Errors: `401` bad/missing key · `400`/`422` validation · `429` hourly cap
(default 50/h, `ZC_MAIL_HOURLY_CAP`) or Graph throttling · `502` with a
structured `{"error": code}` body for Graph-side failures (`token_error`,
`permission_error`, `graph_unavailable`).

Every send is logged (timestamp, caller key id, recipients, subject). Bodies
are logged only when `AUDIT_FULL=1`.

### curl example

```bash
curl -sS https://<host>/api/v1/email/send \
  -H "X-API-Key: claude-main:<secret>" \
  -H "Content-Type: application/json" \
  -d '{
    "to": ["ahall@zombiecomponents.com"],
    "subject": "ZC Mail Sender self-test",
    "body": "If you can read this in the inbox and see a copy in Sent Items, the pipeline works.",
    "body_type": "text"
  }'
```

### Function descriptor (for Claude sessions)

```
send_email(to: list[str], subject: str, body: str, body_type: str = "text",
           cc: list[str] = [], bcc: list[str] = [], save_to_sent: bool = true)
-> POST /api/v1/email/send with header X-API-Key
```

Guardrails a calling session should know: 50 sends/hour, 20 recipients/message,
no attachments, FROM is always ahall@zombiecomponents.com.

## Test plan (from the handoff)

1. Token acquisition works (first send exercises it).
2. Self-test send to ahall@zombiecomponents.com → inbox arrival + Sent Items copy.
3. `Test-ApplicationAccessPolicy`: Granted for ahall, Denied for any other identity.
4. Received headers: SPF and DKIM pass natively (Graph sends via Exchange Online).
5. Negative tests: no key → 401; 21+ recipients → 400; HTML body renders.
6. First production send: the pending steel-pipe RFQ — **confirm it wasn't
   already sent manually before firing; do not double-send.**
