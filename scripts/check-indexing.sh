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
if [ -n "${MAX_URLS:-}" ] && [ "${#urls[@]}" -gt "$MAX_URLS" ]; then
  echo "Capping at first $MAX_URLS of ${#urls[@]} sitemap URLs (set MAX_URLS to change)."
  urls=("${urls[@]:0:$MAX_URLS}")
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
