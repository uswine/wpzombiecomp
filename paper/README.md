# A No-Go Theorem for the Relativistic Propulsion of Macroscopic Condensed Matter

Research paper establishing that accelerating ordinary macroscopic condensed matter
(intact solids ≥ 1 cm) to β = 0.99 is prohibited under known physics, via a proof by
cases over an exhaustive classification of physical couplings.

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

- **Case G (gravity)** — the unique heat-free coupling, kinematically capped at ~0.5c
  by the ISCO orbital speed (mass-independent), ≲0.7c with Kerr spin. Closed by dynamics.
- **Case M-environmental (interstellar medium)** — propulsion-independent keystone: at
  0.99c the ISM is a 5.7 GeV/nucleon hadron beam depositing ~2 MW/m² at mean density;
  equilibrium temperature exceeds the melting point of ordinary solids.
- **Case EM-γ (beamed sail)** — the ppm absorptivity floor cannot survive the 14× Doppler
  sweep; emissivity of sub-micron films closes the pincer; thermal–diffraction scissors
  force planetary-scale apertures.
- **Cases M-rocket / EM-s (onboard & structured force)** — relativistic mass ratios and
  waste-heat inequalities; strength-capped acceleration forces 110+ AU track lengths.
- **Boundary cases** owned explicitly (eon-timescale burns, sub-0.5c gravitational flukes,
  idealized wafers), each tagged inequality [I] / probability [P] / engineering [E].

Prior-art search (adversarially verified citations): no published no-go theorem exists for
macroscopic matter at ~0.99c; closest antecedents are Semyonov (2014, 2018), Yurtsever &
Wilkinson (2018, binding only at γ~10⁸), Hoang et al. (2017, ISM damage at 0.2c), and
Guillochon & Loeb (2015, c/3 stellar ejection ceiling).
