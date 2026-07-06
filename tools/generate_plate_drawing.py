#!/usr/bin/env python3
"""Generate the waterjet fabrication print + DXF for the 24" perforated plate.

Hole pattern was optimized numerically (see docs/DESIGN.md addendum):
sweep of hole diameters 1.005..2.20 with spacing locked at 1.333*D,
0.50 edge ligament, 3.50 solid hub. Optimum: D=2.000, 60 holes in 4
staggered concentric rows (24/18/12/6), min c-c exactly 2.666 verified
over all pairs, open area 188.5 in^2 (41.7%).

Outputs: drawings/plate-24-perforated.svg, drawings/plate-24-perforated.dxf
"""
import math
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "drawings")

D = 2.000
S = 2.666                 # 1.333 x D
R_PLATE = 12.0
HUB_D = 3.5
# row radius, hole count, first-hole angle deg (phases = max-min stagger solution)
ROWS = [(10.500, 24, 7.5), (7.864, 18, 0.0), (5.257, 12, 5.0), (2.786, 6, 20.0)]
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

# ---- plate outline, centerlines
circle(CX, CY, R_PLATE * SC, sw=2.4)
cl = R_PLATE * SC + 26
line(CX - cl, CY, CX + cl, CY, sw=0.7, dash="16 5 3 5")
line(CX, CY - cl, CX, CY + cl, sw=0.7, dash="16 5 3 5")

# hub zone (no cut - reference only)
circle(CX, CY, HUB_D / 2 * SC, sw=0.9, dash="10 4 2 4")

# rows: construction circles + holes
for r, n, ph in ROWS:
    circle(CX, CY, r * SC, sw=0.7, dash="16 5 3 5")
    for j in range(n):
        hx, hy = T(*pol(r, ph + 360 * j / n))
        circle(hx, hy, D / 2 * SC, sw=1.6)

# ---- pitch dimension between a row-1 and row-2 hole (exactly 2.666)
p1 = T(*pol(ROWS[0][0], 7.5))
p2 = T(*pol(ROWS[1][0], 0.0))
for p in (p1, p2):
    line(p[0] - 7, p[1], p[0] + 7, p[1], sw=0.8)
    line(p[0], p[1] - 7, p[0], p[1] + 7, sw=0.8)
line(p1[0], p1[1], p2[0], p2[1], sw=0.8, m1=True, m2=True)
mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
leader(mx, my, mx + 170, my + 185, "2.666 C-C MIN (1.333×Ø), ROWS STAGGERED")

# ---- hole diameter callout (row 1 hole at 52.5 deg)
hc = pol(ROWS[0][0], 52.5)
he = T(hc[0] + (D / 2) * math.cos(math.radians(52.5)),
       hc[1] + (D / 2) * math.sin(math.radians(52.5)))
leader(he[0], he[1], he[0] + 32, he[1] - 82, "Ø2.000 THRU, 60 PLCS")

# ---- edge margin (top hole at 97.5 deg, hole edge r=11.5 to plate edge r=12)
a = 97.5
q1, q2 = T(*pol(R_PLATE - 0.5, a)), T(*pol(R_PLATE, a))
line(q1[0], q1[1], q2[0], q2[1], sw=0.8, m1=True, m2=True)
leader((q1[0] + q2[0]) / 2, (q1[1] + q2[1]) / 2, CX - 290, CY - R_PLATE * SC - 28,
       ".500 MIN EDGE MARGIN", anchor="end")

# ---- hub leader
hb = T(*pol(HUB_D / 2, 235))
leader(hb[0], hb[1], 390, 907, "Ø3.500 SOLID HUB — NO CUTS", anchor="end")

# ---- outer row radius dim (rest are in table)
rr = T(*pol(ROWS[0][0], 217))
line(CX, CY, rr[0], rr[1], sw=0.8, m2=True)
text(CX + 0.78 * (rr[0] - CX) - 4, CY + 0.78 * (rr[1] - CY) + 22, "R10.500", size=13)

# ---- overall diameter dim below plate
yd = CY + R_PLATE * SC + 42
line(CX - R_PLATE * SC, CY, CX - R_PLATE * SC, yd + 6, sw=0.7)
line(CX + R_PLATE * SC, CY, CX + R_PLATE * SC, yd + 6, sw=0.7)
line(CX - R_PLATE * SC, yd, CX + R_PLATE * SC, yd, sw=0.9, m1=True, m2=True)
text(CX, yd - 7, "Ø24.000", size=15, anchor="middle")

# ---- edge view strip (thickness)
ey0, ey1 = 950, 950 + 0.375 * SC
raw(f'<defs><marker id="ae" markerWidth="11" markerHeight="8" refX="10" refY="4" '
    f'orient="auto"><path d="M0,0 L11,4 L0,8 Z" fill="{BLACK}"/></marker>'
    f'<marker id="as" markerWidth="11" markerHeight="8" refX="1" refY="4" orient="auto">'
    f'<path d="M11,0 L0,4 L11,8 Z" fill="{BLACK}"/></marker>'
    f'<pattern id="ht" width="6" height="6" patternTransform="rotate(45)" '
    f'patternUnits="userSpaceOnUse"><line x1="0" y1="0" x2="0" y2="6" '
    f'stroke="{BLACK}" stroke-width="0.6"/></pattern></defs>')
raw(f'<rect x="{CX-R_PLATE*SC:.1f}" y="{ey0}" width="{2*R_PLATE*SC:.1f}" '
    f'height="{ey1-ey0:.1f}" fill="url(#ht)" stroke="{BLACK}" stroke-width="1.4"/>')
text(CX - R_PLATE * SC, ey0 - 8, "EDGE VIEW", size=13)
line(CX + R_PLATE * SC + 26, ey0, CX + R_PLATE * SC + 26, ey1, sw=0.9, m1=True, m2=True)
text(CX + R_PLATE * SC + 34, (ey0 + ey1) / 2 + 4, ".375", size=13)

# ---- right column: notes
NX = 920
notes = [
    ("NOTES:", True),
    ("1. MATERIAL: ASTM A36 PLATE, .375 THK.", False),
    ("2. ALL FEATURES CNC WATERJET CUT THRU MATERIAL.", False),
    ("   NO DRILLING, CHAMFERS, OR COUNTERSINKS.", False),
    ("3. 60 HOLES Ø2.000 IN 4 CONCENTRIC STAGGERED ROWS", False),
    ("   PER HOLE PATTERN TABLE. PATTERN HAS 6-FOLD", False),
    ("   ROTATIONAL SYMMETRY.", False),
    ("4. MIN HOLE-TO-HOLE WEB .666. MIN EDGE MARGIN .500.", False),
    ("   CENTER HUB Ø3.500 SOLID (PIVOT/WELD ZONE).", False),
    ("5. OPEN AREA 188.5 SQ IN = 41.7% OF GROSS.", False),
    ("   EST. FINISHED WEIGHT 28.1 LB.", False),
    ("6. CUT GEOMETRY SUPPLIED AS DXF:", False),
    ("   plate-24-perforated.dxf — USE FOR CAM. KERF", False),
    ("   COMPENSATION BY SHOP. THIS PRINT GOVERNS DIMS.", False),
    ("7. TOLERANCES UNLESS NOTED: .XXX ±.015, ANGLES ±0.5°.", False),
    ("   DEBURR / TUMBLE OPTIONAL. DO NOT SCALE DRAWING.", False),
]
for i, (n, b) in enumerate(notes):
    text(NX, 58 + i * 21, n, size=13.5, weight="bold" if b else "normal")

# ---- hole pattern table
ty = 58 + len(notes) * 21 + 26
text(NX, ty, "HOLE PATTERN TABLE (ALL HOLES Ø2.000)", size=13.5, weight="bold")
cols = [NX, NX + 62, NX + 178, NX + 254, NX + 356, NX + 470]
hdr = ["ROW", "RADIUS", "QTY", "FIRST HOLE", "ANG PITCH"]
rows_tbl = [("1", "10.500", "24", "7.5°", "15.0°"),
            ("2", "7.864", "18", "0.0°", "20.0°"),
            ("3", "5.257", "12", "5.0°", "30.0°"),
            ("4", "2.786", "6", "20.0°", "60.0°"),
            ("", "TOTAL", "60", "", "")]
th = 24
line(cols[0], ty + 10, cols[5], ty + 10, sw=1.2)
for i, hcell in enumerate(hdr):
    text(cols[i] + 6, ty + 28, hcell, size=12.5, weight="bold")
line(cols[0], ty + 36, cols[5], ty + 36, sw=1.2)
for r_i, row in enumerate(rows_tbl):
    for c_i, cell in enumerate(row):
        text(cols[c_i] + 6, ty + 36 + (r_i + 1) * th - 7, cell, size=12.5)
    line(cols[0], ty + 36 + (r_i + 1) * th, cols[5], ty + 36 + (r_i + 1) * th,
         sw=1.2 if r_i in (3, 4) else 0.6)
for c in cols:
    line(c, ty + 10, c, ty + 36 + len(rows_tbl) * th, sw=0.8)
text(NX, ty + 36 + len(rows_tbl) * th + 22,
     "ANGLES CCW FROM +X AXIS. ROW RADII TO HOLE CENTERS.", size=12)

# ---- title block
bx, by, bw, bh = W - 560, H - 148, 542, 130
raw(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="none" '
    f'stroke="{BLACK}" stroke-width="1.8"/>')
line(bx, by + 34, bx + bw, by + 34, sw=1)
line(bx, by + 66, bx + bw, by + 66, sw=1)
line(bx, by + 98, bx + bw, by + 98, sw=1)
line(bx + 300, by + 34, bx + 300, by + bh, sw=1)
text(bx + 12, by + 23, "OFFSET SMOKER PROJECT — WATERJET FABRICATION PRINT",
     size=15, weight="bold")
text(bx + 12, by + 55, "PERFORATED AIRFLOW PLATE, Ø24.00", size=14)
text(bx + 312, by + 55, "DWG NO: WPZ-PLT-001  REV A", size=13)
text(bx + 12, by + 87, "MATL: ASTM A36 · THK .375 · QTY 1", size=13)
text(bx + 312, by + 87, "SCALE: 34 PX/IN · UNITS: IN", size=13)
text(bx + 12, by + 120, "FINISH: AS-CUT (WATERJET)", size=13)
text(bx + 312, by + 120, "SHT 1/1 · 2026-07-06", size=13)

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
ents.append(dxf_circle(0, 0, HUB_D / 2, "REF"))       # hub zone, reference only
for r, _, _ in ROWS:
    ents.append(dxf_circle(0, 0, r, "REF"))           # row construction circles

dxf = ("0\nSECTION\n2\nHEADER\n9\n$INSUNITS\n70\n1\n0\nENDSEC\n"
       "0\nSECTION\n2\nTABLES\n0\nTABLE\n2\nLAYER\n70\n2\n"
       "0\nLAYER\n2\nCUT\n70\n0\n62\n7\n6\nCONTINUOUS\n"
       "0\nLAYER\n2\nREF\n70\n0\n62\n8\n6\nCONTINUOUS\n"
       "0\nENDTAB\n0\nENDSEC\n"
       "0\nSECTION\n2\nENTITIES\n" + "".join(ents) + "0\nENDSEC\n0\nEOF\n")
with open(os.path.join(OUT, "plate-24-perforated.dxf"), "w") as f:
    f.write(dxf)
print(f"wrote plate-24-perforated.dxf ({1 + N_TOT} CUT circles + {1 + len(ROWS)} REF)")
