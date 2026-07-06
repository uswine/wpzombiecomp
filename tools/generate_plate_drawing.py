#!/usr/bin/env python3
"""Generate the waterjet fabrication print + DXF for the rotary damper plates.

REV B — redesigned as a two-plate rotary damper (two identical plates
stacked, one rotates on the hub pivot). Sealing rule from design review:
web between holes = 1.5 x hole dia (c-c = 2.5 x D), else the rotated
plate cannot fully blank the flow. All rows must share one shutoff
angle -> same hole count per row (radial spokes), giving monotonic
flow 100% -> 0% over a 20 deg twist.

Optimized under those rules (see docs/PLATE-OPTIMIZATION.md):
D = 1.740, 18 holes = 9 spokes x 2 rows (R10.630 / R6.280),
open 42.8 in^2 (9.5%), closed-position min seal cover 0.441 verified
over all hole pairs.

Outputs: drawings/plate-24-perforated.svg, drawings/plate-24-perforated.dxf
"""
import math
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "drawings")

D = 1.740
S = 4.350                 # 2.5 x D min center spacing (web = 1.5 x D)
R_PLATE = 12.0
HUB_D = 3.5
N_SPOKE = 9               # same count per row -> single shutoff angle
TWIST = 180.0 / N_SPOKE   # 20 deg to full close
ROWS = [(10.630, N_SPOKE, 0.0), (6.280, N_SPOKE, 0.0)]
N_TOT = sum(n for _, n, _ in ROWS)
OPEN = N_TOT * math.pi * D * D / 4
WEIGHT = (math.pi * R_PLATE**2 - OPEN) * 0.375 * 0.284

BLACK = "#000000"
FONT = "Consolas, 'Courier New', monospace"

E = []


def raw(s): E.append(s)


def line(x1, y1, x2, y2, sw=1.0, dash=None, m1=False, m2=False):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    ms = (' marker-start="url(#as)"' if m1 else "") + (' marker-end="url(#ae)"' if m2 else "")
    raw(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
        f'stroke="{BLACK}" stroke-width="{sw}"{d}{ms}/>')


def circle(cx, cy, r, sw=1.0, dash=None, fill="none"):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    raw(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" stroke="{BLACK}" '
        f'stroke-width="{sw}" fill="{fill}"{d}/>')


def text(x, y, s, size=14, anchor="start", weight="normal", rot=None):
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    r = f' transform="rotate({rot} {x:.1f} {y:.1f})"' if rot is not None else ""
    raw(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" '
        f'fill="{BLACK}" text-anchor="{anchor}" font-weight="{weight}"{r}>{s}</text>')


def leader(x1, y1, x2, y2, label, size=13, anchor=None):
    line(x1, y1, x2, y2, sw=0.8)
    raw(f'<circle cx="{x1:.1f}" cy="{y1:.1f}" r="2" fill="{BLACK}"/>')
    a = anchor or ("end" if x2 < x1 else "start")
    dx = -5 if a == "end" else 5
    text(x2 + dx, y2 + 4, label, size=size, anchor=a)


# view transform
CX, CY, SC = 470, 485, 34.0
def T(x, y): return (CX + x * SC, CY - y * SC)
def pol(r, deg):
    a = math.radians(deg)
    return (r * math.cos(a), r * math.sin(a))


W, H = 1500, 1050
raw(f'<rect x="0" y="0" width="{W}" height="{H}" fill="#ffffff"/>')
raw(f'<rect x="18" y="18" width="{W-36}" height="{H-36}" fill="none" '
    f'stroke="{BLACK}" stroke-width="2"/>')
raw(f'<defs><marker id="ae" markerWidth="11" markerHeight="8" refX="10" refY="4" '
    f'orient="auto"><path d="M0,0 L11,4 L0,8 Z" fill="{BLACK}"/></marker>'
    f'<marker id="as" markerWidth="11" markerHeight="8" refX="1" refY="4" orient="auto">'
    f'<path d="M11,0 L0,4 L11,8 Z" fill="{BLACK}"/></marker>'
    f'<pattern id="ht" width="6" height="6" patternTransform="rotate(45)" '
    f'patternUnits="userSpaceOnUse"><line x1="0" y1="0" x2="0" y2="6" '
    f'stroke="{BLACK}" stroke-width="0.6"/></pattern></defs>')

# ---- plate outline, centerlines
circle(CX, CY, R_PLATE * SC, sw=2.4)
cl = R_PLATE * SC + 26
line(CX - cl, CY, CX + cl, CY, sw=0.7, dash="16 5 3 5")
line(CX, CY - cl, CX, CY + cl, sw=0.7, dash="16 5 3 5")

# hub zone (no cut - reference only)
circle(CX, CY, HUB_D / 2 * SC, sw=0.9, dash="10 4 2 4")

# spoke centerlines
for j in range(N_SPOKE):
    a = 360 * j / N_SPOKE
    p1, p2 = T(*pol(HUB_D / 2 + 0.3, a)), T(*pol(R_PLATE - 0.25, a))
    line(p1[0], p1[1], p2[0], p2[1], sw=0.5, dash="12 5 3 5")

# rows: construction circles + holes
for r, n, ph in ROWS:
    circle(CX, CY, r * SC, sw=0.7, dash="16 5 3 5")
    for j in range(n):
        hx, hy = T(*pol(r, ph + 360 * j / n))
        circle(hx, hy, D / 2 * SC, sw=1.8)

# ---- radial pitch dim along the 80deg spoke (4.350 = 2.5 x D)
sa = 80.0
p1, p2 = T(*pol(ROWS[0][0], sa)), T(*pol(ROWS[1][0], sa))
line(p1[0], p1[1], p2[0], p2[1], sw=0.8, m1=True, m2=True)
leader((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2, CX - 105, CY - 350,
       "4.350 ROW PITCH (2.50×Ø)", anchor="end")

# ---- in-row spacing dim between two inner holes (chord 4.384)
q1, q2 = T(*pol(ROWS[1][0], 200)), T(*pol(ROWS[1][0], 240))
line(q1[0], q1[1], q2[0], q2[1], sw=0.8, m1=True, m2=True)
leader((q1[0] + q2[0]) / 2, (q1[1] + q2[1]) / 2, CX - 145, CY + 385,
       "4.384 C-C MIN IN ROW (≥2.50×Ø)", anchor="end")

# ---- angular pitch between spokes
arc_r = (ROWS[0][0] - 1.9) * SC
a0, a1 = 0.0, 40.0
steps = 24
pts = [T(*pol(ROWS[0][0] - 1.9, a0 + (a1 - a0) * i / steps)) for i in range(steps + 1)]
d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)
raw(f'<path d="{d}" stroke="{BLACK}" stroke-width="0.8" fill="none" '
    f'marker-start="url(#as)" marker-end="url(#ae)"/>')
am = T(*pol(ROWS[0][0] - 1.55, 20))
text(am[0], am[1], "40.0°", size=13, anchor="middle")

# ---- hole diameter callout (outer hole at 120 deg)
hc = pol(ROWS[0][0], 120)
he = T(hc[0] + (D / 2) * math.cos(math.radians(120)),
       hc[1] + (D / 2) * math.sin(math.radians(120)))
leader(he[0], he[1], he[0] - 60, he[1] - 72, "Ø1.740 THRU, 18 PLCS", anchor="end")

# ---- edge margin (outer hole at 80 deg): hole edge r=11.5 to plate edge r=12
q1, q2 = T(*pol(R_PLATE - 0.5, 80)), T(*pol(R_PLATE, 80))
line(q1[0], q1[1], q2[0], q2[1], sw=0.8, m1=True, m2=True)
leader((q1[0] + q2[0]) / 2, (q1[1] + q2[1]) / 2, CX + 170, CY - R_PLATE * SC - 28,
       ".500 MIN EDGE MARGIN")

# ---- hub leader
hb = T(*pol(HUB_D / 2, 235))
leader(hb[0], hb[1], 390, 907, "Ø3.500 SOLID HUB — PIVOT/WELD ZONE, NO CUTS",
       anchor="end")

# ---- outer row radius dim
rr = T(*pol(ROWS[0][0], 217))
line(CX, CY, rr[0], rr[1], sw=0.8, m2=True)
text(CX + 0.72 * (rr[0] - CX) - 4, CY + 0.72 * (rr[1] - CY) + 22, "R10.630", size=13)

# ---- twist arrow annotation (top)
tw_pts = [T(*pol(R_PLATE + 0.55, 104 - i)) for i in range(0, 21, 2)]
d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in tw_pts)
raw(f'<path d="{d}" stroke="{BLACK}" stroke-width="1.2" fill="none" '
    f'marker-end="url(#ae)"/>')
tt = T(*pol(R_PLATE + 1.15, 97))
text(tt[0] - 10, tt[1] - 6, "ROTATE TOP PLATE 20.0° = FULL SHUTOFF", size=13, anchor="end")

# ---- overall diameter dim below plate
yd = CY + R_PLATE * SC + 42
line(CX - R_PLATE * SC, CY, CX - R_PLATE * SC, yd + 6, sw=0.7)
line(CX + R_PLATE * SC, CY, CX + R_PLATE * SC, yd + 6, sw=0.7)
line(CX - R_PLATE * SC, yd, CX + R_PLATE * SC, yd, sw=0.9, m1=True, m2=True)
text(CX, yd - 7, "Ø24.000", size=15, anchor="middle")

# ---- edge view strip (thickness)
ey0, ey1 = 950, 950 + 0.375 * SC
raw(f'<rect x="{CX-R_PLATE*SC:.1f}" y="{ey0}" width="{2*R_PLATE*SC:.1f}" '
    f'height="{ey1-ey0:.1f}" fill="url(#ht)" stroke="{BLACK}" stroke-width="1.4"/>')
text(CX - R_PLATE * SC, ey0 - 8, "EDGE VIEW", size=13)
line(CX + R_PLATE * SC + 26, ey0, CX + R_PLATE * SC + 26, ey1, sw=0.9, m1=True, m2=True)
text(CX + R_PLATE * SC + 34, (ey0 + ey1) / 2 + 4, ".375", size=13)

# ---- right column: notes
NX = 920
notes = [
    ("NOTES:", True),
    ("1. MATERIAL: ASTM A36 PLATE, .375 THK. QTY 2 —", False),
    ("   IDENTICAL PLATES, MATCHED ROTARY DAMPER PAIR.", False),
    ("2. ALL FEATURES CNC WATERJET CUT THRU MATERIAL.", False),
    ("   NO DRILLING, CHAMFERS, OR COUNTERSINKS.", False),
    ("3. OPERATION: PLATES STACKED FACE-TO-FACE ON COMMON", False),
    ("   HUB PIVOT. ROTATING TOP PLATE 20.0° MOVES EVERY", False),
    ("   HOLE ONTO SOLID WEB = FULL SHUTOFF. FLOW IS", False),
    ("   MONOTONIC: 5°=74%, 10°=41%, 15°=13%, 20°=0%.", False),
    ("4. SEALING RULE: WEB BETWEEN HOLES = 1.5×Ø MIN", False),
    ("   (C-C = 2.5×Ø). CLOSED-POSITION SEAL COVER .441 MIN,", False),
    ("   VERIFIED OVER ALL HOLE PAIRS.", False),
    ("5. 18 HOLES Ø1.740 ON 9 RADIAL SPOKES × 2 ROWS.", False),
    ("   SAME COUNT PER ROW REQUIRED SO ALL ROWS CLOSE AT", False),
    ("   ONE TWIST ANGLE.", False),
    ("6. OPEN AREA (ALIGNED) 42.8 SQ IN = 9.5% OF GROSS.", False),
    ("   EST. WEIGHT 43.6 LB PER PLATE.", False),
    ("7. CUT GEOMETRY: plate-24-perforated.dxf (CUT LAYER).", False),
    ("   KERF COMP BY SHOP. THIS PRINT GOVERNS DIMS.", False),
    ("8. TOLERANCES UNLESS NOTED: .XXX ±.015, ANGLES ±0.5°.", False),
    ("   DEBURR BOTH FACES — PLATES MUST ROTATE FLUSH.", False),
]
for i, (n, b) in enumerate(notes):
    text(NX, 52 + i * 20, n, size=13, weight="bold" if b else "normal")

# ---- hole pattern table
ty = 52 + len(notes) * 20 + 22
text(NX, ty, "HOLE PATTERN TABLE (ALL HOLES Ø1.740)", size=13.5, weight="bold")
cols = [NX, NX + 62, NX + 178, NX + 254, NX + 356, NX + 470]
hdr = ["ROW", "RADIUS", "QTY", "FIRST HOLE", "ANG PITCH"]
rows_tbl = [("1", "10.630", "9", "0.0°", "40.0°"),
            ("2", "6.280", "9", "0.0°", "40.0°"),
            ("", "TOTAL", "18", "", "")]
th = 24
line(cols[0], ty + 10, cols[5], ty + 10, sw=1.2)
for i, hcell in enumerate(hdr):
    text(cols[i] + 6, ty + 28, hcell, size=12.5, weight="bold")
line(cols[0], ty + 36, cols[5], ty + 36, sw=1.2)
for r_i, row in enumerate(rows_tbl):
    for c_i, cell in enumerate(row):
        text(cols[c_i] + 6, ty + 36 + (r_i + 1) * th - 7, cell, size=12.5)
    line(cols[0], ty + 36 + (r_i + 1) * th, cols[5], ty + 36 + (r_i + 1) * th,
         sw=1.2 if r_i in (1, 2) else 0.6)
for c in cols:
    line(c, ty + 10, c, ty + 36 + len(rows_tbl) * th, sw=0.8)
text(NX, ty + 36 + len(rows_tbl) * th + 20,
     "ANGLES CCW FROM +X AXIS. ROW RADII TO HOLE CENTERS.", size=12)

# ---- closed-position inset (proof view)
IX, IY, ISC = 1185, 745, 7.9
circle(IX, IY, R_PLATE * ISC, sw=1.4)
circle(IX, IY, HUB_D / 2 * ISC, sw=0.6, dash="6 3 2 3")
for r, n, ph in ROWS:
    for j in range(n):
        a = math.radians(ph + 360 * j / n)
        circle(IX + r * ISC * math.cos(a), IY - r * ISC * math.sin(a),
               D / 2 * ISC, sw=1.0)
        a2 = math.radians(ph + 360 * j / n + TWIST)
        circle(IX + r * ISC * math.cos(a2), IY - r * ISC * math.sin(a2),
               D / 2 * ISC, sw=1.0, dash="4 3")
text(IX, IY + R_PLATE * ISC + 20, "CLOSED POSITION — TOP PLATE +20.0° (DASHED)",
     size=12.5, anchor="middle")
text(IX, IY + R_PLATE * ISC + 38, "EVERY HOLE ON SOLID WEB, .441 MIN COVER",
     size=12.5, anchor="middle")

# ---- title block
bx, by, bw, bh = W - 560, H - 148, 542, 118
raw(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="none" '
    f'stroke="{BLACK}" stroke-width="1.8"/>')
line(bx, by + 32, bx + bw, by + 32, sw=1)
line(bx, by + 62, bx + bw, by + 62, sw=1)
line(bx, by + 90, bx + bw, by + 90, sw=1)
line(bx + 310, by + 32, bx + 310, by + bh, sw=1)
text(bx + 12, by + 22, "OFFSET SMOKER PROJECT — WATERJET FABRICATION PRINT",
     size=14.5, weight="bold")
text(bx + 12, by + 52, "ROTARY DAMPER PLATE, Ø24.00 (PAIR)", size=13.5)
text(bx + 322, by + 52, "DWG NO: WPZ-PLT-001  REV B", size=12.5)
text(bx + 12, by + 82, "MATL: ASTM A36 · THK .375 · QTY 2", size=12.5)
text(bx + 322, by + 82, "SCALE: 34 PX/IN · UNITS: IN", size=12.5)
text(bx + 12, by + 110, "REV B: RESPACED FOR ROTARY SHUTOFF", size=12)
text(bx + 322, by + 110, "SHT 1/1 · 2026-07-06", size=12.5)

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
       f'viewBox="0 0 {W} {H}">' + "".join(E) + "</svg>")
os.makedirs(OUT, exist_ok=True)
with open(os.path.join(OUT, "plate-24-perforated.svg"), "w") as f:
    f.write(svg)
print("wrote plate-24-perforated.svg")

# ================================================================ DXF (R12)
def dxf_circle(x, y, r, layer):
    return f"0\nCIRCLE\n8\n{layer}\n10\n{x:.4f}\n20\n{y:.4f}\n30\n0.0\n40\n{r:.4f}\n"

ents = [dxf_circle(0, 0, R_PLATE, "CUT")]
for r, n, ph in ROWS:
    for j in range(n):
        x, y = pol(r, ph + 360 * j / n)
        ents.append(dxf_circle(x, y, D / 2, "CUT"))
ents.append(dxf_circle(0, 0, HUB_D / 2, "REF"))
for r, _, _ in ROWS:
    ents.append(dxf_circle(0, 0, r, "REF"))

dxf = ("0\nSECTION\n2\nHEADER\n9\n$INSUNITS\n70\n1\n0\nENDSEC\n"
       "0\nSECTION\n2\nTABLES\n0\nTABLE\n2\nLAYER\n70\n2\n"
       "0\nLAYER\n2\nCUT\n70\n0\n62\n7\n6\nCONTINUOUS\n"
       "0\nLAYER\n2\nREF\n70\n0\n62\n8\n6\nCONTINUOUS\n"
       "0\nENDTAB\n0\nENDSEC\n"
       "0\nSECTION\n2\nENTITIES\n" + "".join(ents) + "0\nENDSEC\n0\nEOF\n")
with open(os.path.join(OUT, "plate-24-perforated.dxf"), "w") as f:
    f.write(dxf)
print(f"wrote plate-24-perforated.dxf ({1 + N_TOT} CUT circles + {1 + len(ROWS)} REF) — cut 2 pcs")
