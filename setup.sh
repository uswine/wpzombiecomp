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
