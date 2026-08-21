# Connecting the Runway MCP Server

Runway (the AI video company, [runwayml.com](https://runwayml.com)) hosts an
official MCP server that lets Claude generate images and videos straight from
a conversation — you prompt in chat, generations spend your normal Runway
plan credits, and results are saved to your Runway library.

```
https://mcp.runwayml.com/mcp
```

There is no API key to manage: the server uses OAuth, so "connecting" is just
signing in with your Runway account when the client prompts you.

## What you get

Once connected, Claude can drive Runway's image and video generation using
whatever models your plan tier includes — as of August 2026 the lineup is
**Gen-4.5**, **Seedance 2.5**, **Kling 3.0**, **Veo 3.1**, **GPT Image 2**,
**Nano Banana Pro**, and Gen-4 Image/Turbo. You can name a model in your
prompt ("use Veo") or let the agent choose. Credit costs are the same as in
the Runway app and vary by model, resolution, and clip length.

## Connect it to claude.ai / the Claude apps

This is the route to use for **Claude Code cloud sessions** (the phone
workflow in [PHONE-SETUP.md](PHONE-SETUP.md)) — connectors added to your
claude.ai account are what those sessions can see:

1. Open [claude.ai](https://claude.ai) → **Settings → Connectors** (same
   path in the mobile app).
2. **Add custom connector** → name it `Runway`, paste
   `https://mcp.runwayml.com/mcp`, and click **Add**.
3. Click **Connect** and sign in to your Runway account in the window that
   opens.
4. Runway's tools now appear in the tools/connectors menu of new chats and
   Code sessions; enable them there if they aren't on by default.

## Pasted the URL into a chat and nothing happened?

That's expected — an MCP URL in a message is just text. Neither claude.ai
nor a Claude Code session connects to a server because its address appears
in the conversation; the connection is made in **Settings → Connectors**
(steps above), and a session only carries the tools of connectors that were
already connected — and enabled — when the session started.

If the tools aren't showing up, check in this order:

1. **Is it on the account?** Settings → Connectors should list Runway with
   a **Connected** state. "Added" but never signed in doesn't count — click
   **Connect** and finish the Runway OAuth sign-in.
2. **Is it enabled for the chat?** In the chat or Code session's
   tools/connectors menu, make sure Runway is toggled on.
3. **Did the session start after the connect?** Sessions pick up their tool
   list at launch — connect first, then start a fresh session; an
   already-running session won't gain the tools retroactively.
4. **Ask from inside the session.** A Claude Code cloud session can
   enumerate the account's connectors — just ask Claude to list your
   connectors and it will tell you whether Runway is attached and whether
   it's enabled for that session.

## Connect it to Claude Code (CLI on a computer)

```bash
claude mcp add --transport http runway https://mcp.runwayml.com/mcp
```

Add `--scope user` to make it available in every project instead of just the
current one. Then, inside a session, run `/mcp`, select **runway**, and
finish the OAuth sign-in in the browser tab it opens.

Note the browser requirement: the OAuth flow can't complete inside a
headless cloud container, so for cloud sessions use the claude.ai connector
route above rather than `claude mcp add` inside the session.

## Other clients

Cursor, ChatGPT (with connector/developer mode), Replit, and any other MCP
client that supports remote servers connect the same way: add
`https://mcp.runwayml.com/mcp` as a custom/remote MCP server and sign in
when prompted. The server speaks **Streamable HTTP only** — clients that
only do SSE or stdio can't use it.

## If you want key-based automation instead

For scripted/CI use where an interactive sign-in is awkward, Runway also
publishes a local MCP server,
[`runwayml/runway-api-mcp-server`](https://github.com/runwayml/runway-api-mcp-server)
(Node, stdio). It authenticates with a developer API key
(`RUNWAYML_API_SECRET` from [dev.runwayml.com](https://dev.runwayml.com))
and bills against **developer API credits, which are purchased separately
from app-plan credits**. Its tools:

| Tool | Does |
|---|---|
| `runway_listModels` | List available models + recommended defaults |
| `runway_generateImage` | Text → image (optional reference images) |
| `runway_generateVideo` | Image + text → video |
| `runway_editVideo` | Modify an existing video |
| `runway_upscaleVideo` | Increase video resolution |
| `runway_generateAudio` | Text → speech |
| `runway_getTask` / `runway_cancelTask` | Poll or cancel a generation task |

For interactive use in Claude, the hosted server above is the simpler and
cheaper path (no separate API billing).

## Under the hood (verified against the live endpoint)

Checked 2026-08-20, re-verified 2026-08-21, by probing
`https://mcp.runwayml.com/mcp` directly:

- Transport: Streamable HTTP; unauthenticated JSON-RPC POSTs get
  `401 {"error":"missing_bearer"}` with a `WWW-Authenticate` header pointing
  at the OAuth metadata. Everything — even `initialize`/`tools/list` — sits
  behind auth, so the tool list can't be enumerated without signing in.
- Auth: OAuth 2.1 authorization-code flow with PKCE (S256) and **dynamic
  client registration** (`/register`), so any MCP client can onboard itself
  without pre-registered credentials. Public client (no secret), refresh
  tokens supported. Scopes: `openid`, `api:read_write`.
- Discovery documents:
  `/.well-known/oauth-protected-resource/mcp` and
  `/.well-known/oauth-authorization-server` on `mcp.runwayml.com`.

## Gotchas

- **Two products are named "Runway MCP".** [runway.team](https://runway.team)
  (mobile release management) also ships an MCP server with confusingly
  similar docs. Everything here is about Runway**ML**, the generative media
  company.
- Model availability depends on your Runway plan tier — a model missing from
  the picker usually means a plan limitation, not a connection problem.
- Generations spend real credits; long/high-res video on frontier models is
  the expensive end, so ask for drafts at lower settings first.

## Sources

- [runway.com/mcp](https://runway.com/mcp) — official product page
- [Introducing Runway MCP](https://runwayml.com/news/mcp) — launch announcement
- [Connecting to Runway MCP](https://help.runwayml.com/hc/en-us/articles/51931843164691-Connecting-to-Runway-MCP) — help-center setup article
- [runwayml/runway-api-mcp-server](https://github.com/runwayml/runway-api-mcp-server) — key-based local server
