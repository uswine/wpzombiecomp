#!/usr/bin/env python3
"""
pplx_qualify.py — independent qualification of the paper's load-bearing claims
via the Perplexity Sonar API.

Runs OUTSIDE the Claude Code sandbox (which cannot reach api.perplexity.ai),
on any machine where the Perplexity API is reachable. It reads claims.json,
asks Perplexity to independently verify each claim (with web citations), and
writes a markdown report plus a machine-readable JSON verdict file.

Return channel to Claude: commit the two output files to the repo and push,
or drop them in the shared Google Drive folder. Claude reads them there.

Usage:
    export PERPLEXITY_API_KEY=pplx-...            # do NOT hardcode the key
    python3 pplx_qualify.py                        # uses ./claims.json
    python3 pplx_qualify.py --model sonar-reasoning-pro --claims claims.json

The key is read only from the environment and is never written to disk or to
the output files.
"""
import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.error

API_URL = "https://api.perplexity.ai/chat/completions"

SYSTEM_PROMPT = (
    "You are an independent scientific fact-checker with web access. You are given a "
    "claim from a physics paper and a question. Verify the claim against primary "
    "sources (peer-reviewed papers, arXiv, NASA/ADS). Be adversarial: try to find "
    "where the numbers or attribution are wrong. Then return a verdict.\n\n"
    "Respond in EXACTLY this format:\n"
    "VERDICT: one of CONFIRMED | PARTIALLY-CONFIRMED | DISPUTED | UNVERIFIABLE\n"
    "CONFIDENCE: one of high | medium | low\n"
    "FINDING: 2-4 sentences with the specific numbers/facts you verified or that "
    "differ from the claim. Name the exact source (authors, year, journal/arXiv id).\n"
    "DISCREPANCIES: any way the claim overstates, misattributes, or rounds wrongly; "
    "'none' if the claim is accurate."
)


def ask(model, question, claim, api_key, timeout=120):
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"CLAIM:\n{claim}\n\nQUESTION:\n{question}"},
        ],
        "temperature": 0.0,
    }
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(body).encode(),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode())
    text = data["choices"][0]["message"]["content"]
    citations = data.get("citations") or data.get("search_results") or []
    return text, citations


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--claims", default=os.path.join(os.path.dirname(__file__), "claims.json"))
    ap.add_argument("--model", default="sonar-pro",
                    help="sonar | sonar-pro | sonar-reasoning | sonar-reasoning-pro | sonar-deep-research")
    ap.add_argument("--out-md", default=os.path.join(os.path.dirname(__file__), "..", "qualification", "pplx_results.md"))
    ap.add_argument("--out-json", default=os.path.join(os.path.dirname(__file__), "..", "qualification", "pplx_results.json"))
    args = ap.parse_args()

    api_key = os.environ.get("PERPLEXITY_API_KEY")
    if not api_key:
        sys.exit("ERROR: set PERPLEXITY_API_KEY in the environment first.")

    with open(args.claims) as f:
        claims = json.load(f)["claims"]

    results = []
    md = ["# Independent qualification via Perplexity Sonar\n",
          f"Model: `{args.model}`. Each claim from the paper was verified independently ",
          "against web/primary sources. This file is the return channel to Claude — ",
          "commit it (and the .json) to the repo or share via Drive.\n\n---\n"]

    for i, c in enumerate(claims, 1):
        print(f"[{i}/{len(claims)}] {c['id']} ...", flush=True)
        try:
            text, cites = ask(args.model, c["question"], c["claim"], api_key)
        except urllib.error.HTTPError as e:
            text, cites = f"HTTP {e.code}: {e.read().decode()[:300]}", []
        except Exception as e:
            text, cites = f"ERROR: {e}", []
        results.append({"id": c["id"], "section": c["section"], "response": text, "citations": cites})
        md.append(f"## {c['id']}  ({c['section']})\n")
        md.append(f"**Paper's claim:** {c['claim']}\n")
        md.append(f"**Perplexity verdict:**\n\n{text}\n")
        if cites:
            md.append("\n**Sources:**\n")
            for s in cites:
                url = s if isinstance(s, str) else s.get("url", str(s))
                md.append(f"- {url}")
        md.append("\n---\n")
        time.sleep(1)  # be polite to the API

    os.makedirs(os.path.dirname(os.path.abspath(args.out_md)), exist_ok=True)
    with open(args.out_md, "w") as f:
        f.write("\n".join(md))
    with open(args.out_json, "w") as f:
        json.dump({"model": args.model, "results": results}, f, indent=2)
    print(f"\nWrote {args.out_md} and {args.out_json}")
    print("Now: git add paper/qualification && git commit && git push  (or upload to Drive).")


if __name__ == "__main__":
    main()
