# Perplexity qualification relay

`pplx_qualify.py` independently re-checks the paper's load-bearing claims through
the Perplexity Sonar API, with web citations. It exists because the Claude Code
sandbox cannot reach `api.perplexity.ai` (network egress allowlist), but **any
machine you control can** — so you run this, it writes the results, and Claude
reads them back through the repo or Drive.

## Run it (on your machine / webserver, where Perplexity is reachable)

```bash
export PERPLEXITY_API_KEY=pplx-...        # your key; read only from env, never written to disk
cd paper/tools
python3 pplx_qualify.py                    # default model: sonar-pro
# heavier pass:
python3 pplx_qualify.py --model sonar-reasoning-pro
```

Outputs (git-tracked so they return to Claude):
- `paper/qualification/pplx_results.md`  — human-readable verdicts + sources
- `paper/qualification/pplx_results.json` — machine-readable

## Return the results to Claude

Either:
```bash
git add paper/qualification && git commit -m "Perplexity qualification pass" && git push
```
(Claude reads the pushed files via GitHub), **or** drop the two files in the shared
Google Drive folder (Claude has Drive read access this session).

## What it checks

`claims.json` holds 8 claims — the Hoang 2017 erosion numbers, Guillochon & Loeb's
c/3 stellar ceiling, Semyonov's framing, Lubin's sail velocities, the "no prior
no-go" negative claim, Yurtsever & Wilkinson's CMB ceiling, the ISM heating
sanity-check, and the relativistic-dust destruction limits. Edit or extend that
file to qualify more.

## Notes
- The API key is read only from `PERPLEXITY_API_KEY` and is never written to the
  output files or committed. Do not paste it into any tracked file.
- `sonar-deep-research` is the most thorough model but slower and pricier; for a
  citation cross-check `sonar-pro` or `sonar-reasoning-pro` is plenty.
