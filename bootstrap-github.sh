#!/usr/bin/env bash
#
# bootstrap-github.sh — recreate the wpzombiecomp toolkit on GitHub from scratch.
#
# Run this on any machine with git installed (desktop, laptop, GitHub Codespace):
#
#   bash bootstrap-github.sh
#
# It will:
#   1. Create the repo on GitHub if it doesn't exist (needs the `gh` CLI,
#      otherwise it assumes the repo already exists and just pushes to it).
#   2. Write all project files locally (setup.sh, scripts/check-indexing.sh, README.md).
#   3. Commit and push them to the default branch `main`.
#
set -euo pipefail

GITHUB_USER="uswine"
REPO="wpzombiecomp"
BRANCH="main"
WORKDIR="${1:-$REPO}"

echo "=== Bootstrapping $GITHUB_USER/$REPO into ./$WORKDIR ==="

# 1. Create the repo on GitHub if the gh CLI is available -------------------
if command -v gh >/dev/null 2>&1; then
  if ! gh repo view "$GITHUB_USER/$REPO" >/dev/null 2>&1; then
    gh repo create "$GITHUB_USER/$REPO" --private
    echo "Created GitHub repo $GITHUB_USER/$REPO"
  else
    echo "GitHub repo $GITHUB_USER/$REPO already exists — will push into it."
  fi
else
  echo "gh CLI not found — assuming $GITHUB_USER/$REPO already exists on GitHub."
fi

# 2. Write the project files ------------------------------------------------
mkdir -p "$WORKDIR/scripts"
cd "$WORKDIR"

cat > setup.sh <<'EOF_SETUP'
#!/usr/bin/env bash
#
# setup.sh — bootstrap the Zombie Components SEO/indexing toolkit from scratch.
#
# Usage:  ./setup.sh
#
# What it does:
#   1. Verifies required tools are present (bash, curl, grep, sed).
#   2. Makes all scripts in scripts/ executable.
#   3. Runs a connectivity self-test against zombiecomponents.com.
#   4. Prints how to run the indexing check.
#
set -euo pipefail

SITE="zombiecomponents.com"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== Zombie Components toolkit setup ==="
echo

echo "[1/4] Checking required tools..."
missing=0
for tool in curl grep sed awk; do
  if command -v "$tool" >/dev/null 2>&1; then
    echo "  ok: $tool"
  else
    echo "  MISSING: $tool  (install it and re-run setup)"
    missing=1
  fi
done
[ "$missing" -eq 0 ] || exit 1

echo
echo "[2/4] Making scripts executable..."
chmod +x "$REPO_ROOT"/scripts/*.sh
ls -l "$REPO_ROOT"/scripts/

echo
echo "[3/4] Connectivity self-test..."
if curl -fsS -o /dev/null --max-time 15 "https://$SITE/"; then
  echo "  ok: https://$SITE/ is reachable from this machine"
else
  echo "  WARNING: cannot reach https://$SITE/ from this machine."
  echo "  (Some managed/cloud environments block outbound access to this domain."
  echo "   Run this toolkit from your desktop or phone browser environment instead.)"
fi

echo
echo "[4/4] Done. Next step:"
echo "  ./scripts/check-indexing.sh          # full sitemap + Google indexing report"
echo "  ./scripts/check-indexing.sh URL...   # check specific blog-post URLs only"
EOF_SETUP

cat > scripts/check-indexing.sh <<'EOF_CHECK'
#!/usr/bin/env bash
#
# check-indexing.sh — validate that zombiecomponents.com blog pages are
# crawlable and generate Google index-check links for each of them.
#
# Usage:
#   ./scripts/check-indexing.sh                 # discover URLs from the sitemap
#   ./scripts/check-indexing.sh URL [URL...]    # check only the given URLs
#
# For each page this reports:
#   - HTTP status (is the page live?)
#   - whether robots.txt or a <meta name="robots"> tag blocks indexing
#   - the exact Google "site:" query link to confirm index status manually
#
# Note: true index status lives in Google Search Console
# (https://search.google.com/search-console) — this script verifies the
# technical prerequisites and gives you one-click verification links.
#
set -uo pipefail

SITE="zombiecomponents.com"
UA="Mozilla/5.0 (compatible; ZombieComponentsIndexCheck/1.0)"

fetch() { curl -fsSL --max-time 20 -A "$UA" "$1"; }

echo "=== Google indexing pre-flight check for $SITE ==="
echo

if ! curl -fsS -o /dev/null --max-time 15 "https://$SITE/"; then
  echo "ERROR: https://$SITE/ is not reachable from this machine."
  echo "Run this script from a machine with normal internet access."
  exit 1
fi

# ---- collect URLs -----------------------------------------------------------
urls=()
if [ "$#" -gt 0 ]; then
  urls=("$@")
else
  echo "Discovering URLs from sitemaps..."
  for sm in "https://$SITE/wp-sitemap.xml" "https://$SITE/sitemap.xml" "https://$SITE/sitemap_index.xml"; do
    body="$(fetch "$sm" 2>/dev/null)" || continue
    echo "  found sitemap: $sm"
    # Expand one level of sitemap index, then collect page URLs.
    mapfile -t subs < <(printf '%s' "$body" | grep -o '<loc>[^<]*</loc>' | sed 's/<[^>]*>//g' | grep '\.xml$')
    if [ "${#subs[@]}" -gt 0 ]; then
      for sub in "${subs[@]}"; do
        mapfile -t -O "${#urls[@]}" urls < <(fetch "$sub" 2>/dev/null | grep -o '<loc>[^<]*</loc>' | sed 's/<[^>]*>//g' | grep -v '\.xml$')
      done
    else
      mapfile -t -O "${#urls[@]}" urls < <(printf '%s' "$body" | grep -o '<loc>[^<]*</loc>' | sed 's/<[^>]*>//g' | grep -v '\.xml$')
    fi
    break
  done
fi

if [ "${#urls[@]}" -eq 0 ]; then
  echo "No URLs found. Pass blog-post URLs as arguments instead."
  exit 1
fi
echo "Checking ${#urls[@]} URL(s)..."
echo

# ---- robots.txt -------------------------------------------------------------
robots="$(fetch "https://$SITE/robots.txt" 2>/dev/null || true)"
if printf '%s' "$robots" | grep -qi '^Disallow: /$'; then
  echo "WARNING: robots.txt disallows the whole site — Google cannot crawl it!"
fi

# ---- per-page checks --------------------------------------------------------
problems=0
for url in "${urls[@]}"; do
  status="$(curl -o /dev/null -s -w '%{http_code}' --max-time 20 -A "$UA" -L "$url")"
  html="$(fetch "$url" 2>/dev/null || true)"
  noindex=""
  printf '%s' "$html" | grep -qiE '<meta[^>]+robots[^>]+noindex' && noindex="  <-- NOINDEX TAG, Google will NOT index this page"
  flag="ok"
  if [ "$status" != "200" ] || [ -n "$noindex" ]; then flag="PROBLEM"; problems=$((problems+1)); fi
  echo "[$flag] $status  $url$noindex"
  echo "        verify in Google: https://www.google.com/search?q=site:${url}"
done

echo
echo "=== Summary ==="
echo "${#urls[@]} pages checked, $problems problem(s) found."
echo
echo "To force faster indexing of new blog posts:"
echo "  1. Open Google Search Console: https://search.google.com/search-console?resource_id=sc-domain:$SITE"
echo "  2. Use 'URL Inspection' on each new post and click 'Request Indexing'."
echo "  3. Confirm the sitemap is submitted under Indexing > Sitemaps."
EOF_CHECK

cat > README.md <<'EOF_README'
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
EOF_README

chmod +x setup.sh scripts/check-indexing.sh

# 3. Commit and push --------------------------------------------------------
if [ ! -d .git ]; then
  git init -b "$BRANCH"
fi
git add -A
if git diff --cached --quiet; then
  echo "Nothing new to commit."
else
  git commit -m "Add Google indexing check toolkit for zombiecomponents.com blog pages"
fi

if ! git remote get-url origin >/dev/null 2>&1; then
  git remote add origin "https://github.com/$GITHUB_USER/$REPO.git"
fi
git push -u origin "$BRANCH"

echo
echo "=== Done. Repo is live at: https://github.com/$GITHUB_USER/$REPO ==="
echo "Next: run ./setup.sh, then ./scripts/check-indexing.sh"
