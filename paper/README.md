# Why Rocks Do Not Go 0.99c

*A Coupling-Class Impossibility Argument for Intact Macroscopic Condensed Matter at
β ≈ 0.99 in Ordinary Interstellar Environments.*

Research paper arguing that, under known physics, no demonstrated or physically credible
pathway both accelerates an ordinary macroscopic condensed body (intact solid ≥ 1 cm) to
β = 0.99 and transports it intact through ordinary interstellar matter — a proof by cases
over an exhaustive coupling classification, with every closure tagged [I] contradiction /
[P] rarity / [E] engineering scale. Draft 2, revised after a second adversarial review
round (corrections logged in the paper's Appendix B).

## Contents

| File | Description |
|------|-------------|
| `no-go-theorem.md` | The paper (canonical source) |
| `no-go-theorem.pdf` | Rendered PDF |
| `calcs.py` | Verification script — reproduces every numerical claim in the paper |
| `calcs_output.txt` | Captured output of `calcs.py` |
| `build_pdf.py` | Rebuilds the PDF from the Markdown source (`pip install markdown-pdf`) |

## Reproducing

```bash
python3 calcs.py          # verify every number
python3 build_pdf.py      # rebuild the PDF
```

## Structure of the argument

- **Case G (gravity)** — the unique heat-free coupling; closed channel-by-channel: flybys
  are elastic, moving-hole gains cap at ~0.03c/pass, bound-exchange ejection caps near the
  ISCO speed ~0.5c per encounter, and chains die because exchange capture collapses above
  the first boost's exit speed.
- **Case M-environmental (interstellar medium)** — propulsion-independent keystone: at
  0.99c the ISM is a 5.7 GeV/nucleon hadron beam depositing ~2 MW/m² at mean density;
  equilibrium temperature exceeds the melting point of ordinary solids.
- **Case EM-γ (beamed sail)** — the 14× Doppler factor is a conserved burden: fixed-frequency
  systems impose it on the sail, chirped transmitters relocate it to 71-nm VUV source optics;
  no measured material class carries it at either end. Emissivity and the thermal–diffraction
  scissors close the rest.
- **Cases M-rocket / EM-s (onboard & structured force)** — relativistic mass ratios and
  waste-heat inequalities; strength-capped acceleration forces 110+ AU track lengths.
- **Boundary cases** owned explicitly (eon-timescale burns, sub-0.5c gravitational flukes,
  idealized wafers), each tagged inequality [I] / probability [P] / engineering [E].

Prior-art search (adversarially verified citations): no published no-go theorem exists for
macroscopic matter at ~0.99c; closest antecedents are Semyonov (2014, 2018), Yurtsever &
Wilkinson (2018, binding only at γ~10⁸), Hoang et al. (2017, ISM damage at 0.2c), and
Guillochon & Loeb (2015, c/3 stellar ejection ceiling).
