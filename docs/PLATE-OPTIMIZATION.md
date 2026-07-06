# Rotary Damper Plates — Design & Optimization Record (Rev C)

**Part:** WPZ-PLT-001 Rev C — Ø24.00 × .375 A36, waterjet cut, **QTY 2 identical**
**Print:** `drawings/plate-24-perforated.svg` / `.pdf` · **CAM geometry:** `drawings/plate-24-perforated.dxf`

## Rev C — outer row enlarged (current)

Review direction: outer-row holes 2–3× the Rev B Ø1.740, and OD-to-hole gap held
at 0.500" min. Key insight enabling this: with the same hole *count* per row, each
row can carry its **own diameter** sized to its own radius — common shutoff and
monotonic flow are preserved. Rev B wasted the outer row (Ø1.74 holes spaced 7.4"
apart because the inner row dictated everything).

| Parameter | Value |
|---|---|
| Pattern | **5 spokes × 2 rows: Row 1 = 5 × Ø4.600 at R9.200, Row 2 = 5 × Ø1.700 at R3.500** |
| Outer row vs Rev B | Ø4.600 = **2.64×** Ø1.740 |
| OD-to-hole gap | **0.500 exact** (R9.200 + Ø4.600/2 = 11.500) |
| Spacing | Row 1 c-c 11.561 (2.51×Ø), Row 2 c-c 4.398 (2.59×Ø), radial web 2.550 (1.5× row-2 Ø) |
| Shutoff twist | **36.0°** (= 180/5) |
| Flow vs twist | 9°=61%, 18°=26%, 27°=2%, 36°=0% — monotonic (verified) |
| Closed seal cover | **0.463" minimum** over all fixed-vs-rotated pairs |
| Open area (aligned) | **94.4 in² = 20.9%** (was 42.8 in² in Rev B — 2.2×) |
| Hub | inner hole edge at R2.650 vs hub R1.750 → 0.900 clear |
| Weight | 38.1 lb per plate |

Alternative sized during the sweep: 7 spokes × 2 rows (Ø3.500 outer / Ø1.650
inner) = 82.3 in², twist 25.7° — choose this if a finer-grained look is preferred
over the last 12 in² of flow.

---

# Rev B record (superseded)

## What changed from Rev A and why

Rev A optimized a single perforated plate at 1.333×Ø spacing (60 holes, 41.7% open).
Design review corrected the intent: **two identical plates stacked, one rotating**
— a rotary damper. That kills Rev A twice over:

1. **Sealing.** At 1.333×Ø spacing the web between holes (0.333×Ø) is far narrower
   than a hole, so the rotated plate's holes can never land fully on solid metal —
   the damper cannot shut off. Rule adopted: **web = 1.5×Ø minimum (c-c = 2.5×Ø)**.
   At the closed position each hole then sits centered in a web with real cover on
   both sides.
2. **Common shutoff angle.** A row with n holes seals at a twist of 180/n. Rev A's
   24/18/12/6 rows would seal at 7.5°/10°/15°/30° — no single lever position closes
   them all. Every row must share one closure angle.

## Architecture selection

Candidates evaluated (all with c-c = 2.5×Ø, 0.50" edge margin, Ø3.5 solid hub):

| Architecture | Shutoff | Flow behavior | Best open area |
|---|---|---|---|
| Mixed counts, odd-multiple family (21/15/9 etc.) | ✅ one angle | ❌ **non-monotonic** — flow re-opens to 67% mid-travel | 56.6 in² |
| **Same count every row (radial spokes)** | ✅ one angle | ✅ **monotonic 100%→0%** | **42.8 in²** |
| Single ring, few large holes (daisy) | ✅ | ✅ monotonic | 55–75 in² |

The mixed-count family was rejected on the measured flow curve: between open and
closed the total flow oscillates wildly (7% at 9° twist, back to 67% at 51°),
making the lever position meaningless. Same-count spokes are the classic rotary
damper solution and were selected. The daisy option (e.g. 6 × Ø3.98 = 74.6 in²)
flows most but abandons the multi-row distribution; noted as an alternative if
the damper feeds a plenum where distribution doesn't matter.

## Optimized result (same-count architecture)

Sweep over hole diameter with rows placed inward at 2.5×Ø pitch until the hub
stops the next row; hole count set by the inner row; open area maximized:

**Ø1.740 holes — 18 total on 9 radial spokes × 2 rows (R10.630 / R6.280).**
The raw optimum was Ø1.747, but that fits the 9th hole with 0.003" of spacing
margin; Ø1.740 restores a healthy margin (inner-row web = 1.52×Ø).

| Parameter | Value |
|---|---|
| Hole diameter | Ø1.740 (18 plcs) |
| Row radii / counts | R10.630 × 9, R6.280 × 9 (spokes aligned, first hole at 0°) |
| Spacing | row pitch 4.350 (2.50×Ø exact); in-row c-c 4.384 min (2.52×Ø) |
| Shutoff twist | **20.0°** (= 180/9) |
| Flow vs twist | 0°=100%, 5°=74%, 10°=41%, 15°=13%, 20°=0% — monotonic (verified) |
| Closed-position seal cover | **0.441" minimum**, verified over all fixed-vs-rotated hole pairs |
| Open area (aligned) | 42.8 in² = 9.5% of gross |
| Edge margin / hub | 0.500" exact / inner hole edge at R5.41, hub untouched |
| Weight | 43.6 lb per plate (87 lb pair) |

A third row does not fit: the next row would sit at R1.93, inside the hub limit
of R2.62 — satisfying "rows continue inward until no additional holes fit."

## Notes for the build

- Plates are cut from the **same DXF** — no left/right handing.
- Deburr both faces; the plates must rotate flush against each other to seal.
- The 20° control span maps nicely to a short lever slot; add end stops at 0°
  and 20° so the operator can't over-travel into the next opening cycle.
- If more open area is ever needed: 1 ring of 9 × Ø2.80 gives 55.4 in² and the
  6 × Ø3.98 daisy gives 74.6 in², both rule-compliant and monotonic — at the cost
  of concentrating flow at one radius.

Regenerate print + DXF with `python3 tools/generate_plate_drawing.py`.
