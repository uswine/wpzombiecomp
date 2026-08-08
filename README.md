# wpzombiecomp — Zombie Components SEO / Google-indexing toolkit

Tooling for [zombiecomponents.com](https://zombiecomponents.com/) ("We Bring
Dead Things to Life – Through Recycling") to verify that blog pages — the
posts under **News, Updates and Announcements** (`/nua/`) — are indexed by
Google and technically crawlable.

## Quick start

```bash
./setup.sh                        # one-time bootstrap + connectivity check
./scripts/check-indexing.sh       # full sitemap crawl + indexing report
./scripts/check-indexing.sh https://zombiecomponents.com/some-new-post/
```

`check-indexing.sh` verifies each page is live (HTTP 200), not blocked by
`robots.txt` or a `noindex` meta tag, and prints a one-click
`site:` Google query link per page to confirm index status. Real index
status and "Request Indexing" live in
[Google Search Console](https://search.google.com/search-console).

## Indexing status snapshot (2026-08-08)

Checked via live Google search:

| Page | Indexed? |
|---|---|
| Homepage `zombiecomponents.com` | Yes |
| News/Updates/Announcements `/nua/` | Yes |
| Contact `/contact/` | Yes |
| Store & product pages (many) | Yes |
| Archive pages `/page/N/` | Yes (many) |
| **Newly added individual blog posts** | **Not yet appearing** |

New posts typically take days to weeks to appear unless you request
indexing manually. Fastest fix: Search Console → URL Inspection → paste
each new post URL → **Request Indexing**, and confirm the sitemap is
submitted under Indexing → Sitemaps.
