#!/usr/bin/env python3
"""24" pizza cooking plate for the vertical offset smoker — WPZ-PIZ-001 REV A.

One monolithic Ø24.000 major-OD x 1.000 thick A36 plate, relieved to a
Ø23.000 minor OD between eight equally spaced 1.000-wide weld islands.
Perimeter openings are full-thickness through cuts, 0.500 radial depth,
R.250 internal corners. No secondary ring / shelf / step.

Governing derived geometry (exact):
  island half-angle  w = deg(0.5/12)          = 2.3873 deg  (1.000 arc at OD)
  fillet offset      d = asin(.25/11.75)      = 1.2192 deg
  sidewall tangent   rt = sqrt(11.75^2-.25^2) = 11.74734
  opening span       45 - 2w = 40.225 deg -> 8.425 arc at OD

Outputs: drawings/pizza-plate-24.svg (print), .dxf (one closed LWPOLYLINE
cut contour, true arcs, + REF layer), .stl (1.000 extrusion of the same
profile). STEP: import the DXF into any CAD and extrude 1.000.
"""
import math
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "drawings")

R_MAJ, R_MIN, THK, FIL, N_ISL = 12.0, 11.5, 1.000, 0.250, 8
W_HALF = math.degrees(0.5 / R_MAJ)                 # island half-angle
DELTA = math.degrees(math.asin(FIL / (R_MIN + FIL)))
RT = math.sqrt((R_MIN + FIL) ** 2 - FIL ** 2)      # fillet tangency on sidewall
PITCH = 360.0 / N_ISL


def pol(r, deg):
    a = math.radians(deg)
    return (r * math.cos(a), r * math.sin(a))


# ---------------------------------------------------------------- contour
# CCW segment list: ('line', p0, p1) / ('arc', center, radius, a0_deg, a1_deg)
# arcs traverse CCW from a0 to a1 about center unless a1 < a0 (then CW).
def build_segments():
    segs = []
    for k in range(N_ISL):
        th = k * PITCH
        segs.append(("arc", (0, 0), R_MAJ, th - W_HALF, th + W_HALF))
        segs.append(("line", pol(R_MAJ, th + W_HALF), pol(RT, th + W_HALF)))
        segs.append(("arc", pol(R_MIN + FIL, th + W_HALF + DELTA), FIL,
                     None, None, pol(RT, th + W_HALF), pol(R_MIN, th + W_HALF + DELTA)))
        segs.append(("arc", (0, 0), R_MIN, th + W_HALF + DELTA,
                     th + PITCH - W_HALF - DELTA))
        segs.append(("arc", pol(R_MIN + FIL, th + PITCH - W_HALF - DELTA), FIL,
                     None, None, pol(R_MIN, th + PITCH - W_HALF - DELTA),
                     pol(RT, th + PITCH - W_HALF)))
        segs.append(("line", pol(RT, th + PITCH - W_HALF),
                     pol(R_MAJ, th + PITCH - W_HALF)))
    return segs


def seg_endpoints(s):
    if s[0] == "line":
        return s[1], s[2]
    if s[2] in (R_MAJ, R_MIN):
        return pol(s[2], s[3]), pol(s[2], s[4])
    return s[5], s[6]


def seg_sweep(s):
    """signed sweep (rad, CCW+) of an arc segment"""
    c = s[1]
    p0, p1 = seg_endpoints(s)
    a0 = math.atan2(p0[1] - c[1], p0[0] - c[0])
    a1 = math.atan2(p1[1] - c[1], p1[0] - c[0])
    sw = a1 - a0
    while sw <= -math.pi: sw += 2 * math.pi
    while sw > math.pi: sw -= 2 * math.pi
    return sw


def tessellate(tol=0.005):
    pts = []
    for s in build_segments():
        p0, p1 = seg_endpoints(s)
        if s[0] == "line":
            pts.append(p0)
        else:
            c, r = s[1], s[2]
            sw = seg_sweep(s)
            n = max(2, int(abs(sw) / (2 * math.sqrt(2 * tol / r)) ) + 1)
            a0 = math.atan2(p0[1] - c[1], p0[0] - c[0])
            for i in range(n):
                a = a0 + sw * i / n
                pts.append((c[0] + r * math.cos(a), c[1] + r * math.sin(a)))
    return pts


def verify():
    segs = build_segments()
    # closure: each segment's end == next segment's start
    worst = 0.0
    for i, s in enumerate(segs):
        p1 = seg_endpoints(s)[1]
        p0n = seg_endpoints(segs[(i + 1) % len(segs)])[0]
        worst = max(worst, math.hypot(p1[0] - p0n[0], p1[1] - p0n[1]))
    # tangency: fillet arcs meet neighbors smoothly (radius checks implicit)
    pts = tessellate()
    rr = [math.hypot(x, y) for x, y in pts]
    area = 0.0
    for i in range(len(pts)):
        x0, y0 = pts[i]; x1, y1 = pts[(i + 1) % len(pts)]
        area += x0 * y1 - x1 * y0
    area /= 2
    print(f"contour: {len(segs)} segments, closure error {worst:.2e} in, "
          f"r range [{min(rr):.4f},{max(rr):.4f}], area {area:.2f} in2, "
          f"weight {area*THK*0.284:.1f} lb")
    return area


# ---------------------------------------------------------------- DXF
def write_dxf():
    verts = []          # (x, y, bulge) — bulge applies to segment to next vertex
    for s in build_segments():
        p0, _ = seg_endpoints(s)
        b = 0.0 if s[0] == "line" else math.tan(seg_sweep(s) / 4)
        verts.append((p0[0], p0[1], b))
    e = ["0\nLWPOLYLINE\n8\nCUT\n90\n%d\n70\n1\n" % len(verts)]
    for x, y, b in verts:
        e.append(f"10\n{x:.6f}\n20\n{y:.6f}\n42\n{b:.8f}\n")
    ref = ""
    for r in (R_MAJ, R_MIN):
        ref += f"0\nCIRCLE\n8\nREF\n10\n0\n20\n0\n30\n0\n40\n{r:.4f}\n"
    dxf = ("0\nSECTION\n2\nHEADER\n9\n$INSUNITS\n70\n1\n0\nENDSEC\n"
           "0\nSECTION\n2\nTABLES\n0\nTABLE\n2\nLAYER\n70\n2\n"
           "0\nLAYER\n2\nCUT\n70\n0\n62\n7\n6\nCONTINUOUS\n"
           "0\nLAYER\n2\nREF\n70\n0\n62\n8\n6\nCONTINUOUS\n"
           "0\nENDTAB\n0\nENDSEC\n0\nSECTION\n2\nENTITIES\n"
           + "".join(e) + ref + "0\nENDSEC\n0\nEOF\n")
    with open(os.path.join(OUT, "pizza-plate-24.dxf"), "w") as f:
        f.write(dxf)
    print(f"wrote pizza-plate-24.dxf (1 closed contour, {len(verts)} vertices, true arcs)")


# ---------------------------------------------------------------- STL
def write_stl():
    poly = tessellate(0.01)
    n = len(poly)

    def is_ear(i, idx):
        a, b, c = poly[idx[i - 1]], poly[idx[i]], poly[idx[(i + 1) % len(idx)]]
        cross = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
        if cross <= 0:
            return False
        for j in idx:
            if j in (idx[i - 1], idx[i], idx[(i + 1) % len(idx)]):
                continue
            p = poly[j]
            d1 = (b[0]-a[0])*(p[1]-a[1])-(b[1]-a[1])*(p[0]-a[0])
            d2 = (c[0]-b[0])*(p[1]-b[1])-(c[1]-b[1])*(p[0]-b[0])
            d3 = (a[0]-c[0])*(p[1]-c[1])-(a[1]-c[1])*(p[0]-c[0])
            if d1 > 0 and d2 > 0 and d3 > 0:
                return False
        return True

    idx = list(range(n))
    tris = []
    guard = 0
    while len(idx) > 3 and guard < n * n:
        for i in range(len(idx)):
            guard += 1
            if is_ear(i, idx):
                tris.append((idx[i - 1], idx[i], idx[(i + 1) % len(idx)]))
                del idx[i]
                break
    tris.append(tuple(idx))

    def tri(f, p0, p1, p2):
        ux, uy, uz = p1[0]-p0[0], p1[1]-p0[1], p1[2]-p0[2]
        vx, vy, vz = p2[0]-p0[0], p2[1]-p0[1], p2[2]-p0[2]
        nx, ny, nz = uy*vz-uz*vy, uz*vx-ux*vz, ux*vy-uy*vx
        l = math.sqrt(nx*nx+ny*ny+nz*nz) or 1
        f.write(f"facet normal {nx/l:.6e} {ny/l:.6e} {nz/l:.6e}\n outer loop\n")
        for p in (p0, p1, p2):
            f.write(f"  vertex {p[0]:.6e} {p[1]:.6e} {p[2]:.6e}\n")
        f.write(" endloop\nendfacet\n")

    path = os.path.join(OUT, "pizza-plate-24.stl")
    vol = 0.0
    with open(path, "w") as f:
        f.write("solid pizza_plate_24\n")
        for a, b, c in tris:
            pa, pb, pc = poly[a], poly[b], poly[c]
            tri(f, (pa[0], pa[1], THK), (pb[0], pb[1], THK), (pc[0], pc[1], THK))
            tri(f, (pa[0], pa[1], 0), (pc[0], pc[1], 0), (pb[0], pb[1], 0))
        for i in range(n):
            p0, p1 = poly[i], poly[(i + 1) % n]
            tri(f, (p0[0], p0[1], 0), (p1[0], p1[1], 0), (p1[0], p1[1], THK))
            tri(f, (p0[0], p0[1], 0), (p1[0], p1[1], THK), (p0[0], p0[1], THK))
        f.write("endsolid pizza_plate_24\n")
    # volume check from cap area
    area = 0.0
    for i in range(n):
        x0, y0 = poly[i]; x1, y1 = poly[(i + 1) % n]
        area += x0 * y1 - x1 * y0
    print(f"wrote pizza-plate-24.stl ({2*len(tris)+2*n} facets, "
          f"volume ~{abs(area)/2*THK:.1f} in3)")


# ---------------------------------------------------------------- SVG sheet
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
def poly(pts, sw=1.0, dash=None, fill="none", close=False):
    d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts) + (" Z" if close else "")
    dd = f' stroke-dasharray="{dash}"' if dash else ""
    raw(f'<path d="{d}" stroke="{BLACK}" stroke-width="{sw}" fill="{fill}"{dd}/>')
def text(x, y, s, size=13, anchor="start", weight="normal", rot=None):
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    r = f' transform="rotate({rot} {x:.1f} {y:.1f})"' if rot is not None else ""
    raw(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" '
        f'fill="{BLACK}" text-anchor="{anchor}" font-weight="{weight}"{r}>{s}</text>')
def leader(x1, y1, x2, y2, label, size=12, anchor=None):
    line(x1, y1, x2, y2, sw=0.8)
    raw(f'<circle cx="{x1:.1f}" cy="{y1:.1f}" r="2" fill="{BLACK}"/>')
    a = anchor or ("end" if x2 < x1 else "start")
    text(x2 + (-5 if a == "end" else 5), y2 + 4, label, size=size, anchor=a)


def sheet():
    W, H = 1500, 1050
    raw(f'<rect width="{W}" height="{H}" fill="#fff"/>')
    raw(f'<rect x="16" y="16" width="{W-32}" height="{H-32}" fill="none" '
        f'stroke="{BLACK}" stroke-width="2.2"/>')
    raw(f'<defs><marker id="ae" markerWidth="11" markerHeight="8" refX="10" refY="4" '
        f'orient="auto"><path d="M0,0 L11,4 L0,8 Z" fill="{BLACK}"/></marker>'
        f'<marker id="as" markerWidth="11" markerHeight="8" refX="1" refY="4" orient="auto">'
        f'<path d="M11,0 L0,4 L11,8 Z" fill="{BLACK}"/></marker>'
        f'<pattern id="ht" width="6" height="6" patternTransform="rotate(45)" '
        f'patternUnits="userSpaceOnUse"><line x1="0" y1="0" x2="0" y2="6" '
        f'stroke="{BLACK}" stroke-width="0.55"/></pattern></defs>')
    text(36, 48, '24" PIZZA COOKING PLATE — VERTICAL OFFSET SMOKER', size=24, weight="bold")
    line(36, 60, 900, 60, sw=1.6)

    # ============ 1) TOP VIEW =================================
    cx, cy, s = 300, 350, 18.0
    def TT(p): return (cx + p[0] * s, cy - p[1] * s)
    text(cx, 98, "1) TOP VIEW (PLAN) — GOVERNING", size=15, anchor="middle", weight="bold")
    pts = [TT(p) for p in tessellate(0.003)]
    poly(pts, sw=2.2, close=True)
    circle(cx, cy, R_MIN * s, sw=0.6, dash="10 5 2 5")
    cl = R_MAJ * s + 20
    line(cx - cl, cy, cx + cl, cy, sw=0.6, dash="14 5 3 5")
    line(cx, cy - cl, cx, cy + cl, sw=0.6, dash="14 5 3 5")
    # section line A-A on the horizontal centerline
    text(cx - cl - 4, cy + 4, "A", size=13, anchor="end", weight="bold")
    text(cx + cl + 4, cy + 4, "A", size=13, weight="bold")
    # major OD dim (diagonal at 45)
    p1, p2 = TT(pol(R_MAJ, 225)), TT(pol(R_MAJ, 45))
    line(p1[0], p1[1], p2[0], p2[1], sw=0.8, m1=True, m2=True)
    text(cx - 8, cy - 40, "Ø24.000", size=13, anchor="end")
    text(cx - 8, cy - 24, "MAJOR OD", size=11, anchor="end")
    # minor OD leader (opening root at 22.5 deg)
    q = TT(pol(R_MIN, 157.5))
    leader(q[0], q[1], 60, 545, "Ø23.000 MINOR OD", anchor="start")
    # island width + depth + rad + 8x callouts
    e1 = TT(pol(R_MAJ, 270))
    leader(e1[0], e1[1], 430, 598, '1.000 WELD ISLAND WIDTH (TYP)', anchor="start")
    e2 = TT(pol((R_MAJ + R_MIN) / 2, 67.5))
    leader(e2[0], e2[1], e2[0] + 170, e2[1] - 52, "0.500 RADIAL OPENING DEPTH (TYP)")
    e3 = TT(pol(R_MIN, 45 + W_HALF + DELTA))
    leader(e3[0], e3[1], e3[0] + 205, e3[1] + 20, "R.250 TYP INTERNAL CORNERS")
    e4 = TT(pol(R_MAJ - 0.2, 202.5))
    leader(e4[0], e4[1], 150, 590, "8X WELD ISLANDS EQ SP (45° TYP)")
    # 45 deg angular dim between island centerlines
    arcpts = [TT(pol(R_MAJ - 2.2, a)) for a in range(0, 46, 3)]
    d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in arcpts)
    raw(f'<path d="{d}" stroke="{BLACK}" stroke-width="0.8" fill="none" '
        f'marker-start="url(#as)" marker-end="url(#ae)"/>')
    am = TT(pol(R_MAJ - 1.55, 22.5))
    text(am[0] + 2, am[1] + 4, "45.000°", size=12)

    # ============ 2) SIDE VIEW / SECTION ======================
    sx0, sx1, sy0 = 800, 1380, 120
    ss = (sx1 - sx0) / 24.0
    sy1 = sy0 + THK * ss
    text((sx0 + sx1) / 2, 100, "2) SECTION A-A (THRU ISLAND Ø)", size=15,
         anchor="middle", weight="bold")
    raw(f'<rect x="{sx0}" y="{sy0}" width="{sx1-sx0}" height="{sy1-sy0:.1f}" '
        f'fill="url(#ht)" stroke="{BLACK}" stroke-width="1.6"/>')
    for r in (R_MIN, -R_MIN):
        xr = (sx0 + sx1) / 2 + r * ss
        line(xr, sy0 - 8, xr, sy1 + 8, sw=0.7, dash="4 3")
    line(sx1 + 22, sy0, sx1 + 22, sy1, sw=0.8, m1=True, m2=True)
    text(sx1 + 30, (sy0 + sy1) / 2 + 4, "1.000", size=12)
    text(sx0, sy1 + 22, "ONE SOLID 1.000 THK PLATE — OPENINGS ARE FULL-THICKNESS THRU CUTS", size=11.5)
    text(sx0, sy1 + 38, "NO RING / SHELF / LEDGE / STEP BENEATH OPENINGS. DASHED: Ø23.000 OPENING ROOT REF.", size=11.5)

    # ============ 3) ISOMETRIC ================================
    icx, icy, isc = 1085, 370, 12.5
    text(icx, 218, "3) ISOMETRIC VIEW (1.000 EXTRUSION OF TOP PROFILE)", size=15,
         anchor="middle", weight="bold")
    c30, s30 = math.cos(math.radians(30)), 0.5
    def ISO(x, y, z):
        return (icx + (x - y) * c30 * isc, icy - (z + (x + y) * s30) * isc + 60)
    prof = tessellate(0.008)
    bot = [ISO(x, y, 0) for x, y in prof]
    top = [ISO(x, y, THK) for x, y in prof]
    poly(bot, sw=0.7, close=True)
    # verticals at feature corners (island corners + fillet tangencies)
    for sgm in build_segments():
        for p in seg_endpoints(sgm):
            a, b = ISO(p[0], p[1], 0), ISO(p[0], p[1], THK)
            line(a[0], a[1], b[0], b[1], sw=0.55)
    poly(top, sw=1.8, close=True)

    # ============ 4) DETAIL A — TRUE-CURVATURE PLAN ZOOM ======
    # detail bubble on top view around the 0-deg island
    bb = TT(pol((R_MAJ + R_MIN) / 2, 0))
    circle(bb[0], bb[1], 30, sw=1.0, dash="6 4")
    text(bb[0] + 34, bb[1] - 24, "B", size=14, weight="bold")

    text(60, 618, "4) DETAIL B — PLAN, TRUE CURVATURE", size=14, weight="bold")
    dcx, dby, dS = 250, 792, 62.0    # radial dir drawn UP; baseline ~R11.35
    def DD(r, adeg):                 # plate polar -> detail screen (island at top)
        x, y = pol(r, adeg)
        return (dcx + y * -1 * -dS * 0 + (x * 0) + ( -pol(r, adeg)[1]) * -dS, 0)
    def DDp(r, adeg):
        x, y = pol(r, adeg)          # rotate +90 so 0-deg radial points up
        xr, yr = -y, x
        return (dcx + xr * dS, dby - (yr - 11.35) * dS)
    # local outline: root left -> fillet -> wall -> island arc -> wall -> fillet -> root right
    seq = []
    for a in [x / 3 for x in range(-40, -int((W_HALF + DELTA) * 3) - 1, 1)] + [-(W_HALF + DELTA)]:
        seq.append((R_MIN, a))
    fc = pol(R_MIN + FIL, -(W_HALF + DELTA))
    a0 = math.atan2(pol(R_MIN, -(W_HALF + DELTA))[1] - fc[1], pol(R_MIN, -(W_HALF + DELTA))[0] - fc[0])
    a1 = math.atan2(pol(RT, -W_HALF)[1] - fc[1], pol(RT, -W_HALF)[0] - fc[0])
    sw_ = a1 - a0
    while sw_ <= -math.pi: sw_ += 2 * math.pi
    while sw_ > math.pi: sw_ -= 2 * math.pi
    fill_l = [(math.hypot(fc[0] + FIL * math.cos(a0 + sw_ * t / 8) - 0, fc[1] + FIL * math.sin(a0 + sw_ * t / 8)),
               math.degrees(math.atan2(fc[1] + FIL * math.sin(a0 + sw_ * t / 8), fc[0] + FIL * math.cos(a0 + sw_ * t / 8))))
              for t in range(9)]
    seq += fill_l
    seq += [(RT, -W_HALF), (R_MAJ, -W_HALF)]
    for a in [x / 3 for x in range(-int(W_HALF * 3), int(W_HALF * 3) + 1)]:
        seq.append((R_MAJ, a))
    seq += [(R_MAJ, W_HALF), (RT, W_HALF)]
    seq += [(r, -a) for r, a in reversed(fill_l)]
    for a in [x / 3 for x in range(int((W_HALF + DELTA) * 3) + 1, 41)]:
        seq.append((R_MIN, a))
    poly([DDp(r, a) for r, a in seq], sw=2.2)
    # reference arcs
    for rr_ in (R_MAJ, R_MIN):
        poly([DDp(rr_, a) for a in [x / 2 for x in range(-27, 28)]], sw=0.6, dash="8 5 2 5")
    p24 = DDp(R_MAJ, 10.5)
    text(p24[0] - 8, p24[1] - 8, "Ø24.000 REF", size=11, anchor="end")
    p23 = DDp(R_MIN, -10.5)
    text(p23[0] + 10, p23[1] + 18, "Ø23.000 REF", size=11)
    # dims: island width at OD
    c1, c2 = DDp(R_MAJ, -W_HALF), DDp(R_MAJ, W_HALF)
    ytop = min(c1[1], c2[1]) - 30
    line(c1[0], c1[1] - 4, c1[0], ytop - 6, sw=0.6)
    line(c2[0], c2[1] - 4, c2[0], ytop - 6, sw=0.6)
    line(c1[0], ytop, c2[0], ytop, sw=0.8, m1=True, m2=True)
    text((c1[0] + c2[0]) / 2, ytop - 6, "1.000", size=12, anchor="middle")
    # radial depth at +9 deg
    d1, d2 = DDp(R_MIN, 9), DDp(R_MAJ, 9)
    line(d1[0], d1[1], d2[0], d2[1], sw=0.8, m1=True, m2=True)
    text(d2[0] + 6, (d1[1] + d2[1]) / 2 + 4, ".500", size=12)
    # fillet leader
    fpt = DDp(R_MIN + 0.08, -(W_HALF + DELTA * 0.6))
    leader(fpt[0], fpt[1], fpt[0] + 78, fpt[1] - 34, "R.250 TYP")
    # region labels — the key clarification
    text(66, 668, "OPEN — OUTSIDE PLATE EDGE", size=11.5)
    text(dcx, dby + 34, "SOLID PLATE — FLAT BOTH FACES, CONSTANT 1.000 THK", size=11.5, anchor="middle")
    text(dcx, dby + 52, "ISLANDS ARE IN-PLANE OUTLINE FEATURES — NOT RAISED", size=11.5, anchor="middle")
    # radial axis arrow
    ax0, ax1 = DDp(R_MIN - 0.35, -13.4), DDp(R_MAJ + 0.35, -13.4)
    raw(f'<line x1="{ax0[0]+34:.1f}" y1="{ax0[1]:.1f}" x2="{ax1[0]+34:.1f}" y2="{ax1[1]:.1f}" '
        f'stroke="{BLACK}" stroke-width="0.9" marker-end="url(#ae)"/>')
    text(ax1[0] + 34, ax1[1] - 8, "RADIAL", size=10.5, anchor="middle")

    # ============ 5) EDGE DEVELOPMENT (PLAN) + EDGE ELEVATION =
    ex = 838
    text(ex, 618, "5) EDGE DEVELOPMENT — UNWRAPPED (NTS)", size=14, weight="bold")
    text(ex, 638, "TOP: PLAN (VERTICAL AXIS = RADIAL, NOT HEIGHT) · BOTTOM: EDGE ELEVATION", size=11)
    pitch, iw, th_ = 158, 24, 30
    yb2 = ex and 712
    xs = ex
    path = f'M {xs:.1f} {yb2:.1f} '
    for i2 in range(3):
        x0 = xs + i2 * pitch + (pitch - iw) / 2
        path += (f'L {x0-8:.1f} {yb2:.1f} A 8 8 0 0 0 {x0:.1f} {yb2-8:.1f} '
                 f'L {x0:.1f} {yb2-th_:.1f} L {x0+iw:.1f} {yb2-th_:.1f} '
                 f'L {x0+iw:.1f} {yb2-8:.1f} A 8 8 0 0 0 {x0+iw+8:.1f} {yb2:.1f} ')
    path += f'L {xs+3*pitch:.1f} {yb2:.1f}'
    raw(f'<path d="{path}" stroke="{BLACK}" stroke-width="1.8" fill="none"/>')
    for i2 in range(3):
        x0 = xs + i2 * pitch + (pitch - iw) / 2
        text(x0 + iw / 2, yb2 - th_ - 8, "1.00", size=11, anchor="middle")
        text(x0 + iw + (pitch - iw) / 2, yb2 - 12, "OPENING 8.425 REF", size=10.5, anchor="middle")
    text(xs + 3 * pitch + 8, yb2 - th_ + 4, "Ø24.000 LINE", size=10)
    text(xs + 3 * pitch, yb2 + 14, "Ø23.000 LINE (OPENING ROOT)", size=10, anchor="end")
    raw(f'<line x1="{xs-26}" y1="{yb2:.1f}" x2="{xs-26}" y2="{yb2-th_:.1f}" '
        f'stroke="{BLACK}" stroke-width="0.9" marker-end="url(#ae)"/>')
    text(xs - 32, yb2 - th_ + 4, "RADIAL", size=10, anchor="end")
    text(xs + 1.5 * pitch, yb2 + 32, "PLATE BODY CONTINUES INBOARD (SOLID, FLAT)", size=10.5, anchor="middle")
    # edge elevation: constant thickness band — proves no raised surfaces
    yb3 = yb2 + 96
    tb = 26
    raw(f'<rect x="{xs}" y="{yb3}" width="{3*pitch}" height="{tb}" fill="url(#ht)" '
        f'stroke="{BLACK}" stroke-width="1.6"/>')
    for i2 in range(3):
        x0 = xs + i2 * pitch + (pitch - iw) / 2
        line(x0, yb3, x0, yb3 + tb, sw=0.7, dash="4 3")
        line(x0 + iw, yb3, x0 + iw, yb3 + tb, sw=0.7, dash="4 3")
    line(xs + 3 * pitch + 20, yb3, xs + 3 * pitch + 20, yb3 + tb, sw=0.8, m1=True, m2=True)
    text(xs + 3 * pitch + 28, yb3 + tb / 2 + 4, "1.000", size=11)
    text(xs, yb3 - 8, "EDGE ELEVATION (LOOKING RADIALLY INBOARD):", size=10.5)
    text(xs, yb3 + tb + 18, "CONSTANT 1.000 THK EVERYWHERE — FLAT FACES, NO RAISED SURFACES.", size=10.5)
    text(xs, yb3 + tb + 34, "DASHED: ISLAND SIDE EDGES. OPENING ROOT EDGE SITS 0.500 INBOARD.", size=10.5)
    line(xs, yb3 + tb + 52, xs + 3 * pitch, yb3 + tb + 52, sw=0.8, m1=True, m2=True)
    text(xs + 1.5 * pitch, yb3 + tb + 68,
         "REPEAT AROUND FULL CIRCUMFERENCE — 8 ISLANDS · PITCH 9.425 REF · 45° TYP",
         size=10.5, anchor="middle")

    # ============ table =======================================
    tx, ty = 490, 645
    text(tx, ty, "DIMENSIONAL SUMMARY", size=13.5, weight="bold")
    rows = [("PLATE DIAMETER (MAJOR OD)", "24.000"),
            ("MINOR OD (OPENING ROOTS)", "23.000"),
            ("PLATE THICKNESS", "1.000"),
            ("WELD ISLAND QTY / SPACING", "8 / 45.000°"),
            ("ISLAND WIDTH AT MAJOR OD", "1.000"),
            ("ISLAND RADIAL PROJECTION", "0.500"),
            ("OPENING RADIAL DEPTH", "0.500 THRU"),
            ("OPENING ARC AT OD", "8.425 REF"),
            ("INTERNAL CORNER RADIUS", "0.250 TYP"),
            ("OPENING TYPE", "FULL-THK THRU-CUT"),
            ("MATERIAL", "ASTM A36"),
            ("QUANTITY", "1")]
    c0, c1, c2 = tx, tx + 212, tx + 320
    th2 = 21
    line(c0, ty + 8, c2, ty + 8, sw=1.2)
    for i, (a, b) in enumerate(rows):
        text(c0 + 5, ty + 8 + (i + 1) * th2 - 6, a, size=11)
        text(c1 + 8, ty + 8 + (i + 1) * th2 - 6, b, size=11)
        line(c0, ty + 8 + (i + 1) * th2, c2, ty + 8 + (i + 1) * th2,
             sw=1.2 if i == len(rows) - 1 else 0.5)
    for c in (c0, c1, c2):
        line(c, ty + 8, c, ty + 8 + len(rows) * th2, sw=0.8)

    # ============ notes + tolerances ==========================
    notes = [
        "NOTES:",
        "1. ONE MONOLITHIC FLAT PLATE — NO RING/SHELF/LEDGE/STEP.",
        "2. OPENINGS FULL-THICKNESS THRU. WATERJET/PLASMA OK.",
        "3. ISLANDS = ONLY WELD ATTACHMENT POINTS (8X EQ SP).",
        "4. INTERNAL CORNERS R.250 UNO. DEBURR ALL EDGES.",
        "5. CUT FILE pizza-plate-24.dxf — ONE CLOSED CONTOUR,",
        "   TRUE ARCS. KERF COMP BY SHOP.",
        "6. STL = 1.000 EXTRUSION. STEP: IMPORT DXF, EXTRUDE 1.000.",
        "7. NO RAISED SURFACES — ISLANDS ARE IN-PLANE (DETAIL B).",
        "8. EST WT 119 LB. FLATNESS .060 MAX. VERIFY BEFORE CUT.",
    ]
    for i, nline in enumerate(notes):
        text(36, 872 + i * 14.5, nline, size=11, weight="bold" if i == 0 else "normal")
    bx, by = 1082, 940
    raw(f'<rect x="{bx}" y="{by}" width="382" height="72" fill="none" '
        f'stroke="{BLACK}" stroke-width="1.6"/>')
    text(bx + 191, by + 22, "ALL DIMENSIONS ARE IN INCHES", size=13, anchor="middle", weight="bold")
    text(bx + 191, by + 42, "TOLERANCES: ±0.030 U.N.O. · ANGLES ±0.25°", size=12, anchor="middle")
    text(bx + 191, by + 62, "DWG WPZ-PIZ-001 REV A · 2026-07-06 · SHT 1/1", size=11.5, anchor="middle")

    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'viewBox="0 0 {W} {H}">' + "".join(E) + "</svg>")
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "pizza-plate-24.svg"), "w") as f:
        f.write(svg)
    print("wrote pizza-plate-24.svg")


if __name__ == "__main__":
    verify()
    write_dxf()
    write_stl()
    sheet()
