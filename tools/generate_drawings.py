#!/usr/bin/env python3
"""Generate blueprint sheets for the smoker door spring-hinge assembly.

Outputs drawings/sheet1-assembly.svg .. sheet4-torque.svg.
All geometry is computed from the worked-example parameters below, which match
docs/DESIGN.md.  Run:  python3 tools/generate_drawings.py
"""
import math
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "drawings")

# ---------------------------------------------------------------- parameters
R_SHELL = 12.0          # chamber radius, in
DOOR_LO, DOOR_HI = -40.0, 80.0   # door arc on shell, deg from horizontal
HINGE = (13.2, 82.0)    # hinge pin: radius, angle deg (just off shell, above door)
W_DOOR, L_CG, BETA = 60.0, 12.24, 52.3   # lb, in, deg
K_SPR, PRELOAD, N_SPR = 110.0, 2.50, 2   # in-lb/turn, turns, count
CAM_BASE, VALLEY, RAMP = 2.50, 0.45, 15.0  # in, in, deg
NOTCH_D, NOTCH_W, NOTCH_AT = 0.20, 8.0, 88.0
F_FOLLOW = 120.0        # follower die-spring preload, lb
ROLLER_R = 0.75

SEAT_T = F_FOLLOW * VALLEY / math.radians(RAMP)
NOTCH_T = F_FOLLOW * NOTCH_D / math.radians(NOTCH_W)

# ---------------------------------------------------------------- style
BG = "#14304d"
LINE = "#e8f1fa"      # object lines
MED = "#bcd6ec"       # secondary
DIM = "#9fc2e0"       # dimensions
GHOST = "#7ea6c9"     # hidden / alternate position
ACCENT = "#f5b942"    # annotations / zones
FONT = "Consolas, 'Courier New', monospace"


class Sheet:
    def __init__(self, w=1500, h=1050):
        self.w, self.h = w, h
        self.e = []

    def raw(self, s):
        self.e.append(s)

    def line(self, x1, y1, x2, y2, stroke=LINE, sw=1.5, dash=None, marker=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        m = f' marker-end="url(#arr)"' if marker else ""
        self.raw(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                 f'stroke="{stroke}" stroke-width="{sw}"{d}{m}/>')

    def circle(self, cx, cy, r, stroke=LINE, sw=1.5, fill="none", dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.raw(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" stroke="{stroke}" '
                 f'stroke-width="{sw}" fill="{fill}"{d}/>')

    def path(self, d, stroke=LINE, sw=1.5, fill="none", dash=None):
        dd = f' stroke-dasharray="{dash}"' if dash else ""
        self.raw(f'<path d="{d}" stroke="{stroke}" stroke-width="{sw}" fill="{fill}"{dd}/>')

    def poly(self, pts, stroke=LINE, sw=1.5, fill="none", dash=None, close=False):
        d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts) + (" Z" if close else "")
        self.path(d, stroke, sw, fill, dash)

    def text(self, x, y, s, size=15, fill=LINE, anchor="start", weight="normal", rot=None):
        s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        r = f' transform="rotate({rot} {x:.1f} {y:.1f})"' if rot is not None else ""
        self.raw(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" '
                 f'fill="{fill}" text-anchor="{anchor}" font-weight="{weight}"{r}>{s}</text>')

    def leader(self, x1, y1, x2, y2, label, size=14, fill=ACCENT, anchor=None):
        self.line(x1, y1, x2, y2, stroke=fill, sw=1)
        self.circle(x1, y1, 2.5, stroke=fill, sw=1, fill=fill)
        a = anchor or ("end" if x2 < x1 else "start")
        dx = -6 if a == "end" else 6
        self.text(x2 + dx, y2 + 4, label, size=size, fill=fill, anchor=a)

    def dim_lin(self, x1, y1, x2, y2, label, off=0.0, size=14):
        """Linear dimension between two points, offset perpendicular by off px."""
        ang = math.atan2(y2 - y1, x2 - x1)
        nx, ny = -math.sin(ang), math.cos(ang)
        a = (x1 + nx * off, y1 + ny * off)
        b = (x2 + nx * off, y2 + ny * off)
        self.line(x1, y1, a[0] + nx * 5, a[1] + ny * 5, stroke=DIM, sw=0.8)
        self.line(x2, y2, b[0] + nx * 5, b[1] + ny * 5, stroke=DIM, sw=0.8)
        self.raw(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" '
                 f'stroke="{DIM}" stroke-width="1" marker-start="url(#arrs)" marker-end="url(#arr)"/>')
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        rot = math.degrees(ang)
        if rot > 90 or rot < -90:
            rot += 180
        self.text(mx + nx * 8, my + ny * 8, label, size=size, fill=DIM, anchor="middle", rot=rot)

    def frame_and_title(self, title, sheet_no, scale):
        self.raw(f'<rect x="0" y="0" width="{self.w}" height="{self.h}" fill="{BG}"/>')
        self.raw(f'<rect x="18" y="18" width="{self.w-36}" height="{self.h-36}" '
                 f'fill="none" stroke="{LINE}" stroke-width="2.5"/>')
        # title block, bottom right
        bx, by, bw, bh = self.w - 560, self.h - 138, 542, 120
        self.raw(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="none" '
                 f'stroke="{LINE}" stroke-width="1.5"/>')
        self.line(bx, by + 40, bx + bw, by + 40, sw=1)
        self.line(bx, by + 80, bx + bw, by + 80, sw=1)
        self.line(bx + 350, by + 40, bx + 350, by + bh, sw=1)
        self.text(bx + 12, by + 26, "OFFSET SMOKER — DOOR SPRING-HINGE ASSEMBLY",
                  size=17, weight="bold")
        self.text(bx + 12, by + 66, title, size=15, fill=MED)
        self.text(bx + 12, by + 106, "UNITS: INCHES · REV A — PROPOSAL", size=13, fill=DIM)
        self.text(bx + 362, by + 66, f"SHT {sheet_no}/4 · {scale}", size=14, fill=MED)
        self.text(bx + 362, by + 106, "2026-07-04", size=13, fill=DIM)

    def save(self, name):
        defs = (f'<defs>'
                f'<marker id="arr" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto">'
                f'<path d="M0,0 L10,4 L0,8 Z" fill="{DIM}"/></marker>'
                f'<marker id="arrs" markerWidth="10" markerHeight="8" refX="1" refY="4" orient="auto">'
                f'<path d="M10,0 L0,4 L10,8 Z" fill="{DIM}"/></marker>'
                f'<pattern id="hatch" width="7" height="7" patternTransform="rotate(45)" patternUnits="userSpaceOnUse">'
                f'<line x1="0" y1="0" x2="0" y2="7" stroke="{MED}" stroke-width="1"/></pattern>'
                f'</defs>')
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
               f'viewBox="0 0 {self.w} {self.h}">{defs}' + "".join(self.e) + "</svg>")
        os.makedirs(OUT, exist_ok=True)
        with open(os.path.join(OUT, name), "w") as f:
            f.write(svg)
        print("wrote", name)


# ---------------------------------------------------------------- transforms
def view(ox, oy, s):
    """inch-space (x right, y up) -> px with y flip"""
    return lambda x, y: (ox + x * s, oy - y * s)


def pol(r, deg):
    a = math.radians(deg)
    return (r * math.cos(a), r * math.sin(a))


def rot_about(p, c, deg):
    a = math.radians(deg)
    dx, dy = p[0] - c[0], p[1] - c[1]
    return (c[0] + dx * math.cos(a) - dy * math.sin(a),
            c[1] + dx * math.sin(a) + dy * math.cos(a))


def arc_pts(r, a0, a1, n=60):
    return [pol(r, a0 + (a1 - a0) * i / n) for i in range(n + 1)]


# ================================================================ SHEET 1
def sheet1():
    s = Sheet()
    s.frame_and_title("ASSEMBLY — END VIEW, DOOR 0°/45°/90°", 1, "14 PX/IN")
    T = view(560, 600, 14.0)
    H = pol(*HINGE)
    hx, hy = T(*H)

    # chamber shell
    s.circle(*T(0, 0), 12.0 * 14, sw=2.5)
    s.circle(*T(0, 0), 11.75 * 14, sw=1, dash="3 4")
    cx, cy = T(0, 0)
    s.line(cx - 20, cy, cx + 20, cy, stroke=MED, sw=0.8, dash="10 4 2 4")
    s.line(cx, cy - 20, cx, cy + 20, stroke=MED, sw=0.8, dash="10 4 2 4")

    # door band (sits proud of shell for clarity) + strap up to hinge pin
    RI, RO = 12.15, 12.55
    strap_top = pol((RI + RO) / 2, DOOR_HI + 1)

    def door_band(delta, color, sw, dash=None):
        inner = [rot_about(p, H, delta) for p in arc_pts(RI, DOOR_LO - 2, DOOR_HI + 1)]
        outer = [rot_about(p, H, delta) for p in arc_pts(RO, DOOR_LO - 2, DOOR_HI + 1)]
        s.poly([T(*p) for p in inner + outer[::-1]], stroke=color, sw=sw,
               dash=dash, close=True)
        s.line(*T(*rot_about(strap_top, H, delta)), *T(*H), stroke=color,
               sw=sw, dash=dash)

    door_band(0, LINE, 3)
    # 45 deg ghost: mid-surface arc only, to cut clutter
    mid45 = [rot_about(p, H, 45) for p in arc_pts((RI + RO) / 2, DOOR_LO - 2, DOOR_HI + 1)]
    s.poly([T(*p) for p in mid45], stroke=GHOST, sw=1.2, dash="6 5")
    s.line(*T(*rot_about(strap_top, H, 45)), *T(*H), stroke=GHOST, sw=1.2, dash="6 5")
    door_band(90, GHOST, 1.3, dash="6 5")

    # power spring canister (near shaft end) - dashed, with spiral
    s.circle(hx, hy, 3.5 * 14, stroke=MED, sw=1.6, dash="8 5")
    spiral = []
    for i in range(0, 361 * 4 + 1, 6):
        r = 0.75 + (2.9 - 0.75) * i / (360 * 4)
        a = math.radians(i)
        spiral.append(T(H[0] + r * math.cos(a), H[1] + r * math.sin(a)))
    s.poly(spiral, stroke=MED, sw=0.9)

    # cam disc (far shaft end) - phantom, with follower roller at seat
    s.circle(hx, hy, 2.5 * 14, stroke=ACCENT, sw=1.2, dash="12 4 2 4")
    roll = (H[0] + 2.80 * math.cos(math.radians(150)),
            H[1] + 2.80 * math.sin(math.radians(150)))
    s.circle(*T(*roll), ROLLER_R * 14, stroke=ACCENT, sw=1.4)

    # hinge pin, boss (drawn after canister so it reads on top)
    s.circle(hx, hy, 0.5 * 14, sw=2, fill=BG)
    s.circle(hx, hy, 0.75 * 14, sw=1.2)

    # standoff bracket: two struts from shell to canister rim
    for a_sh, a_cn in ((122, 138), (106, 112)):
        p_sh = pol(12.0, a_sh)
        p_cn = (H[0] + 3.5 * math.cos(math.radians(a_cn)),
                H[1] + 3.5 * math.sin(math.radians(a_cn)))
        s.line(*T(*p_sh), *T(*p_cn), stroke=LINE, sw=2.4)
    # heat shield between shell and canister
    for r_sh in (12.70, 12.85):
        s.poly([T(*pol(r_sh, a)) for a in range(96, 132, 3)], stroke=ACCENT, sw=1.2)

    # CG and weight arrow
    G = pol(9.92, 20)
    gx, gy = T(*G)
    s.circle(gx, gy, 4, stroke=ACCENT, sw=1.2, fill=ACCENT)
    s.raw(f'<line x1="{gx}" y1="{gy+8}" x2="{gx}" y2="{gy+52}" stroke="{ACCENT}" '
          f'stroke-width="1.5" marker-end="url(#arr)"/>')
    s.text(gx + 12, gy + 46, "W = 60 LB", size=14, fill=ACCENT)

    # travel arc with arrow: bottom door edge sweep about H
    tip_i, tip_o = pol(RI, DOOR_LO - 2), pol(RO, DOOR_LO - 2)
    sweep = [T(*rot_about(tip_o, H, d)) for d in range(15, 89, 3)]
    s.poly(sweep, stroke=ACCENT, sw=1.2, dash="4 5")
    p_end, p_prev = sweep[-1], sweep[-3]
    s.raw(f'<line x1="{p_prev[0]:.1f}" y1="{p_prev[1]:.1f}" x2="{p_end[0]:.1f}" y2="{p_end[1]:.1f}" '
          f'stroke="{ACCENT}" stroke-width="1.2" marker-end="url(#arr)"/>')
    mid = T(*rot_about(tip_o, H, 48))
    s.text(mid[0] + 12, mid[1], "90° TRAVEL", size=15, fill=ACCENT)

    # snap zone: thin swept sliver of the door tip, 0-15 deg
    sl = ([rot_about(tip_o, H, d) for d in range(0, 16, 3)] +
          [rot_about(tip_i, H, d) for d in range(15, -1, -3)])
    s.poly([T(*p) for p in sl], stroke=ACCENT, sw=1,
           fill="rgba(245,185,66,0.30)", close=True)
    sz = T(*rot_about(pol(RO + 0.4, DOOR_LO - 2), H, 8))
    s.leader(sz[0], sz[1], sz[0] + 140, sz[1] + 70, "SNAP ZONE 0–15°")

    # dimensions
    s.dim_lin(*T(-12, 0), *T(12, 0), "Ø24.00 SHELL", off=13.6 * 14)

    # leaders (spread clockwise to avoid collisions)
    s.leader(hx + 2.5 * 14 * 0.5, hy - 2.5 * 14 * 0.87, hx + 230, hy - 150,
             "SNAP CAM Ø5.00 — FAR SHAFT END (SHT 2)")
    s.leader(hx - 3.5 * 14 * 0.94, hy - 3.5 * 14 * 0.34, hx - 190, hy - 95,
             "POWER-SPRING CANISTER, 2 PL (SHT 3)", anchor="end")
    fx, fy = T(*roll)
    s.leader(fx, fy, fx - 130, fy + 65, "CAM FOLLOWER ROLLER (SHT 2)", anchor="end")
    shx, shy = T(*pol(12.78, 114))
    s.leader(shx, shy, shx - 110, shy - 75, "16-GA 304 HEAT SHIELD", anchor="end")
    bx1, by1 = T(*pol(12.0, 122))
    s.leader(bx1, by1, bx1 - 80, by1 + 105, "STANDOFF BRACKETS, 3/16 PLT, 2.00 AIR GAP",
             anchor="end")
    s.leader(hx, hy, hx + 250, hy - 55, "HINGE PIN Ø1.00, 1.2 OFF SHELL, 3 BUSHED BOSSES")
    dx1, dy1 = T(*rot_about(pol((RI + RO) / 2, 25), H, 45))
    s.leader(dx1, dy1, dx1 + 150, dy1 - 15, "DOOR AT 45° (ASSIST ZONE)")
    dx2, dy2 = T(*rot_about(pol(RO, 15), H, 90))
    s.leader(dx2, dy2, dx2 + 60, dy2 - 55, "DOOR AT 90° — HELD BY CAM NOTCH")
    ddx, ddy = T(*pol(RO, -14))
    s.leader(ddx, ddy, ddx + 150, ddy + 70, "DOOR, 120° ARC × 30 LG, CLOSED")

    # notes
    notes = [
        "NOTES:",
        "1. DOOR + HINGE SHAFT ROTATE TOGETHER; SHAFT RIDES IN 3",
        "   GRAPHITE-BRONZE BUSHED WELD BOSSES ON SHELL.",
        "2. ALL SPRING HARDWARE OUTBOARD, 2.00 AIR GAP BEHIND",
        "   POLISHED SS SHIELD. NO SPRING TOUCHES HOT STEEL.",
        "3. CAM DETENT PULLS DOOR SHUT LAST 15° (~105 IN-LB SEAL).",
        "4. SPRINGS CARRY ~73% OF DOOR WEIGHT: PEAK HAND EFFORT",
        "   ~11 LB AT 20 IN HANDLE VS 37 LB UNASSISTED.",
        "5. SHALLOW CAM NOTCH AT 88° PARKS DOOR VERTICAL.",
        "6. EXAMPLE CHAMBER 24 OD × 1/4 WALL; SEE DESIGN.MD §4",
        "   AND CALCULATOR.HTML TO RESCALE TO ACTUAL BLUEPRINTS.",
    ]
    for i, n in enumerate(notes):
        s.text(52, 60 + i * 22, n, size=14, fill=MED if i else LINE,
               weight="normal" if i else "bold")
    s.save("sheet1-assembly.svg")


# ================================================================ SHEET 2
def cam_radius(phi):
    """cam profile radius at cam angle phi deg (0 = valley seat)"""
    phi = phi % 360
    if phi <= RAMP:
        return CAM_BASE - VALLEY * (1 - phi / RAMP)
    if abs(phi - NOTCH_AT) <= NOTCH_W / 2:
        return CAM_BASE - NOTCH_D * math.cos(math.pi * (phi - NOTCH_AT) / NOTCH_W) ** 2
    if 93 <= phi <= 99:
        return CAM_BASE + 0.60 * math.sin(math.pi * (phi - 93) / 6)
    return CAM_BASE


def sheet2():
    s = Sheet()
    s.frame_and_title("SNAP CAM & FOLLOWER DETAIL", 2, "55 PX/IN")
    T = view(620, 560, 55.0)
    bx, by = T(0, 0)

    prof = [T(*pol(cam_radius(p), p + 150)) for p in [x * 0.5 for x in range(0, 721)]]
    s.poly(prof, sw=2.5, close=True)
    s.circle(bx, by, 0.5 * 55, sw=2, fill=BG)            # 1.000 bore
    kw, kd = 0.25 * 55, 0.125 * 55
    s.raw(f'<rect x="{bx-kw/2:.1f}" y="{by-0.5*55-kd:.1f}" width="{kw:.1f}" height="{kd:.1f}" '
          f'fill="none" stroke="{LINE}" stroke-width="2"/>')
    s.line(bx - 26, by, bx + 26, by, stroke=MED, sw=0.8, dash="10 4 2 4")
    s.line(bx, by - 26, bx, by + 26, stroke=MED, sw=0.8, dash="10 4 2 4")
    s.circle(bx, by, CAM_BASE * 55, stroke=MED, sw=0.7, dash="3 5")

    # roller seated in valley (valley direction = 150 deg global)
    roll = pol(cam_radius(0) + ROLLER_R, 150)
    rx, ry = T(*roll)
    s.circle(rx, ry, ROLLER_R * 55, stroke=ACCENT, sw=2)
    s.circle(rx, ry, 5, stroke=ACCENT, sw=1, fill=ACCENT)
    # follower arm + pivot
    piv = pol(7.0, 118)
    px, py = T(*piv)
    s.line(px, py, rx, ry, stroke=ACCENT, sw=2.4)
    s.circle(px, py, 8, stroke=ACCENT, sw=2, fill=BG)
    # die spring: zigzag from mid-arm, perpendicular, to anchor block
    mid = ((piv[0] + roll[0]) / 2, (piv[1] + roll[1]) / 2)
    av = (roll[0] - piv[0], roll[1] - piv[1])
    al = math.hypot(*av)
    perp = (-av[1] / al, av[0] / al)
    if perp[0] > 0:
        perp = (-perp[0], -perp[1])
    anch = (mid[0] + 2.9 * perp[0], mid[1] + 2.9 * perp[1])
    ax, ay = T(*anch)
    mx, my = T(*mid)
    zig = []
    for i in range(9):
        t = i / 8
        x, y = mx + (ax - mx) * t, my + (ay - my) * t
        if 0 < i < 8:
            off = 9 if i % 2 else -9
            ang = math.atan2(ay - my, ax - mx) + math.pi / 2
            x += off * math.cos(ang); y += off * math.sin(ang)
        zig.append((x, y))
    s.poly(zig, stroke=ACCENT, sw=1.8)
    s.raw(f'<rect x="{ax-10:.1f}" y="{ay-5:.1f}" width="20" height="10" fill="none" '
          f'stroke="{ACCENT}" stroke-width="1.6"/>')

    # angular position markers
    for adeg, lab, r_lab in [(150, "0° SEAT", 4.35), (165, "15° RAMP END", 4.45),
                             (238, "88° HOLD-OPEN", 4.05), (246, "93° STOP TAB", 5.0)]:
        s.line(*T(*pol(CAM_BASE + 0.75, adeg)), *T(*pol(CAM_BASE + 1.45, adeg)),
               stroke=DIM, sw=1)
        tx, ty = T(*pol(r_lab, adeg))
        s.text(tx, ty, lab, size=13, fill=DIM, anchor="middle")

    # dimensions & leaders
    s.dim_lin(bx, by, *T(*pol(CAM_BASE, 200)), "R2.500 BASE", off=14)
    vx, vy = T(*pol(cam_radius(0), 150))
    s.leader(vx, vy, 240, 330, "VALLEY .450 × 15° RAMP", anchor="end")
    nx, ny = T(*pol(CAM_BASE - NOTCH_D, 238))
    s.leader(nx, ny, 850, 660, "NOTCH .200 DP × 8° WIDE")
    s.leader(bx, by - 0.5 * 55 - kd, 850, 380, "Ø1.000 BORE, 1/4 × 1/8 KEYWAY, .500 PLT")
    stx, sty = T(*pol(CAM_BASE + 0.6, 246))
    s.leader(stx, sty, 750, 780, "STOP TAB — DOOR HALTS AT 93°")
    s.leader(rx - 20, ry + 20, 270, 540, "1.50 CAM FOLLOWER ROLLER", anchor="end")
    s.leader(px, py, 618, 200, "PIVOT, Ø.500 SHOULDER BOLT ON BRACKET")
    s.leader(ax, ay + 8, 330, 700, "DIE SPRING 1 OD × 2.5, 120 LB PRELOAD + ADJUSTER")

    notes = [
        "NOTES:",
        "1. VALLEY RAMP: .450 RISE OVER 15°, LINEAR, BLEND R.12 ENDS.",
        f"   SEAT DETENT TORQUE = 120 LB × .450/.262 RAD ≈ {SEAT_T:.0f} IN-LB.",
        f"2. HOLD-OPEN NOTCH TORQUE ≈ {NOTCH_T:.0f} IN-LB.",
        "3. DWELL 15°–84° IS CONSTANT RADIUS — ZERO CAM TORQUE IN",
        "   ASSIST ZONE; DOOR FEEL THERE IS PURE RIBBON SPRING.",
        "4. FLAME-CUT OK; GRIND RAMP AND NOTCH SMOOTH. EDGE BREAK .03.",
        "5. CAM KEYED TO SHAFT: VALLEY SEATS WHEN DOOR FULLY CLOSED.",
    ]
    for i, n in enumerate(notes):
        s.text(52, 60 + i * 22, n, size=14, fill=MED if i else LINE,
               weight="normal" if i else "bold")
    s.save("sheet2-cam.svg")


# ================================================================ SHEET 3
def sheet3():
    s = Sheet()
    s.frame_and_title("POWER-SPRING CANISTER — SECTION & FACE", 3, "48 PX/IN")
    T = view(510, 470, 48.0)
    SHELL_X = -3.35          # shell surface; case left face at -1.35 -> 2.00 gap

    # section through axis: x = axial, y = radial
    s.line(*T(-4.1, 0), *T(4.2, 0), stroke=MED, sw=0.8, dash="12 4 2 4")
    # shaft
    s.poly([T(-3.9, 0.5), T(3.6, 0.5)], sw=2)
    s.poly([T(-3.9, -0.5), T(3.6, -0.5)], sw=2)
    # arbor hub
    for sgn in (1, -1):
        s.poly([T(-1.0, 0.5 * sgn), T(-1.0, 0.815 * sgn), T(1.0, 0.815 * sgn),
                T(1.0, 0.5 * sgn)], sw=2)
    # ribbon coil (hatched annulus) both sides
    for sgn in (1, -1):
        y0, y1 = 0.815 * sgn, 2.55 * sgn
        s.raw(f'<rect x="{T(-1.0,0)[0]:.1f}" y="{min(T(0,y0)[1],T(0,y1)[1]):.1f}" '
              f'width="{2.0*48:.1f}" height="{abs(y1-y0)*48:.1f}" fill="url(#hatch)" '
              f'stroke="{MED}" stroke-width="1.2"/>')
    # case: U section, ID 6.5, OD 7.0, internal width 2.25; bolted cover right
    for sgn in (1, -1):
        s.poly([T(-1.35, 0.55 * sgn), T(-1.35, 3.5 * sgn), T(1.35, 3.5 * sgn),
                T(1.35, 3.25 * sgn), T(-1.125, 3.25 * sgn), T(-1.125, 0.55 * sgn)],
               sw=2, close=True)
        s.poly([T(1.125, 0.55 * sgn), T(1.125, 3.25 * sgn)], sw=2)
        s.poly([T(1.35, 0.55 * sgn), T(1.35, 3.30 * sgn)], sw=2)
        # ratchet teeth on case OD
        for x in (-1.05, -0.45, 0.15, 0.75):
            s.poly([T(x, 3.5 * sgn), T(x + 0.18, 3.72 * sgn), T(x + 0.36, 3.5 * sgn)],
                   stroke=ACCENT, sw=1.4)
    # pawl + bracket collar, top
    s.poly([T(-0.10, 4.4), T(0.15, 3.75), T(0.40, 4.4)], stroke=ACCENT, sw=1.8)
    s.text(*T(0.62, 4.62), "PAWL", size=13, fill=ACCENT)
    s.poly([T(SHELL_X, 4.1), T(-0.2, 4.1), T(-0.10, 4.4)], sw=2.2)
    # shell + heat shield in gap
    s.poly([T(SHELL_X, -4.6), T(SHELL_X, 4.6)], sw=3)
    s.poly([T(SHELL_X - 0.22, -4.6), T(SHELL_X - 0.22, 4.6)], sw=1.2)
    s.text(*T(SHELL_X, 5.35), "SHELL / END OF DOOR CUTOUT", size=13, fill=MED,
           anchor="middle")
    for xs in (-2.50, -2.62):
        s.poly([T(xs, -4.2), T(xs, 4.2)], stroke=ACCENT, sw=1.4)
    s.text(*T(-2.56, -4.62), "16-GA 304 SHIELD", size=13, fill=ACCENT, anchor="middle")

    # keeper pin
    s.line(*T(0.4, 3.75), *T(0.4, 2.2), stroke=ACCENT, sw=1.2, dash="5 4")
    s.leader(*T(0.4, 2.9), 720, 240, "KEEPER-PIN HOLE — LOCK BEFORE SERVICE")

    # dimensions (case dims on right, widths below)
    s.dim_lin(*T(1.35, 3.5), *T(1.35, -3.5), "7.00 OD", off=-115)
    s.dim_lin(*T(1.125, 3.25), *T(1.125, -3.25), "6.50 CASE ID", off=-70)
    s.dim_lin(*T(-1.125, -3.25), *T(1.125, -3.25), "2.25 CASE WIDTH", off=60)
    s.dim_lin(*T(SHELL_X, 3.9), *T(-1.35, 3.9), "2.00 AIR GAP", off=-34)
    s.leader(*T(0.5, 1.7), 820, 175, "RIBBON COIL 2.00 × .085, WOUND ON ARBOR")
    s.leader(*T(-3.7, -0.5), 150, 600, "Ø1.000 HINGE SHAFT", anchor="start")
    s.leader(*T(-0.5, 0.815), 120, 260, "Ø1.25 ARBOR, KEYED + RIBBON SLOT", anchor="start")

    # face view, right side
    F = view(1130, 430, 40.0)
    fx, fy = F(0, 0)
    s.circle(fx, fy, 3.5 * 40, sw=2)
    for a in range(0, 360, 15):
        s.line(*F(*pol(3.5, a)), *F(*pol(3.72, a + 7)), stroke=ACCENT, sw=1.2)
        s.line(*F(*pol(3.72, a + 7)), *F(*pol(3.5, a + 15)), stroke=ACCENT, sw=1.2)
    s.circle(fx, fy, 0.5 * 40, sw=1.6)
    s.circle(fx, fy, 0.625 * 40, sw=1.2)
    spiral = []
    for i in range(0, 361 * 5 + 1, 5):
        r = 0.68 + (3.1 - 0.68) * i / (360 * 5)
        spiral.append(F(*pol(r, i)))
    s.poly(spiral, stroke=MED, sw=1.1)
    s.text(fx, fy + 3.5 * 40 + 46, "FACE VIEW — COVER OFF", size=14, fill=MED,
           anchor="middle")
    s.text(fx, fy + 3.5 * 40 + 68, "WIND CASE W/ SPANNER; PAWL CLICKS 15°/TOOTH",
           size=13, fill=DIM, anchor="middle")

    notes = [
        "NOTES:",
        "1. SPRING: 2.00 × .085 CR-SI RIBBON, 175 IN LG (14.6 FT),",
        "   K ≈ 110 IN-LB/TURN. INNER END KEYED TO ARBOR (ON SHAFT),",
        "   OUTER END HOOKED TO CASE.",
        "2. NOMINAL PRELOAD 2.5 TURNS/SPRING (σ = 114 KSI).",
        "   MAX 3.25 TURNS (σ = 150 KSI) — STAMP LIMIT ON CASE.",
        "3. CASE ROTATES IN BRACKET COLLAR FOR PRELOAD; PAWL HOLDS.",
        "4. ⚠ STORED ENERGY ~250 J WOUND. INSTALL KEEPER PIN BEFORE",
        "   REMOVING ANY BRACKET FASTENER.",
        "5. SOURCING: CUSTOM POWER SPRING (VULCAN, JOHN EVANS' SONS).",
        "   BUDGET ALT: GARAGE-DOOR TORSION STOCK, SAME SHAFT + CAM",
        "   — SEE DESIGN.MD §7.",
    ]
    for i, n in enumerate(notes):
        s.text(52, 730 + i * 20, n, size=13, fill=MED if i else LINE,
               weight="normal" if i else "bold")
    s.save("sheet3-canister.svg")


# ================================================================ SHEET 4
def sheet4():
    s = Sheet()
    s.frame_and_title("TORQUE BALANCE VS DOOR ANGLE", 4, "CHART")
    x0, y0, w, h = 150, 120, 1180, 640          # plot area
    tmin, tmax = -800, 700

    def X(th): return x0 + th / 90 * w
    def Y(t): return y0 + (tmax - t) / (tmax - tmin) * h

    # grid
    for th in range(0, 91, 15):
        s.line(X(th), y0, X(th), y0 + h, stroke="#27496e", sw=1)
        s.text(X(th), y0 + h + 24, f"{th}°", size=14, fill=DIM, anchor="middle")
    for t in range(tmin, tmax + 1, 100):
        s.line(x0, Y(t), x0 + w, Y(t), stroke="#27496e", sw=1 if t else 0)
        s.text(x0 - 10, Y(t) + 5, f"{t}", size=13, fill=DIM, anchor="end")
    s.line(x0, Y(0), x0 + w, Y(0), stroke=MED, sw=1.8)
    s.raw(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="none" '
          f'stroke="{LINE}" stroke-width="1.5"/>')
    s.text(x0 + w / 2, y0 + h + 52, "DOOR OPENING ANGLE", size=15, fill=MED, anchor="middle")
    s.text(x0 - 100, y0 + h / 2, "TORQUE ABOUT HINGE, IN-LB (OPENING +)", size=15,
           fill=MED, anchor="middle", rot=-90)

    # snap zone + hold-open shading
    s.raw(f'<rect x="{X(0)}" y="{y0}" width="{X(15)-X(0):.1f}" height="{h}" '
          f'fill="rgba(245,185,66,0.10)"/>')
    s.raw(f'<rect x="{X(84)}" y="{y0}" width="{X(90)-X(84):.1f}" height="{h}" '
          f'fill="rgba(245,185,66,0.10)"/>')
    s.text(X(7.5), y0 + 24, "SNAP", size=13, fill=ACCENT, anchor="middle")
    s.text(X(87), y0 + 24, "HOLD", size=13, fill=ACCENT, anchor="middle")

    def Tg(th): return -W_DOOR * L_CG * math.cos(math.radians(th - BETA))
    def Ts(th): return N_SPR * K_SPR * (PRELOAD - th / 360)
    def Tc(th): return -SEAT_T * max(0.0, 1 - th / RAMP)

    ths = [i / 4 for i in range(0, 361)]
    s.poly([(X(t), Y(Tg(t))) for t in ths], stroke=GHOST, sw=2, dash="7 5")
    s.poly([(X(t), Y(Ts(t))) for t in ths], stroke=MED, sw=2, dash="2 4")
    s.poly([(X(t), Y(Tc(t))) for t in ths if t <= 16], stroke=ACCENT, sw=2, dash="7 3 2 3")
    s.poly([(X(t), Y(Tg(t) + Ts(t) + Tc(t))) for t in ths], stroke=ACCENT, sw=3.5)

    # legend
    lx, ly = x0 + 40, y0 + 180
    for i, (lab, col, dash, sw) in enumerate([
            ("GRAVITY (CLOSING)", GHOST, "7 5", 2),
            ("RIBBON SPRINGS ×2 (OPENING)", MED, "2 4", 2),
            ("CAM DETENT (CLOSING, 0–15°)", ACCENT, "7 3 2 3", 2),
            ("NET ON DOOR", ACCENT, None, 3.5)]):
        s.line(lx, ly + i * 26, lx + 56, ly + i * 26, stroke=col, sw=sw, dash=dash)
        s.text(lx + 68, ly + i * 26 + 5, lab, size=14, fill=col)

    # annotations
    s.leader(X(2), Y(Tg(2) + Ts(2) + Tc(2)), X(13), Y(-560),
             "NET CLOSING THRU ENTIRE SNAP ZONE — NO STALL")
    s.leader(X(55), Y(Tg(55) + Ts(55)), X(48), Y(-430),
             "PEAK EFFORT 216 IN-LB ≈ 11 LB AT 20 IN HANDLE", anchor="end")
    s.leader(X(89), Y(Tg(89) + Ts(89)), X(66), Y(-260),
             "-86 AT 90°: HELD BY 172 IN-LB NOTCH", anchor="end")
    s.leader(X(52.3), Y(Tg(52.3)), X(60), Y(-740),
             "BARE DOOR PEAKS 735 IN-LB (37 LB AT HANDLE)")

    s.save("sheet4-torque.svg")


if __name__ == "__main__":
    sheet1()
    sheet2()
    sheet3()
    sheet4()
