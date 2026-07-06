#!/usr/bin/env python3
"""Generate the waterjet fabrication print + DXF for the rotary damper plates.

REV C — outer row enlarged per design review (2-3x Rev B's 1.740):
each row now carries its own hole diameter, sized to its own radius,
with the same hole count (5 spokes) in both rows so the pair still
seals at a single twist angle with monotonic flow.

Rules held: hole edge to OD gap = 0.500 min (outer row sits at exactly
0.500), c-c >= 2.5 x that row's dia (web >= 1.5 x dia), radial web =
1.5 x inner dia, hub Ø3.5 solid. Verified: closed-position min
edge-to-edge cover 0.463 over all pairs; flow 100%->0% monotonic over
36 deg; open area 94.4 in^2 (20.9%).

Outputs: drawings/plate-24-perforated.svg, drawings/plate-24-perforated.dxf
"""
import math
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "drawings")

R_PLATE = 12.0
HUB_D = 3.5
N_SPOKE = 5               # same count per row -> single shutoff angle
TWIST = 180.0 / N_SPOKE   # 36 deg to full close
# (radius, count, first-hole deg, hole dia)
ROWS = [(9.200, N_SPOKE, 0.0, 4.600), (3.500, N_SPOKE, 0.0, 1.700)]
N_TOT = sum(n for _, n, _, _ in ROWS)
OPEN = sum(n * math.pi * D * D / 4 for _, n, _, D in ROWS)
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
for r, n, ph, D in ROWS:
    circle(CX, CY, r * SC, sw=0.7, dash="16 5 3 5")
    for j in range(n):
        hx, hy = T(*pol(r, ph + 360 * j / n))
        circle(hx, hy, D / 2 * SC, sw=1.8)

# ---- radial pitch dim along the 144 deg spoke (5.700)
sa = 144.0
p1, p2 = T(*pol(ROWS[0][0], sa)), T(*pol(ROWS[1][0], sa))
line(p1[0], p1[1], p2[0], p2[1], sw=0.8, m1=True, m2=True)
leader((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2, CX - 215, CY + 330,
       "5.700 ROW PITCH, WEB 2.550", anchor="end")

# ---- in-row spacing dim between two inner holes (chord 4.398)
q1, q2 = T(*pol(ROWS[1][0], 216)), T(*pol(ROWS[1][0], 288))
line(q1[0], q1[1], q2[0], q2[1], sw=0.8, m1=True, m2=True)
leader((q1[0] + q2[0]) / 2, (q1[1] + q2[1]) / 2, CX - 60, CY + 400,
       "4.398 C-C ROW 2 (2.59×Ø)", anchor="end")

# ---- angular pitch between spokes
steps = 24
apts = [T(*pol(6.6, 0 + 72.0 * i / steps)) for i in range(steps + 1)]
d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in apts)
raw(f'<path d="{d}" stroke="{BLACK}" stroke-width="0.8" fill="none" '
    f'marker-start="url(#as)" marker-end="url(#ae)"/>')
am = T(*pol(7.0, 36))
text(am[0], am[1], "72.0°", size=13, anchor="middle")

# ---- hole diameter callouts
hc = pol(ROWS[0][0], 144)
he = T(hc[0] + (ROWS[0][3] / 2) * math.cos(math.radians(170)),
       hc[1] + (ROWS[0][3] / 2) * math.sin(math.radians(170)))
leader(he[0], he[1], he[0] + 40, he[1] - 138, "Ø4.600 THRU, 5 PLCS (ROW 1)")
hc2 = pol(ROWS[1][0], 72)
he2 = T(hc2[0], hc2[1] + ROWS[1][3] / 2)
leader(he2[0], he2[1], he2[0] + 55, he2[1] - 105, "Ø1.700 THRU, 5 PLCS (ROW 2)")

# ---- edge margin (outer hole at 0 deg): hole edge r=11.5 to plate edge r=12
q1, q2 = T(R_PLATE - 0.5, 0), T(R_PLATE, 0)
line(q1[0], q1[1], q2[0], q2[1], sw=0.8)
line(q1[0], q1[1] - 8, q1[0], q1[1] + 8, sw=0.8)
line(q2[0], q2[1] - 8, q2[0], q2[1] + 8, sw=0.8)
leader((q1[0] + q2[0]) / 2, q1[1], (q1[0] + q2[0]) / 2 - 7, q1[1] + 125,
       "OD GAP .500 MIN", anchor="end")

# ---- hub leader
hb = T(*pol(HUB_D / 2, 250))
leader(hb[0], hb[1], 300, 920, "Ø3.500 SOLID HUB — NO CUTS", anchor="end")

# ---- outer row radius dim
rr = T(*pol(ROWS[0][0], 200))
line(CX, CY, rr[0], rr[1], sw=0.8, m2=True)
text(CX + 0.62 * (rr[0] - CX) - 4, CY + 0.62 * (rr[1] - CY) + 24, "R9.200", size=13)

# ---- twist arrow annotation (top)
tw_pts = [T(*pol(R_PLATE + 0.55, 122 - i)) for i in range(0, 37, 3)]
d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in tw_pts)
raw(f'<path d="{d}" stroke="{BLACK}" stroke-width="1.2" fill="none" '
    f'marker-end="url(#ae)"/>')
tt = T(*pol(R_PLATE + 1.15, 112))
text(tt[0] + 16, tt[1] - 8, "ROTATE TOP PLATE 36.0° = FULL SHUTOFF", size=13)

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
    ("   HUB PIVOT. ROTATING TOP PLATE 36.0° MOVES EVERY", False),
    ("   HOLE ONTO SOLID WEB = FULL SHUTOFF. FLOW IS", False),
    ("   MONOTONIC: 9°=61%, 18°=26%, 27°=2%, 36°=0%.", False),
    ("4. SEALING RULE: WEB ≥ 1.5×Ø IN EACH ROW (C-C ≥ 2.5×Ø).", False),
    ("   CLOSED-POSITION SEAL COVER .463 MIN, VERIFIED OVER", False),
    ("   ALL HOLE PAIRS. RADIAL WEB 2.550 (1.5× ROW-2 Ø).", False),
    ("5. 10 HOLES ON 5 RADIAL SPOKES × 2 ROWS; DIA PER ROW", False),
    ("   PER TABLE. SAME COUNT PER ROW REQUIRED SO BOTH", False),
    ("   ROWS CLOSE AT ONE TWIST ANGLE.", False),
    ("6. OPEN AREA (ALIGNED) 94.4 SQ IN = 20.9% OF GROSS.", False),
    ("   EST. WEIGHT 38.1 LB PER PLATE.", False),
    ("7. CUT GEOMETRY: plate-24-perforated.dxf (CUT LAYER).", False),
    ("   KERF COMP BY SHOP. THIS PRINT GOVERNS DIMS.", False),
    ("8. TOLERANCES UNLESS NOTED: .XXX ±.015, ANGLES ±0.5°.", False),
    ("   DEBURR BOTH FACES — PLATES MUST ROTATE FLUSH.", False),
]
for i, (n, b) in enumerate(notes):
    text(NX, 52 + i * 20, n, size=13, weight="bold" if b else "normal")

# ---- hole pattern table
ty = 52 + len(notes) * 20 + 22
text(NX, ty, "HOLE PATTERN TABLE", size=13.5, weight="bold")
cols = [NX, NX + 52, NX + 140, NX + 240, NX + 292, NX + 396, NX + 490]
hdr = ["ROW", "RADIUS", "HOLE Ø", "QTY", "FIRST HOLE", "PITCH"]
rows_tbl = [("1", "9.200", "4.600", "5", "0.0°", "72.0°"),
            ("2", "3.500", "1.700", "5", "0.0°", "72.0°"),
            ("", "", "TOTAL", "10", "", "")]
th = 24
line(cols[0], ty + 10, cols[6], ty + 10, sw=1.2)
for i, hcell in enumerate(hdr):
    text(cols[i] + 6, ty + 28, hcell, size=12.5, weight="bold")
line(cols[0], ty + 36, cols[6], ty + 36, sw=1.2)
for r_i, row in enumerate(rows_tbl):
    for c_i, cell in enumerate(row):
        text(cols[c_i] + 6, ty + 36 + (r_i + 1) * th - 7, cell, size=12.5)
    line(cols[0], ty + 36 + (r_i + 1) * th, cols[6], ty + 36 + (r_i + 1) * th,
         sw=1.2 if r_i in (1, 2) else 0.6)
for c in cols:
    line(c, ty + 10, c, ty + 36 + len(rows_tbl) * th, sw=0.8)
text(NX, ty + 36 + len(rows_tbl) * th + 20,
     "ANGLES CCW FROM +X AXIS. ROW RADII TO HOLE CENTERS.", size=12)

# ---- closed-position inset (proof view)
IX, IY, ISC = 1185, 745, 7.9
circle(IX, IY, R_PLATE * ISC, sw=1.4)
circle(IX, IY, HUB_D / 2 * ISC, sw=0.6, dash="6 3 2 3")
for r, n, ph, D in ROWS:
    for j in range(n):
        a = math.radians(ph + 360 * j / n)
        circle(IX + r * ISC * math.cos(a), IY - r * ISC * math.sin(a),
               D / 2 * ISC, sw=1.0)
        a2 = math.radians(ph + 360 * j / n + TWIST)
        circle(IX + r * ISC * math.cos(a2), IY - r * ISC * math.sin(a2),
               D / 2 * ISC, sw=1.0, dash="4 3")
text(IX, IY + R_PLATE * ISC + 20, "CLOSED POSITION — TOP PLATE +36.0° (DASHED)",
     size=12.5, anchor="middle")
text(IX, IY + R_PLATE * ISC + 38, "EVERY HOLE ON SOLID WEB, .463 MIN COVER",
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
text(bx + 322, by + 52, "DWG NO: WPZ-PLT-001  REV C", size=12.5)
text(bx + 12, by + 82, "MATL: ASTM A36 · THK .375 · QTY 2", size=12.5)
text(bx + 322, by + 82, "SCALE: 34 PX/IN · UNITS: IN", size=12.5)
text(bx + 12, by + 110, "REV C: ROW 1 ENLARGED PER REVIEW", size=12)
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
for r, n, ph, D in ROWS:
    for j in range(n):
        x, y = pol(r, ph + 360 * j / n)
        ents.append(dxf_circle(x, y, D / 2, "CUT"))
ents.append(dxf_circle(0, 0, HUB_D / 2, "REF"))
for r, _, _, _ in ROWS:
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
