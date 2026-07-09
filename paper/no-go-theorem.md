# A No-Go Theorem for the Relativistic Propulsion of Macroscopic Condensed Matter

**Allen Hall**

*Draft prepared 2026-07-09. Verification script: `calcs.py` (this repository). All numerical claims in this paper are reproduced by that script; line-by-line chains appear in Appendix A.*

---

## Abstract

We establish that accelerating ordinary macroscopic condensed matter — an intact solid body of characteristic size ≥ 1 cm and ordinary material composition — to β = 0.99 (γ ≈ 7.09) is prohibited under known physics, in the following precise sense: the combined requirements that known physics imposes on any acceleration pathway are mutually contradictory across the entire parameter space of proposed and conceivable mechanisms, except in explicitly bounded limiting cases which we state and own. The argument is a proof by cases over an exhaustive classification of physical couplings. Gravity, the unique interaction that accelerates a body without transmitting force through its structure, is shown to be kinematically capped near 0.5c (≈ 0.7c with maximal black-hole spin) by the innermost-stable-circular-orbit speed — a modal impossibility independent of observation. Every non-gravitational coupling acts on the body's charges and structure and therefore deposits heat governed by an absorptivity that cannot be held at demonstrated laboratory floors across the 14× Doppler sweep of the acceleration; the resulting thermal inequalities, combined with diffraction-limited beam delivery and interstellar-medium heating at 6 GeV per nucleon, close every engineered pathway. At 0.99c the interstellar medium alone imposes a frontal heating load of ~2 MW/m² at the mean galactic density — an equilibrium temperature above the melting point of every silicate and metal short of the most refractory solids — while any shield able to stop the resulting 6-GeV hadronic cascades costs ~10⁶ times the areal mass budget any beam-driven scheme can push. Each claim is tagged as an inequality (impossibility) or a probability (rarity); the two are never conflated. We survey prior art: components of this argument exist in the literature — relativistic rocket energetics (Semyonov 2014, 2018), interstellar-medium damage to relativistic spacecraft (Hoang et al. 2017; Drobny et al. 2021), laser-sail scaling ceilings conceded by the pathway's own advocates (Lubin 2016), gravitational ejection ceilings for stars (Guillochon & Loeb 2015), and a formal environmental speed limit binding only at γ ~ 10⁸ (Yurtsever & Wilkinson 2018) — but a targeted search of the published record finds no prior work stating a no-go theorem for macroscopic condensed matter at ~0.99c over all coupling classes; each prior source stops short of impossibility, addresses a different speed regime, or addresses non-macroscopic bodies. Nature's own record corroborates the theorem: every observed mechanism that accelerates matter to relativistic speeds delivers it as particles or plasma; the fastest observed intact bodies are stars below a percent of c, the theoretical stellar ejection ceiling is c/3, and the fastest known solid objects move at 10⁻⁴ c.

---

## 1. Statement of the problem

### 1.1 The claim

**Theorem (informal).** *No process consistent with known physics accelerates an ordinary macroscopic condensed body to β = 0.99 and leaves it intact, except along explicitly bounded boundary cases (§9) that are themselves closed or rate-suppressed to effective nonexistence.*

Three terms carry weight and are defined now.

**Ordinary macroscopic condensed matter.** A solid body of characteristic linear size L ≥ 10⁻² m, bound by chemical (electromagnetic) cohesion, with tensile/compressive strength S ≤ 10¹⁰ Pa (diamond is ~10¹¹ Pa in ideal crystals; engineering solids are 10⁷–10⁹ Pa), density ρ ~ 10³–2×10⁴ kg/m³, and melting or sublimation temperature T_m ≤ 4,300 K (the highest known, Ta–Hf–C systems). "Intact" means the body arrives as a connected solid, not as vapor, plasma, or a debris cloud.

**β = 0.99.** Then γ = (1−β²)^(−1/2) = 7.0888, and the kinetic energy per unit rest mass is

    E_k/m = (γ − 1)c² = 6.089 c² = 5.47 × 10¹⁷ J/kg.

Every kilogram must be given six times its own annihilation energy. This single number is the antagonist of every argument below.

**Known physics.** The Standard Model plus general relativity, together with the measured properties of condensed matter (strengths, absorptivities, vapor pressures) and the measured astrophysical environment (interstellar densities, black-hole populations). We claim no prophecy about undiscovered physics; the theorem's modality is "prohibited under known physics as combined requirements."

### 1.2 The form of the argument

The theorem is not derived from a single conservation law. It is a **scaling-emergent impossibility**: each requirement in isolation can be met; the conjunction cannot. The proof form is therefore a case analysis over an exhaustive classification of couplings (§3), where each case is closed by an exhibited contradiction — two physics-derived inequalities unsatisfiable simultaneously — swept over the full parameter space, or, where a case cannot be closed by inequality, by an explicit probability bound that is stated as such.

**Epistemic ground rules.** Every load-bearing claim below is tagged:

- **[I]** — inequality: a demonstrated contradiction within known physics. These support the word *impossible*.
- **[P]** — probability: a rarity bound. These support *effectively nonexistent* and never *impossible*.
- **[E]** — engineering-emergent: no principle forbids it, but the required artifact scale is exhibited and its absurdity quantified. These support *closed for any bounded actor* and are flagged as the theorem's honest soft spots.

Observational absence is assigned zero evidentiary weight throughout (§11 explains why); the theorem rests on dynamics, not on surveys.

---

## 2. The energy scale and the two fates of transferred energy

### 2.1 Kinematic anchors

| β | γ | E_k/mc² | E_k (J/kg) |
|------|--------|---------|------------|
| 0.10 | 1.0050 | 0.0050 | 4.53 × 10¹⁴ |
| 0.20 | 1.0206 | 0.0206 | 1.85 × 10¹⁵ |
| 0.50 | 1.1547 | 0.1547 | 1.39 × 10¹⁶ |
| 0.90 | 2.2942 | 1.2942 | 1.16 × 10¹⁷ |
| 0.99 | 7.0888 | 6.0888 | 5.47 × 10¹⁷ |

Between 0.5c and 0.99c the required energy grows by a factor of 39. The theorem's structure follows this cliff: below ~0.5c one heat-free pathway exists in principle (§4); above it, none does.

### 2.2 A correction we impose on ourselves: transferred energy is not deposited heat

A tempting shortcut — "any process transferring 6 mc² to a body must thermalize a ruinous fraction of it in the body" — is **false**, and the theorem must not lean on it. The counterexample is the beamed light sail: a photon of lab energy E reflecting from a mirror receding at β returns with energy E(1−β)/(1+β); the fraction transferred to the sail's kinetic energy is 2β/(1+β) → 0.995 at β = 0.99. Reflected energy leaves at c and never thermalizes in the sail. Only the *absorbed* fraction α heats it, and demonstrated dielectric mirrors reach α ~ 10⁻⁶ at their design wavelength (ion-beam-sputtered stacks; cavity finesse > 10⁵ is routine). Integrating the reflection efficiency over the burn, the incident beam energy needed to reach 0.99c is

    E_inc = ∫₀^0.99 (1+β)/(2β) c² dγ = 5.89 × 10¹⁷ J/kg ≈ 1.08 × E_k,

so at α = 10⁻⁶ the absorbed dose is only ~5.9 × 10¹¹ J/kg. A sail of areal density 1 g/m² (1,000 m² of sail area per kilogram, radiating from two faces) at 1,000 K rejects heat at 2σT⁴ × 1000 m²/kg = 1.13 × 10⁸ W/kg and sheds that dose in ~5.2 × 10³ s. **The naive total-energy thermal budget closes at the design wavelength.** [I — as a counterexample]

This is why the theorem must be, and is, built from the sharper facts: the absorptivity floor cannot survive the Doppler sweep (§6), the beam cannot stay focused for the required time (§7), the interstellar medium is itself a beam the payload cannot dodge (§5), and the sole coupling exempt from all of this is kinematically capped (§4). The remainder of the paper assembles exactly these.

---

## 3. Classification of couplings (the case structure)

**Lemma 1 (exhaustiveness).** *Any process that changes the momentum of a body couples to it through one of:*

1. **(G)** gravity — spacetime curvature acting on mass-energy;
2. **(EM-γ)** electromagnetic radiation — photons absorbed, emitted, or reflected at the body's surface;
3. **(EM-s)** structured electromagnetic force — static or quasi-static fields acting on charges/currents/magnetization carried by the body (coilguns, mass drivers, charged-body accelerators);
4. **(M)** matter exchange — momentum carried by massive particles: rocket exhaust ejected from the body, or external particle beams / medium impinging on it;
5. **(C)** contact — mechanical push through a structure (a limiting case of EM-s at atomic scale; treated with it).

*Justification.* The Standard Model admits four interactions. The strong and weak forces have ranges of 10⁻¹⁵–10⁻¹⁸ m and cannot exert coherent macroscopic forces on a neutral body; they enter only inside case (M) as the mechanism of particle energy deposition. What remains is gravity and electromagnetism in its radiative, quasi-static, and particle-mediated guises. The list is exhaustive under known physics. ∎

**Lemma 2 (the structural dichotomy).** *Gravity is the unique coupling in Lemma 1 that accelerates a body without transmitting force through its structure.* A body in free fall is locally inertial at any coordinate acceleration whatsoever — 1 g or 10¹² g — by the equivalence principle: no load path, no internal stress, no compression, no heat. Every other coupling acts on the body's charges: the force enters at surfaces or throughout the bulk, is redistributed by elastic stress, and is subject to the dissipative response of real materials (finite conductivity, finite absorptivity, hysteresis). The exemption and the equivalence principle are the same fact. Only tidal *gradients* — the part of gravity that cannot be transformed away — stress the body, and they are bounded in §4. ∎

The theorem is then a proof by cases: **(G)** in §4; **(M)-environmental** — the interstellar medium, which every pathway must face — in §5; **(EM-γ)** in §6–7; **(M)-rocket and (EM-s/C)** in §8.

---

## 4. Case G: the gravitational pathway is kinematically capped near 0.5c [I]

Gravity is the one loophole candidate: it accelerates without heating. The question is purely dynamical: *what is the maximum speed to which gravitational dynamics can eject an intact strength-bound body?*

### 4.1 Ejection speed is bounded by pericenter orbital speed

Slingshot ejection — whether a three-body Hills-type exchange or an encounter with a moving black hole — leaves the ejecta with a terminal speed of the order of the orbital speed at the deepest point of the encounter. (A single static-BH flyby is elastic: speed in equals speed out; net gain requires the binary's orbital energy, and the geometric-mean scaling v_ej ~ √(v_orb · v_peri) of the Hills mechanism cannot exceed the pericenter orbital speed itself.) The bound on ejection is therefore the bound on the deepest *survivable, bound-orbit-capable* pericenter.

This logic is established in the literature for stars. Hills (1988) found stellar-binary disruption by a supermassive black hole ejects stars at up to ~4,000 km/s; Guillochon & Loeb (2015), asking precisely the maximum-ejection question ("the fastest unbound stars in the universe"), find the classical mechanism tops out near 10⁴ km/s (~0.03c) and that only the extreme configuration — a star bound to the secondary of a merging massive-black-hole binary — occasionally reaches ~10⁵ km/s, **one third the speed of light**, the ceiling being set by tidal disruption of the star at its deepest survivable pericenter. (The observed record is S5-HVS1 at 1,755 km/s ≈ 0.006c; Koposov et al. 2020.) What follows transposes their tidal-limit logic from self-gravity-bound stars to strength-bound solids, which survive far deeper — and finds the ceiling that replaces c/3.

### 4.2 The floor on pericenter: ISCO, and where strength bites

Two constraints set the floor:

**(a) Dynamics.** Inside the innermost stable circular orbit (ISCO), r_ISCO = 6GM/c² for a Schwarzschild hole, there are no stable orbits: a body that dips inside without precisely tuned angular momentum plunges. The locally measured circular-orbit speed at the Schwarzschild ISCO is

    v_ISCO = c/2,   independent of the black-hole mass.

**(b) Material strength.** The tidal gradient 2GM/r³ across a body of half-length L loads it with stress σ_t ≈ ρ (2GM/r³) L²/2. Survival requires r³ ≥ ρ G M L²/S. For a 1-m rock (ρ = 3,000 kg/m³, S = 10⁸ Pa):

| M_BH | r_strength | r_ISCO | governing | local v_circ at limit |
|-----------|-----------|--------------|-----------|----------------------|
| 10 M☉ | 215 km | 88.6 km | strength | 0.28 c |
| 10³ M☉ | 999 km | 8.9 × 10³ km | ISCO | 0.50 c |
| 10⁶ M☉ | 10⁴ km | 8.9 × 10⁶ km | ISCO | 0.50 c |
| 4.3 × 10⁶ M☉ (Sgr A*) | 1.6 × 10⁴ km | 3.8 × 10⁷ km | ISCO | 0.50 c |

**Correction to an earlier draft:** at the ISCO of a *stellar-mass* hole the tidal gradient is ~4 × 10⁶ s⁻² per meter — a meter-scale rock is shredded there (σ_t ~ 1.4 × 10⁹ Pa ≥ S); an earlier draft's figure of "a few hundred Pa" was wrong by seven orders of magnitude. The conclusion nevertheless *strengthens*: because r_strength ∝ (ML²)^{1/3} while r_ISCO ∝ M, the tidal gradient at the ISCO falls as 1/M², and a meter rock reaches the ISCO with margin at every M ≳ 10³ M☉ (tidal stress ~10⁵ Pa at 10³ M☉, ~0.1 Pa at 10⁶ M☉ — margins of 10³ to 10⁹ against S = 10⁸ Pa). Tidal stress scales as L²: it shreds stars (self-gravity-bound, effective S → 0 at scale) and ignores rocks. The deepest survivable configuration in the universe — a small strength-bound body at the ISCO of a supermassive black hole — tops out at locally measured orbital speed c/2. [I]

**Spin.** For a maximally spinning Kerr hole (a* → 1) the prograde ISCO descends toward GM/c² and orbital speeds rise; astrophysical spins are bounded away from extremality (the Thorne limit a* ≈ 0.998), and we grant 0.6–0.7c as the heroic ceiling. **The Penrose loophole closes itself:** extracting the hole's rotational energy to eject a fragment faster requires the body to split inside the ergosphere with fragment separation velocity exceeding c/2 (Wald 1974) — that is, it requires a relativistic launcher *already operating* at the very speed scale in question, embedded in the payload; the "gravitational" pathway then contains a non-gravitational engine and inherits every dissipative inequality of §§5–8. Passive dynamics gets no Penrose bonus. Even at the heroic ceiling:

    γ(0.5c) = 1.155 → E_k = 0.155 mc²;  γ(0.7c) = 1.400 → E_k = 0.400 mc².

Against the requirement γ = 7.09, E_k = 6.09 mc², the shortfall is a factor of **39 in energy** at 0.5c (15 at 0.7c). No configuration of gravitational dynamics ejects a passive strength-bound body at γ = 7. [I]

### 4.3 Chained encounters do not compound

A second slingshot must present, *in the frame of the already-moving body*, a pericenter deeper (in velocity terms) than the first — but the ISCO speed is an invariant local bound, not a frame artifact: each encounter's gain is capped by the same c/2-scale ceiling in the body's instantaneous frame, with geometrically decaying returns in the lab frame, while the phase-space alignment probability of successive deep encounters multiplies to effective zero. Chains asymptote; they do not diverge. [I for the ceiling; P for the alignment]

### 4.4 Below the ceiling: the sub-0.5c gravitational fluke [P]

Below ~0.5c the pathway exists in principle. It is rate-suppressed to effective nonexistence by the conjunction of: (a) capture phase space — deep survivable passes require quiescent compact objects, while rocks form in metal-rich stellar environments, not black-hole merger neighborhoods, and gravitational-wave capture cross-sections are minuscule; (b) environmental dose — accreting systems bathe the pericenter region in radiation that vaporizes small bodies (an SMBH at even 10⁻⁴ of Eddington outshines the Sun by ~10⁶ within the pericenter distances at issue), while quiescent systems are the rare dark subset; (c) post-ejection erosion in the interstellar medium (§5 applies from 0.1c upward with force). Each factor is a probability statement, and we tag the conjunction [P]: *no inequality forbids a 0.3c pebble; the universe simply has almost no machinery for making one and active machinery for destroying it in transit.*

**Conclusion of Case G: at 0.99c the unique heat-free coupling is closed by dynamics alone — the cupboard cannot hold the item. This is a modal impossibility, not an observational absence.** [I]

---

## 5. Case M-environmental: the interstellar medium is a particle beam no pathway can dodge [I at 0.99c]

Whatever the propulsion, a body at β = 0.99 moving through the interstellar medium (ISM) intercepts, in its own frame, a hadron beam of energy (γ−1)m_p c² = **5.7 GeV per hydrogen atom** at number flux γnβc. This case is propulsion-independent — it binds beamed sails, rockets, mass drivers, and naturally flung rocks equally — which is why it is the keystone of the parameter sweep.

### 5.1 Frontal heating of a thick body

For any body thicker than the hadronic cascade depth (nuclear interaction length ~66 g/cm² in rock, ~25 cm; cascades deposit the bulk of 6-GeV energy within ~1 m), the intercepted power per unit frontal area at ISM density n is

    P = γ n β c (γ−1) m_p c².

At the mean warm-ISM density n = 1 cm⁻³ and β = 0.99: **P = 1.9 × 10⁶ W/m²**. A body radiating from front and back faces equilibrates at

    T_eq = (P/2σ)^{1/4} = 2,030 K   (2,410 K if only the leading face radiates effectively).

| n (cm⁻³) | P (W/m²) | T_eq (K, 2-face) |
|----------|-----------|------------------|
| 0.1 | 1.9 × 10⁵ | 1,140 |
| 1 | 1.9 × 10⁶ | 2,030 |
| 10 | 1.9 × 10⁷ | 3,610 |
| 100 | 1.9 × 10⁸ | 6,420 |

Silicates melt at 1,400–1,900 K; iron at 1,811 K; tungsten at 3,695 K; graphite sublimes near 3,900 K; the most refractory known carbides fail by ~4,300 K. **At the mean galactic density, β = 0.99 melts every ordinary rock and every structural metal. Passage through any region denser than ~20 cm⁻³ — and multi-parsec trajectories do not get to choose their weather — exceeds the failure temperature of every solid known.** [I]

The survivors of the n = 1 cm⁻³ row (tungsten, graphite, ultra-refractory carbides at their limiting temperatures) are not rocks but curated monoliths, and they do not escape: at 2,000–2,400 K they sublime continuously in vacuum; every square meter of frontal surface absorbs a fluence of 2.2 × 10²⁴ six-GeV protons per 10 parsecs (an integrated 2 × 10¹⁵ J/m², delivered as hadronic cascades that amorphize, embrittle, and spall the lattice); and the accompanying dust — ~1% of ISM mass in ~0.1 μm grains — arrives as 4.6 J point detonations (each grain carries the energy of a rifle round in a cross-section of 10⁻¹⁴ m²) at ~10¹¹ impacts per m² per year, cratering the face faster than sputtering alone. Deceleration is symmetric: any mission profile that ends with intact matter must run this gauntlet twice. [I for heating]

The erosion rates have a quantitative literature anchor at lower β. Hoang, Lazarian, Burkhart & Loeb (2017) computed, for quartz surfaces at v = 0.2c: gas bombardment (including heavy-ion track formation) damages a surface layer ~0.1 mm deep over a column N_H ≈ 2 × 10¹⁸ cm⁻² (Karlušić 2017 argues the track model overestimates this; we carry it as an upper anchor), while **dust cratering by explosive evaporation erodes ~0.5 mm over N_H ≈ 3 × 10¹⁷ cm⁻²** — roughly 30× more erosive per unit column than gas, and, at the mean density n = 1 cm⁻³ (3.1 × 10¹⁸ cm⁻² per parsec), **~5 mm of surface per parsec traveled, already at 0.2c**. Drobny et al. (2021) add a subsurface channel that survives even perfect erosion mitigation: implanted H/He accumulates below the surface (Bethe–Bloch range) and drives blistering and exfoliation. At 0.99c every impactor carries 30× the 0.2c energy (5.7 GeV vs. 19 MeV per nucleon) and the thermal channel of §5.1 operates on top. Centimeters of frontal loss per tens of parsecs is the *floor*; the melting inequality above is the ceiling. [I at 0.99c via heating; erosion rates cited at 0.2c and extrapolated — the extrapolation is ours and is conservative in direction, since per-impact energy and cascade depth both grow.]

### 5.2 Thin bodies do not escape by transparency

A 1 g/m² sail is ~10⁻⁴ g/cm² thick; a 6-GeV proton deposits only ~200 eV traversing it (minimum-ionizing dE/dx ≈ 2 MeV per g/cm²), for a deposited power of ~0.07 W/m² — thermally negligible. But the sail pays instead through the damage channel: every traversing proton leaves an ionization track, every ~0.1 μm dust grain removes a crater orders of magnitude larger than itself in a film with no bulk to spare, and over interstellar fluences (10²⁴ p/m² per 10 pc) the accumulated displacement damage in a membrane a few hundred atoms thick destroys the optical properties (α, ε, R) on which the sail's thermal survival depends (§6–7). A thin body trades the heating death for the erosion death. [I on fluence; erosion-rate constants from Hoang et al. 2017]

Nature has already run the L → 0 limit of this experiment. Hoang, Lazarian & Schlickeiser (2015), examining the old proposal (Spitzer 1949; Hayakawa 1972) that relativistic dust grains are ultra-high-energy cosmic-ray primaries, found that sub-micron solid grains (a) cannot be radiation-pressure accelerated beyond γ < 2 even by the most powerful astrophysical sources, and (b) if somehow made relativistic, are destroyed — Coulomb-exploded by collisional charging after sweeping a gas column of only ~10¹⁷ cm⁻² (**0.03 parsecs** at n = 1 cm⁻³). The smallest condensed solids fail *faster* than macroscopic ones (charging stress is a surface effect); the mesoscale is closed at both ends. [I, published]

### 5.3 Shielding is self-defeating

Stopping the cascade requires ~5 nuclear interaction lengths: ~430 g/cm² = **4,300 kg/m²** of graphite. For the beamed-sail pathway, whose entire scheme rests on areal densities of order 1 g/m² (§7), a shield costs **4 × 10⁶ times the mass budget** — the shield requirement and the acceleration requirement are contradictory by six orders of magnitude. For a thick monolith the shield *is* the melting face of §5.1. There is no third option: matter either stops the beam (and takes its power) or passes it (and takes its damage). [I]

---

## 6. Case EM-γ, part 1: the absorptivity floor cannot survive the Doppler sweep [I on the sweep; measured floors]

The beamed sail earned its counterexample status (§2.2) with three simultaneously held properties: α ~ 10⁻⁶, areal density ~1 g/m², high reflectivity R. All three are demonstrated — *separately, at fixed wavelength, at centimeter scale*. The acceleration itself destroys the first.

### 6.1 The 14× sweep

As the sail accelerates 0 → 0.99c, the beam it receives redshifts in its frame by

    D(β) = √((1+β)/(1−β)) = 14.1 at β = 0.99.

A mirror designed for wavelength λ₀ must, over the burn, remain a ppm-absorption mirror from λ₀ to 14λ₀ — more than three octaves.

### 6.2 Why ppm floors are narrow-band physics

Demonstrated α ~ 10⁻⁶ mirrors are quarter-wave dielectric stacks: interference structures whose reflectivity band is set by the index contrast, with fractional bandwidth Δλ/λ ~ 0.2–0.5. Outside the stopband, reflectivity collapses and the field penetrates the full stack: absorption rises by 3–6 orders of magnitude. No interference structure holds a stopband over a 14× ratio: a chirped or stacked-stack design covering three octaves multiplies layer count and thickness — and the absorption of a dielectric stack scales with the material the field samples, so broadening the band raises areal mass and α together. Worse, the sweep runs from 1 μm *into the mid-infrared*, where every oxide and nitride has its reststrahlen/phonon bands (SiO₂ absorbs catastrophically at 8–9.5 μm; a 1-μm-designed stack swept to 14 μm crosses its own lattice resonances, α → 10⁻¹). Metals are genuinely broadband — and improve toward the infrared (Hagen–Rubens, α ∝ √ν) — but their floor across the band is α ~ 10⁻³–10⁻² (finite Drude conductivity), three to four orders above budget. Sweeping α from 10⁻⁶ to even 10⁻⁴ multiplies the absorbed dose of §2.2 by 100; the thermal budget that closed in hours now requires the sail to radiate at powers implying equilibrium temperatures far beyond any coating's damage threshold (§7 quantifies).

**Tagging this claim honestly:** we searched for, and the literature does not provide, a first-principles theorem bounding the absorption of an arbitrary reflector over a fixed band (the Kramers–Kronig relations couple dispersion to loss and forbid a *lossless, massless, broadband* mirror as a consistent set of optical constants, and Drude conductivity floors metals, but no published inequality covers all conceivable structures). The claim is therefore tagged: **[I over every measured mirror class]** — dielectric stacks, photonic crystals, metals, across thousands of published absorption spectra, none sustains α ≤ 10⁻⁵ over a 14× band, and the mid-infrared phonon physics the sweep runs into points the wrong way — **and [E] against undiscovered metamaterials.** A referee who exhibits a ppm-absorption three-octave gram-scale reflector falsifies this tier; none exists in the record.

### 6.4 The defect-statistics wall

All ppm absorptivities on record are measured on centimeter-scale superpolished substrates. A sail is 10⁶–10⁹ times that area, and its survival at ~10¹¹ W/m² of continuous illumination is governed not by mean absorption but by the extreme-value statistics of the *worst* defect on the sheet: a single absorbing inclusion is a burn-through site, and burn-through in a stressed membrane under petawatt illumination is not a local event. Large-area coating at ppm uniformity has never been demonstrated, and area scaling of damage thresholds is a known, adverse, extreme-value regime — the mean is not the operative statistic. [E — a demonstration gap, tagged as such, sitting *underneath* the [I]-level closures of §§6.2–6.3.]

### 6.3 Emissivity closes the pincer from the other side

The sail's only cooling channel is thermal radiation, and a film optically thin at 1 μm is optically thin — hence a *bad emitter* — at its own 3–10 μm emission wavelengths: real sub-micron films have hemispherical emissivities ε ~ 0.01–0.1 unless deliberately structured (which adds mass and its own absorption). Equilibrium temperature scales as ε^(−1/4). Rerunning §2.2's closed budget with honest parameters:

| α (swept) | ε | T_eq for the baseline burn |
|-----------|------|---------------------------|
| 10⁻⁶ | 1.0 | 875 K — closes (the §2.2 idealization) |
| 10⁻⁶ | 0.1 | 1,556 K — marginal |
| 10⁻⁶ | 0.05 | 1,851 K — coating death |
| 10⁻⁴ | 0.05 | > 5,800 K nominal — vaporized long before |

The α that survives a 14× sweep and the ε of a real gram-per-square-meter film cannot coexist with any coating's survival temperature. **The two requirements — reflect a three-octave band at ppm absorption, and radiate the residue from a sub-micron film — are jointly unsatisfiable in measured material physics.** [I over all measured classes; formally [E] against undiscovered metamaterials, and we say so plainly.]

---

## 7. Case EM-γ, part 2: the thermal–diffraction scissors [I/E]

Independently of coatings, the beam must *stay on the sail*, and here two timescales cross.

**Thermal floor on burn time.** Absorbed energy αE_inc must be radiated at ≤ 2εσT⁴ per unit sail area (T ≤ coating limit):

    t_burn ≥ t_min = α E_inc ρ_A / (2εσT⁴),   ρ_A = areal density.

**Diffraction ceiling on burn time.** A transmitter of aperture D at wavelength λ holds its spot within a sail of size s only out to d_max ≈ sD/(2.44λ); the sail, spending the burn near c, exits the focus after

    t_burn ≤ t_max = s D / (2.44 λ ⟨β⟩ c).

The scissors condition t_min ≤ t_max yields the required aperture:

    D ≥ 2.44 λ ⟨β⟩ c · α E_inc ρ_A / (2εσT⁴ s).

Sweeping the parameter space:

| α | ε | T (K) | s (m) | D required |
|--------|------|-------|-------|-----------------|
| 10⁻⁶ | 1.0 | 1,000 | 30 | 117 km |
| 10⁻⁶ | 0.5 | 1,500 | 30 | 46 km |
| 10⁻⁵ | 0.1 | 1,500 | 100 | 695 km |
| 10⁻⁴ | 0.05 | 1,000 | 30 | 2.3 × 10⁵ km (18 Earth diameters) |

Read the first row honestly: with the idealized (§2.2) sail, the aperture is "only" ~100 km of optically coherent, phase-locked emitter — pushing ~1.1 × 10¹⁴ W per kilogram of payload (a 100-kg body needs ~11 PW, five hundred times humanity's mean power output, held for over an hour at micro-radian pointing across ~10 AU), while the sail rides at ~5,800 g mean acceleration (a bare wafer survives, machinery does not). No physical law forbids a 100-km laser; we tag the row [E] and place it in the boundary cases. But the idealized row is not available: §6 showed α cannot hold 10⁻⁶ across the sweep, and ε cannot reach 1 in a gram-scale film. With honest optical constants the aperture inflates to planetary diameters and the beam power to stellar fractions — and §5 has already charged the sail 4 × 10⁶× its mass budget for ISM shielding it cannot buy, then destroys its coating in transit anyway. **The conjunction closes: every point of the (α, ε, T, s, ρ_A) space fails at least one of — Doppler-band absorption (§6.2), emissivity (§6.3), diffraction aperture (§7), ISM (§5).** [I over measured physics, with the [E] boundary row owned in §9.]

Slowing down does not help: a longer, gentler burn covers more distance, and the aperture requirement *grows* with burn distance. The scissors cut in both directions; this is why the eon-timescale boundary case (§9.1) must abandon beaming altogether.

---

## 8. Cases M-rocket, EM-s, C: onboard and structured-force propulsion [I]

### 8.1 The rocket inequality

The relativistic rocket equation for exhaust speed w gives the mass ratio

    m₀/m₁ = [(1+β)/(1−β)]^(c/2w).

| β | chemical (w ≈ 1.5×10⁻⁵c) | fission fragments (0.05c) | fusion (0.1c) | photon (c) |
|------|--------------------------|---------------------------|----------------|------------|
| 0.10 | 10⁸⁷² | 7.4 | 2.7 | 1.11 |
| 0.50 | 10⁴⁷⁷¹ | 5.9 × 10⁴ | 243 | 1.73 |
| 0.90 | 10¹²⁷⁸⁸ | 6.1 × 10¹² | 2.5 × 10⁶ | 4.36 |
| 0.99 | 10²²⁹⁸⁹ | ~10²³ | 3.1 × 10¹¹ | 14.1 |

Chemical and fission propulsion are dead at any relativistic β (mass ratios exceeding the particle count of the observable universe). Fusion at 0.99c demands a mass ratio of 3 × 10¹¹ — a Ceres of fuel per kilogram delivered — before a single inefficiency is charged. [I]

### 8.2 The waste-heat inequality

Any onboard converter of efficiency η handling the energy flow leaves W = E_k(1−η)/η in the ship. At β = 0.99 and a generous η = 0.8: W = 1.37 × 10¹⁷ J/kg. Radiating at a space-reactor-class 200 W per kilogram of ship: **2.2 × 10⁷ years**. At a fantastical 1 kW/kg and η = 0.99: 175,000 years — during which the "burn" is limited by its own radiator, and the ship crosses the §5 gauntlet at increasing β with its radiators forward. The photon rocket avoids reaction-mass arithmetic (mass ratio 14.1) but must generate and *emit as light* 7.0 mc² = 6.3 × 10¹⁷ J per delivered kilogram through an onboard engine whose every percent of inefficiency is 10¹⁵ J/kg of onboard heat: it is the waste-heat inequality in its purest form. Onboard pathways fail on the conjunction (mass ratio) ∧ (waste heat): each is independently fatal at 0.99c. [I]

### 8.3 Structured-force machines (mass drivers, coilguns, charged accelerators)

Any external machine gripping the body through electromagnetic structure transmits force through the body's own material: acceleration is capped by strength,

    a ≤ S/(ρL) ≈ 3.3 × 10⁴ m/s² ≈ 3,400 g   (1-m body at S = 10⁸ Pa, ρ = 3,000),

so the track length obeys

    ℓ ≥ (γ−1)c²ρL/S ≈ 1.6 × 10¹³ m ≈ 110 AU  (at 100% of ultimate strength; ~1,100 AU at a sane working stress).

An accelerator a hundred to a thousand AU long, aligned and powered to deliver 5.5 × 10¹⁷ J/kg with the payload's dissipative response (eddy currents in any conductor under changing fields, hysteresis, flux penetration in superconductors driven at their critical limits) charging heat *into the payload* throughout — and the exit door opens onto §5. No single inequality kills the idealized frictionless version; the conjunction (track scale [E]) ∧ (payload dissipation floor [I-material]) ∧ (ISM at exit [I]) does. The body also cannot be gripped gravitationally to evade the strength cap — that is Case G, already closed. [I∧E]

---

## 9. Boundary cases, owned in the main text

The theorem's honesty rests on stating exactly what it does not forbid.

**9.1 Eon-timescale acceleration.** [Open in principle] Nothing above forbids accelerating a body gently for geological time: at a sustained 10⁻³ m/s² proper acceleration, 0.99c arrives after ~70,000 years — and ~5 × 10²⁰ m of path, **eighteen kiloparsecs, a galactic radius**. The heat-rejection inequalities all relax as t_burn → ∞; everything charged per unit *distance* does not. Beamed schemes must hold the §7 focus over that whole path — apertures beyond planetary scale, the scissors again; onboard schemes still pay §8.1's mass ratios in full (mass ratio is time-independent); the §5 ISM dose is charged per parsec, and an 18-kpc run at climbing β through unchosen interstellar weather is §5 compounded thousands of times over; and any machine holding itself together for 10⁵ years exceeds every engineering-lifetime datum by orders of magnitude. We class this case [E]: not forbidden by inequality, closed for any bounded actor, and — decisively — the ISM and Doppler constraints it cannot relax still bind at the destination velocity.

**9.2 The sub-0.5c gravitational fluke.** [P] As §4.4: a strength-bound pebble ejected at 0.1–0.5c by a deep encounter with a quiescent massive black hole violates no inequality. Its production channels are rate-suppressed (phase space, environment), and §5 erodes it in transit (a 0.3c pebble intercepts ~7 kW/m² in a 10 cm⁻³ cloud — thermally survivable at ~500 K equilibrium, but cratering- and sputtering-limited on kiloparsec paths at Hoang-et-al. erosion rates). We bound, we do not forbid.

**9.3 The idealized single-wavelength wafer.** [E] The §7 first row: a gram-scale bare wafer, a 100-km coherent aperture, petawatts, and a trajectory short enough to out-run coating damage. Every added requirement (a payload; deceleration; arrival intact through §5; the Doppler sweep it cannot actually evade) re-closes it. It survives as a reminder that the theorem is about *macroscopic intact matter*, not about whether photons push.

**9.4 What the theorem never claimed.** Particles and plasma reach γ ≫ 7 daily, in nature (cosmic rays to 10²⁰ eV) and in machines. The theorem is precisely about the gap between them and condensed matter: binding energies of eV per atom versus kinetic demands of GeV per nucleon — a nine-order-of-magnitude mismatch between what holds a solid together and what the journey delivers to every atom of its leading face.

---

## 10. Prior art

A targeted literature search (fanned across the propulsion, astrophysics, materials, and thermodynamics corpora, with adversarial verification of every citation below against its primary source) finds **no published no-go theorem for macroscopic condensed matter at ~0.99c**. This is a negative claim and we hold it at the confidence a negative deserves — the search was broad, not exhaustive. The components have distinguished pedigrees; we claim novelty for the assembly, the coupling-classification closure, and the ISCO ceiling for strength-bound bodies.

- **The closest prior art: Semyonov.** Oleg G. Semyonov, "Relativistic rocket: Dream and reality" (Acta Astronautica 99, 2014, 52–70) and "Pros and cons of relativistic interstellar flight" (Acta Astronautica 151, 2018, 736–742; arXiv:1807.08608) identifies exactly two physical factors "that stand against our dream of the stars — thermodynamics and radiation hazard": the onboard power generator and heat-disposing radiator grow the dry mass and cap the achievable speed (our §8.2), and ship-frame interstellar gas "turns into oncoming flux of hard ionizing radiation" while relativistic dust causes mechanical damage (our §5). He is the nearest published position to this paper's — and he explicitly stops short of it, proposing antimatter fuel, shielding, and beamed-matter propulsion as mitigations rather than concluding impossibility. Where he offers engineering hope, our §§5–8 offer the closing inequalities.
- **A published formal ceiling — in a different regime.** Yurtsever & Wilkinson, "Limits and signatures of relativistic spaceflight" (Acta Astronautica 142, 2018, 37–44; arXiv:1503.05845) prove the vacuum itself imposes a sub-light ceiling on any macroscopic baryonic object: blueshifted CMB photons exceed the e⁺e⁻ pair-production threshold when γ(1+β) ≥ 2.47 × 10⁸, i.e. γ ~ 10⁸, with drag and ionization channels opening from γ(1+β) ~ 10⁴. This is the only formal no-go-style theorem we find in print, and it is complementary to ours: at γ = 7.09 the CMB blueshifts to a harmless ~10⁻² eV (which is why the CMB appears nowhere in our tiers). Their theorem caps the far ultrarelativistic regime from the environment side; ours closes the 0.99c regime from the coupling-and-materials side.
- **Beamed propulsion, by its own advocates.** Marx (Nature 211, 1966) proposed laser propulsion to relativistic speeds; Redding (Nature 213, 1967) identified the deceleration problem at once. Forward (J. Spacecraft & Rockets 21, 1984) developed the staged lightsail. Lubin, "A Roadmap to Interstellar Flight" (JBIS 69, 2016; arXiv:1604.01356) is the maximal contemporary case for directed energy, and its own numbers are the concession: a full DE-STAR 4 — a 50–70 GW, kilometer-scale phased array — propels a *gram-scale wafer* with a 1 m sail to ~0.26c; the same system takes a 100 kg payload only to ~0.01c and 10⁵ kg to ~10³ km/s. Kulkarni, Lubin & Zhang (AJ 155, 155, 2018; arXiv:1710.10732) confirm diffraction caps gram-scale craft near 0.2c. The steep mass–velocity cliff in the advocates' own roadmap is §7's scissors, observed from inside. The Breakthrough Starshot materials literature (Atwater et al., Nature Materials 17, 2018; Ilic, Went & Atwater, Nano Letters 18, 2018) states the reflectivity–mass–absorption–emissivity trades of §6 as the central unsolved sail problem — at 0.2c, where the Doppler sweep is 1.22× rather than our 14×.
- **ISM damage.** Hoang, Lazarian, Burkhart & Loeb (ApJ 837, 5, 2017; arXiv:1608.05284) give the canonical quantitative treatment at 0.2c: gas (with heavy-ion track formation) damages quartz to ~0.1 mm depth over N_H ~ 2 × 10¹⁸ cm⁻² (Karlušić, arXiv:1701.04319, argues this overestimates track damage — carried here as a qualification); dust cratering erodes ~0.5 mm over N_H ~ 3 × 10¹⁷ cm⁻², ~30× more erosive per column. Antecedents: Early & London (2000, 2018) on lightsail dust damage. Drobny et al. (ApJ 908, 248, 2021; arXiv:2103.07517) and Cohen et al. (ApJ 930, 74, 2022) add subsurface gas-accumulation blistering. All frame damage at 0.1–0.3c as an engineering challenge; our §5 extends the same mechanism inventory to β = 0.99, where per-nucleon energy crosses into the GeV hadronic-cascade regime and the *thermal* channel becomes independently fatal — that extension is ours, and it converts a challenge into an inequality.
- **The natural analog.** Hoang, Lazarian & Schlickeiser (ApJ 806, 255, 2015; arXiv:1412.0578): sub-micron grains cap at γ < 2 under radiation-pressure acceleration by the most powerful sources known, and relativistic grains are Coulomb-exploded after ~10¹⁷ cm⁻² of transit — effectively retiring the Spitzer (1949)/Hayakawa (1972) relativistic-dust cosmic-ray hypothesis. Published, peer-reviewed non-survivability of condensed matter at relativistic speed, in the L → 0 limit.
- **Gravitational ejection ceilings.** Hills (Nature 331, 687, 1988) founded binary-disruption ejection (~4 × 10³ km/s). Guillochon & Loeb, "The fastest unbound stars in the universe" (ApJ 806, 124, 2015; arXiv:1411.5022) find the classical mechanism caps near 10⁴ km/s (0.03c) and that stars bound to the secondary of a merging massive-black-hole binary are occasionally ejected at ~10⁵ km/s — c/3 — with the ceiling set by tidal disruption at the deepest survivable pericenter. The observed record: S5-HVS1, 1,755 km/s (Koposov et al., MNRAS 491, 2020). Our §4 transposes their tidal-limit logic from self-gravity-bound stars to strength-bound solids, which survive deeper, and finds the mass-independent ISCO ceiling c/2 (≲0.7c Kerr). We find no prior statement of this ceiling for strength-bound bodies; it is the theorem's decisive novel step, and the step on which the unconditional 0.99c claim rests.
- **Thermodynamic bounds: the theorem that is not there.** A universal entropy-production lower bound for "any coupling that accelerates a body" would upgrade Lemma 2 from classification to derivation. Our search did not find one, and the structure of the finite-time-thermodynamics literature explains why: its bounds (optimal-transport dissipation bounds, Aurell et al. 2011; the thermodynamic-speed-limit family) price *state-space* change per unit time and vanish in the slow-driving limit, while quantum speed limits (Margolus–Levitin type) are non-binding by tens of orders of magnitude at macroscopic energies. **We therefore do not claim the original proposal's Hypothesis 3 ("every coupling has finite irreversibility") as a theorem.** The heat floors in this paper come from measured material response — α, ε, conductivity — not from a general principle; and the one coupling with no material response, gravity, is exactly the one we close kinematically. Hypothesis 3 survives only in the amended, case-checked form: *every coupling either deposits heat in the payload through its measured material response, or is tidally/kinematically self-limited below ~0.5c.*

**The assembly is the theorem.** Each literature above closes its own corridor and stops. Semyonov closes rockets and gestures at sails; Lubin champions sails and concedes grams; Hoang et al. erode sails and stop at 0.3c; Guillochon & Loeb cap gravity and consider only stars. Assembled, with the coupling classification of §3 guaranteeing no unexamined corridor remains, they are no longer a collection of engineering complaints but a closed case analysis. That closure — and the ISCO ceiling that seals the one heat-free door — is what this paper adds.

---

## 11. Discussion: nature's record, read correctly

The corroboration (never a premise): nature runs every accelerator we cannot. Supernovae, kilonovae, SMBH slingshots, pulsar winds, jets — 13.8 Gyr of them, across ~10¹¹ galaxies. The census of what these deliver at relativistic speed is unanimous: **particles and plasma**. Kilonova ejecta at 0.1–0.3c arrive as r-process plasma. Jets at γ ~ 10–50 are ionized flows. Cosmic rays reach macroscopic *energies* (10²⁰ eV) in single nuclei. Meanwhile the record for observed intact-body speed stands at S5-HVS1's 1,755 km/s ≈ 0.006c (a star; S4714's pericenter dash at ~0.08c is a momentary orbital speed, also a star); the theoretical stellar ceiling is Guillochon & Loeb's occasional c/3; and for solids the record-holders are the three known interstellar objects at 26–60 km/s — 10⁻⁴ c. The theorem explains this record; the record did not produce the theorem. We assign the non-observation of fast rocks zero weight (a dark meter rock at 0.5c has detection probability ≈ 0 in every existing survey: expected detections ≈ 0 under either hypothesis) — and note that the *positive* record, of what relativistic accelerators demonstrably emit, is Bayesian corroboration of exactly the dichotomy the theorem proves: nature's mechanisms all couple through the channels of Lemma 1, and everything they fling fast, they first tear apart.

The claim's modality bears final restatement. We have not proven a law of nature; we have exhibited that the requirements known physics imposes — six annihilation-units per kilogram, delivered through couplings that are either dissipative in measured matter or capped at half lightspeed by orbital dynamics, across a medium that charges GeV per nucleon at the door — are *jointly contradictory* for intact macroscopic solids at β = 0.99, everywhere in parameter space, with the boundary cases of §9 explicitly bounded. New physics could void the theorem; nothing within known physics does. The universe, on current evidence, does not ship rocks at lightspeed — not because no one has tried hard enough, but because the shipping department's every door is either on fire or half a c too slow.

---

## References

1. Ackeret, J. (1946). "Zur Theorie der Raketen." *Helvetica Physica Acta* 19, 103–112. (Relativistic rocket equation.)
2. Atwater, H. A., et al. (2018). "Materials challenges for the Starshot lightsail." *Nature Materials* 17, 861–867.
3. Aurell, E., Mejía-Monasterio, C., & Muratore-Ginanneschi, P. (2011). "Optimal protocols and optimal transport in stochastic thermodynamics." *Physical Review Letters* 106, 250601.
4. Cohen, A. N., et al. (2022). *The Astrophysical Journal* 930, 74. arXiv:2201.02721. (Blistering thresholds and leading-edge erosion for relativistic spacecraft.)
5. Drobny, J., Cohen, A. N., Curreli, D., Lubin, P., Pelizzo, M., & Umansky, M. (2021). "Damage to relativistic interstellar spacecraft by ISM impact gas accumulation." *The Astrophysical Journal* 908, 248. arXiv:2103.07517.
6. Early, J. T., & London, R. A. (2000). "Dust grain damage to interstellar laser-pushed lightsail." *Journal of Spacecraft and Rockets* 37, 526–531; London, R. A., & Early, J. T. (2018). *JBIS* 71, 133.
7. Forward, R. L. (1984). "Roundtrip interstellar travel using laser-pushed lightsails." *Journal of Spacecraft and Rockets* 21, 187–195.
8. Guillochon, J., & Loeb, A. (2015). "The fastest unbound stars in the universe." *The Astrophysical Journal* 806, 124. arXiv:1411.5022.
9. Hayakawa, S. (1972). "Cosmic ray dust grains." *Astrophysics and Space Science* 16, 238. (Relativistic-dust UHECR hypothesis.)
10. Hills, J. G. (1988). "Hyper-velocity and tidal stars from binaries disrupted by a massive Galactic black hole." *Nature* 331, 687–689.
11. Hoang, T., Lazarian, A., & Schlickeiser, R. (2015). "On origin and destruction of relativistic dust and its implication for ultrahigh energy cosmic rays." *The Astrophysical Journal* 806, 255. arXiv:1412.0578.
12. Hoang, T., Lazarian, A., Burkhart, B., & Loeb, A. (2017). "The interaction of relativistic spacecrafts with the interstellar medium." *The Astrophysical Journal* 837, 5. arXiv:1608.05284.
13. Ilic, O., Went, C. M., & Atwater, H. A. (2018). "Nanophotonic heterostructures for efficient propulsion and radiative cooling of relativistic light sails." *Nano Letters* 18, 5583–5589.
14. Karlušić, M. (2017). arXiv:1701.04319. (Unrefereed comment arguing ref. 12's ion-track damage model overestimates gas damage; carried here as a qualification.)
15. Koposov, S. E., et al. (2020). "Discovery of a nearby 1700 km/s star ejected from the Milky Way by Sgr A*." *Monthly Notices of the Royal Astronomical Society* 491, 2465–2480. (S5-HVS1.)
16. Kulkarni, N., Lubin, P., & Zhang, Q. (2018). "Relativistic spacecraft propelled by directed energy." *The Astronomical Journal* 155, 155. arXiv:1710.10732.
17. Lubin, P. (2016). "A roadmap to interstellar flight." *Journal of the British Interplanetary Society* 69, 40–72. arXiv:1604.01356.
18. Marx, G. (1966). "Interstellar vehicle propelled by terrestrial laser beam." *Nature* 211, 22–23.
19. Purcell, E. M. (1963). "Radioastronomy and communication through space." Brookhaven Lecture Series BNL-658.
20. Redding, J. L. (1967). "Interstellar vehicle propelled by terrestrial laser beam." *Nature* 213, 588–589.
21. Semyonov, O. G. (2014). "Relativistic rocket: Dream and reality." *Acta Astronautica* 99, 52–70.
22. Semyonov, O. G. (2018). "Pros and cons of relativistic interstellar flight." *Acta Astronautica* 151, 736–742. arXiv:1807.08608.
23. Spitzer, L. (1949). "The dynamics of the interstellar medium. III." *The Astrophysical Journal* 109, 337. (Radiation-pressure grain acceleration.)
24. von Hoerner, S. (1962). "The general limits of space travel." *Science* 137, 18–23.
25. Wald, R. M. (1974). "Energy limits on the Penrose process." *The Astrophysical Journal* 191, 231–233.
26. Yurtsever, U., & Wilkinson, S. (2018). "Limits and signatures of relativistic spaceflight." *Acta Astronautica* 142, 37–44. arXiv:1503.05845.

*Citations 2–5, 8, 11, 12, 14–17, 21, 22, 26 were verified against their primary sources (abstract-level verbatim checks, 3-voter adversarial review) during the preparation of this paper; the remainder are standard historical references.*

---

## Appendix A: numerical verification chains

Plain-text, line-by-line; reproduced by `calcs.py`.

```
A1. gamma(0.99) = 1/sqrt(1-0.99^2) = 1/sqrt(0.0199) = 7.0888
A2. KE/kg = (7.0888-1)*(2.998e8)^2 = 6.0888*8.988e16 = 5.472e17 J/kg
A3. Reflected Doppler (1-0.99)/(1+0.99) = 0.01/1.99 = 1/199
A4. Sail-frame sweep sqrt(1.99/0.01) = sqrt(199) = 14.1
A5. E_inc = int_0^0.99 (1+b)/(2b) c^2 dgamma = 5.89e17 J/kg (numerical, N=2e6 steps)
A6. Absorbed at alpha=1e-6: 5.89e11 J/kg
A7. Sail 1 g/m^2 -> 1000 m^2/kg; P_rad = 2*eps*sigma*T^4*1000
    at eps=1, T=1000K: 2*5.67e-8*1e12*1000 = 1.134e8 W/kg
A8. t_min = 5.89e11/1.134e8 = 5.19e3 s = 1.44 h
A9. ISM flux (ship frame) = gamma*n*beta*c = 7.0888*1e6*0.99*2.998e8
    = 2.104e15 protons/m^2/s at n=1 cm^-3
A10. E/proton = 6.0888*938.27 MeV = 5.713 GeV = 9.153e-10 J
A11. P_ISM = 2.104e15*9.153e-10 = 1.926e6 W/m^2
A12. T_eq(2-face) = (1.926e6/(2*5.6704e-8))^0.25 = 2,030 K
A13. Dust: grain m = (4/3)pi(1e-7)^3*2000 = 8.4e-18 kg;
     E = 6.0888*8.4e-18*8.988e16 = 4.6 J
A14. Shield: 5*86 g/cm^2 = 430 g/cm^2 = 4,300 kg/m^2; /1e-3 kg/m^2 = 4.3e6x
A15. ISCO: r = 6GM/c^2; local v_circ = c/2 (Schwarzschild, any M)
A16. Tidal stress, 1-m rock, 10 Msun ISCO (r=88.6 km):
     2GM/r^3 = 2*1.327e21/(8.86e4)^3 = 3.82e6 s^-2
     sigma_t = 3000*3.82e6*0.25/2 = 1.4e9 Pa  (FAILS: strength governs)
A17. Same rock, 4.3e6 Msun ISCO (r=3.81e10 m): 2GM/r^3 = 2.06e-5 s^-2
     sigma_t = 3000*2.06e-5*0.25/2 ~ 8e-3 Pa  (margin ~1e10: ISCO governs)
A18. gamma(0.5) = 1.1547; KE ratio (gamma(0.99)-1)/(gamma(0.5)-1) = 39.4
A19. Rocket, photon: m0/m1 = gamma(1+beta) = 7.0888*1.99 = 14.1
A20. Rocket, fusion w=0.1c: log10(MR) = log10(199)/(2*0.1) = 11.49 -> 3.1e11
A21. Waste heat, eta=0.8: 5.472e17*0.25 = 1.368e17 J/kg
     t at 200 W/kg = 6.84e14 s = 2.17e7 yr
A22. Scissors aperture: D = 2.44*lam*<b>*c*alpha*E_inc*rho_A/(2 eps sigma T^4 s)
     baseline (1e-6,1.0,1000K,30m,1e-3): D = 117 km
     swept (1e-4,0.05,1000K,30m,1e-3): D = 2.3e5 km
A23. Mass-driver: a_max = S/(rho L) = 1e8/3000 = 3.33e4 m/s^2 = 3,400 g
     l = (gamma-1)c^2/a_max = 5.472e17/3.33e4 = 1.64e13 m = 110 AU
     (at ultimate strength; x10 at working stress -> ~1,100 AU)
A24. 10 pc transit at 0.99c: t = 10*3.086e16/(0.99*2.998e8) = 1.04e9 s = 33 yr
     fluence = 2.104e15 * 1.04e9 = 2.19e24 p/m^2
```

## Appendix B: corrections adopted during adversarial review

Positions tested and failed during review, recorded so they are not resurrected: (1) "transferred energy = deposited heat" — false, §2.2; (2) "any absorption at 6 mc² = vaporization" — false at design wavelength, §2.2; (3) "thin films can't be low-absorption mirrors" — false as stated (the true constraint is the three-way trade, §6); (4) "no surface survives the CW intensity" — false at cm scale (the true constraint is defect statistics at sail area); (5, 6) "gravitational acceleration/turning stresses the payload" — false, equivalence principle, §3 Lemma 2; (7) "spaghettification kills slingshotting rocks" — false around SMBHs — and the earlier draft's own tidal number for a 10 M☉ ISCO was wrong in the favorable direction (corrected, §4.2: stellar-mass ISCOs do shred meter rocks; SMBH ISCOs do not, and the c/2 ceiling is unchanged); (8) "the stellar velocity ceiling applies to rocks" — false, scaling inverts, §4.2; (9) "thermal mass dooms rocks in flybys" — false (transient skin depth is cm-scale); (10) "surveys would show fast rocks" — zero evidentiary weight either way, §11; (11) "photon rocket and sail fail identically" — false, they fail by distinct inequalities (§8.2 vs. §§6–7).
