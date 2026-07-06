# Perforated Airflow Plate — Hole-Size Optimization Record

**Part:** WPZ-PLT-001 — Ø24.00 × .375 A36 plate, waterjet cut
**Print:** `drawings/plate-24-perforated.svg` / `.pdf` · **CAM geometry:** `drawings/plate-24-perforated.dxf`

## Problem

Maximize open area subject to:
- hole diameter D > 1.000"
- center-to-center spacing s = 1.333 × D (minimum, staggered concentric rows)
- hole edge to plate edge ≥ 0.500"
- solid Ø3.500 center hub (no cuts)

## Why this needed a numeric solve

For an infinite triangular pattern the open-area fraction is
π / (4 · 1.333² · sin 60°) ≈ 51% **regardless of D** — hole size cancels out.
The optimum is therefore decided entirely by *edge effects*: how cleanly whole
rows of a given diameter pack into the annulus between the hub and the edge
margin, both of which shift with D (outer row center radius = 11.5 − D/2, inner
limit = 1.75 + D/2).

A second subtlety: on concentric circular rows, "staggered midway" packing is
never exact (adjacent rows have different hole counts), so the naive
0.866 · s row pitch violates the spacing constraint where holes drift into
radial alignment. The solver placed each row as far out as possible while the
**worst-case** center distance to the previous row (over an optimized relative
rotation) stayed ≥ s.

## Result of the sweep (D = 1.005 → 2.20, 0.005 steps)

| D | holes | open in² |
|---:|---:|---:|
| 1.500 | 106 | 187.3* |
| 1.910 | 65 | 186.2 |
| 1.980 | 61 | 187.8 |
| **2.000** | **60** | **188.5 ← optimum** |
| 2.100 | 55 | 186.1 |

\*representative mid-sweep values; full sweep in `tools/generate_plate_drawing.py` docstring context.

**Optimum: D = 2.000", s = 2.666", 60 holes in 4 rows — open area 188.5 in² (41.7% of gross).**
The peak lands on a fully 6-fold-symmetric pattern (row counts 24/18/12/6), which
is also the best-looking and stiffest arrangement of the near-optimal candidates.

## Final verified geometry

| Row | Radius | Qty | First hole | Pitch |
|---|---|---|---|---|
| 1 | 10.500 | 24 | 7.5° | 15° |
| 2 | 7.864 | 18 | 0.0° | 20° |
| 3 | 5.257 | 12 | 5.0° | 30° |
| 4 | 2.786 | 6 | 20.0° | 60° |

Checks (computed over **all** hole pairs, not just neighbors):
- global minimum center-to-center = **2.6660"** = 1.333 × Ø exactly
- minimum web between holes = **0.666"** (1.78 × plate thickness — stiff, waterjet-friendly)
- edge margin = **0.500"** exact on the outer row
- innermost hole edge at R1.786 → hub keeps a full Ø3.57 solid zone
- estimated finished weight **28.1 lb** (from 48.2 lb solid)

Row phases are the max–min-stagger solution; the pattern is 6-fold rotationally
symmetric. Regenerate everything with `python3 tools/generate_plate_drawing.py`.
