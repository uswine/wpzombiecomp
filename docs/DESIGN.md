# Offset Smoker — Door Spring-Hinge Assembly
### Cam-detent snap-close + coiled ribbon (power spring) lift assist

**Status:** Design proposal for review
**Drawings:** `drawings/sheet1-assembly.svg` … `sheet4-torque.svg`
**Sizing tool:** `calculator.html` (open in any browser, works offline)

> **Note on dimensions.** The earlier blueprint work isn't in this repository, so the
> worked example below assumes a typical 24" OD × ¼"-wall pipe cook chamber with a
> 120°-arc × 30"-long top-hinged door (~60 lb). Every number derives from the formulas
> in §4, and `calculator.html` re-solves the whole design for your actual chamber
> diameter, door arc, and door length — plug in the real blueprint dimensions and it
> outputs the spring and cam specs directly.

---

## 1. What the mechanism does

Three distinct behaviors over the 90° door travel, exactly as requested:

| Zone | Door angle | Behavior | What provides it |
|---|---|---|---|
| **Snap zone** | 0°–15° | Door is pulled shut with authority and held sealed (~105 in·lb net closing at the seat) | Cam detent valley + spring-loaded roller follower |
| **Assist zone** | 15°–88° | Ribbon springs carry ~70–75% of the door weight; peak hand effort ≈ **11 lb** instead of **37 lb** bare | Two power-spring canisters on the hinge shaft |
| **Hold-open** | 88°–90° | Door parks vertical with ~2× holding margin; a light tug releases it | Shallow second notch in the same cam |

The key idea is **decoupling**: the ribbon springs provide a nearly flat counterbalance
torque across the whole swing, and the cam detent provides the over-center snap
*only* in the last 15°. Each is tuned independently — follower spring preload sets the
slam/seal force, ribbon spring preload sets how light the door feels. A single spring
trying to do both jobs can't, because the two behaviors want opposite torque signs
near closed.

## 2. Architecture (per door)

```
                        [cook chamber, end view]
   heat shield ─┐            ┌─ standoff bracket (2" air gap)
                ▼            ▼
  ┌────────────────────────────────────────────────────────────┐
  │  LEFT SHAFT END              HINGE LINE              RIGHT  │
  │  power-spring canister   1" shaft in 3 bronze-      power-  │
  │  + preload ratchet       bushed weld-on bosses      spring  │
  │  + SNAP CAM & follower                              canister│
  └────────────────────────────────────────────────────────────┘
```

- **Hinge shaft** — 1.000" CRS (4140 preferred) running the full door width plus 3"
  past each end. The door is welded to the shaft through two gusseted straps, so
  *door and shaft rotate together*. Shaft rides in three weld-on DOM bosses with
  graphite-plugged bronze bushings (no grease to cook off).
- **Power-spring canisters (×2)** — one on each shaft end. Coiled ribbon spring
  (the type in your reference photo, scaled up): inner end keyed to an arbor on the
  shaft, outer end hooked to the case. The case sits in a bracket collar with
  **ratchet teeth on its OD and a pawl on the bracket** — preload is adjusted with a
  spanner in one-tooth clicks, no disassembly, exactly like winding a recoil starter.
- **Snap cam** — a 5" Ø × ½" profiled disc keyed to the left shaft end. A 1.5" cam
  follower roller on a pivot arm, loaded by a 120 lb die spring on the bracket,
  rides the cam. The valley at 0° creates the snap; the shallow notch at 88° is the
  hold-open. Between them the cam is a constant-radius dwell → zero cam torque, so
  the assist zone feels pure spring.
- **Everything outboard** — canisters, cam, and follower all hang on standoff
  brackets 2" off the shell with a polished 16-ga 304 stainless radiation shield in
  the gap. Nothing but the shaft and bosses touches hot steel.

## 3. Why it behaves the way you asked

Torque about the hinge, opening positive (worked example, full curves on Sheet 4):

| θ | Gravity | Springs | Cam | **Net** | Hand @ 20" handle |
|---:|---:|---:|---:|---:|---:|
| 0° | −449 | +550 | −206 | **−105** | held shut |
| 6° | −507 | +546 | −124 | **−85** | pulls itself closed |
| 15° | −584 | +541 | 0 | **−43** | crossover — spring takes over |
| 52° | −734 | +518 | 0 | **−216** | 10.9 lb (37 lb unassisted) |
| 90° | −581 | +495 | 0 | **−86** | held by 172 in·lb notch |

Note the net torque is **monotonically closing through the entire snap zone** — this
took one design iteration to get right. With a 12° linear ramp the fading detent
crossed under the spring surplus at ~9° and the door would have hung there instead of
snapping shut. The fix is a 15° ramp with 0.45" valley depth, which keeps ≥30 in·lb
of closing margin at every angle in the zone. **If you rescale the design, re-check
this with the calculator — it flags a stall automatically.**

Failure mode is benign: if a ribbon spring ever breaks, you simply have a heavy door
again — the hinge still works and the cam still snaps it shut.

## 4. Sizing math (what the calculator implements)

**Door weight & CG.** For a door of arc angle 2α on a chamber of radius R,
length D, plate thickness t: W = R·(2α)·D·t·0.284 + hardware. The CG sits on the arc
bisector at radius r = R·sin α / α.

**Gravity torque.** With hinge pin at position **H** (just off the shell above the
door's top edge) and CG at **G**: L = |HG|, β = angle of H→G below horizontal at
closed. Then T_g(θ) = W·L·cos(θ − β), closing. For the example: W·L = 735 in·lb,
β = 52.3°. Gravity peaks mid-swing (θ = β) — this is why a flat spring curve is the
right counterbalance shape.

**Ribbon springs.** Torque per spring M = k·(n_preload − θ/360). Rate
k = 2πE·I / L_ribbon with I = b·t³/12. Bending stress σ = 6M/(b·t²); keep ≤150 ksi
for chrome-silicon (fatigue life is effectively unlimited at our 0.25-turn working
stroke).

**Cam detent.** Energy method: T_detent = F_follower × (valley depth / ramp angle in
radians). Snap-through requires T_detent(θ) > T_spring(θ) − T_gravity(θ) for all θ in
the ramp.

## 5. Worked-example specification

| Item | Spec |
|---|---|
| Ribbon spring (×2) | Chrome-silicon or 17-7 PH ribbon, **2.00" × 0.085" × 175" (14.6 ft)**, k ≈ 110 in·lb/turn, wound on 1.25" arbor |
| Canister | 6.5" case ID × 7.0" OD × 2.25" internal width, 12-ga case, bolted cover, ratchet teeth on OD |
| Nominal preload | **2.5 turns per spring** (550 in·lb total at closed, σ = 114 ksi) |
| Preload hard limit | **3.25 turns** (σ = 150 ksi) — stamp on the case |
| Snap cam | 5.00" Ø × ½" plate, 2.50" base radius, valley **0.45" deep over 15°**, hold-open notch 0.20" over 8° centered at 88°, stop tab at 93°, 1.000" bore + ¼" keyway |
| Follower | 1.5" Ø cam follower roller on 4" pivot arm, 1" OD × 2.5" medium die spring preloaded to **120 lb** with adjuster bolt |
| Shaft | 1.000" × 40" CRS/4140, ¼" keyways both ends |
| Bushings | Graphite-plugged bronze, 1.00" ID in 1.50" OD DOM weld bosses (×3) |
| Brackets | 3/16" plate standoffs, 2.0" air gap, 16-ga 304 polished heat shield |

### Tuning procedure
1. Door welded and hung, springs relaxed: verify free swing and that the cam roller
   seats in the valley at full close.
2. Wind each canister to 2.5 turns (ratchet clicks are marked on the case).
3. Lift test: door should take roughly 10–12 lb at the handle mid-swing and stay put
   at vertical. Too heavy → +1 click each side, alternating. Pops open at the seat or
   won't snap the last few degrees → back off, or add follower preload instead.
4. Slam check: release from 30°; door must accelerate through the snap zone and seat
   with a thunk, no hesitation.

### ⚠ Stored-energy safety
A wound canister stores real energy (~250 J each at full preload). Each case gets a
**keeper-pin hole** that locks arbor to case for assembly/service — pin in before any
bracket bolt comes out. Wind only with the spanner, never fingers on the ratchet ring.

## 6. Heat management

Outside-shell skin near the door runs roughly 250–400 °F on a hard fire. Spring
temper starts degrading above ~350 °F for music wire, so:
- **Material:** chrome-silicon (good to ~475 °F) or 17-7 PH stainless ribbon — not
  plain blued clock-spring steel.
- **Standoff + shield:** the 2" air gap with a polished stainless shield between
  shell and canister keeps the spring pack under ~200 °F, well inside its rating.
- **Bushings:** graphite-plugged bronze — nothing to melt or cook off; a dab of
  copper anti-seize on the keyways at assembly.

## 7. Alternatives considered — and my recommendation

| Option | Snap-close? | Assist quality | Heat | Verdict |
|---|---|---|---|---|
| **Ribbon power spring + snap cam** (this design) | ✅ crisp, tunable | ✅ near-flat curve, click-adjustable | ✅ with standoff | **Primary recommendation** |
| Helical torsion spring on the hinge line (garage-door stock) + same cam | ✅ same cam | ✅ nearly identical | ✅ | **Best budget fallback** — see below |
| Gas struts | ❌ (fights closing) | ✅ | ❌ seals die ~175 °F | Rejected |
| Counterweight arm | ❌ can't snap | ✅ never wears out | ✅ | The classic, but no snap and a head-height swing hazard |
| Cable + extension spring on a spiral drum | ✅ (drum profile) | ✅ most shapeable curve | ✅ | Works, but the most exposed clutter and a cable to fray |

Honest sourcing note: 250 in·lb-class power springs are **custom-order** parts
(Vulcan Spring, John Evans' Sons, etc. — a few weeks and real money for two). If that
becomes a hassle, the drop-in alternative keeps *everything* in this design — shaft,
cam, follower, brackets, behavior — and swaps each canister for a ~12" length of
off-the-shelf garage-door torsion spring (0.243" wire × 2" ID stock ≈ 39 in·lb/turn;
wound ~3.5 turns via a plain anchor collar) sleeved in a guard tube on the same shaft.
You lose the beautiful coiled-ribbon look and the one-click ratchet adjustment; you
gain ~$60 hardware-store parts. Mechanically they are equivalent here because our
working stroke is only a quarter turn.

So: the mechanism you proposed is genuinely the right one for the feel you described —
the cam gives it the snap a counterweight never can, and the ribbon spring gives the
flattest assist curve of anything that survives the heat. I'd build it as drawn, with
the garage-spring variant in your back pocket if the custom spring quote comes back
ugly.
