"""MotionCore product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders: the clear anodized finned module with rounded
extrusion edges, a gasket parting line under the lid, stainless lid screws, a name plate and a
rating label, a clear inspection window over the safety supervisor, contactor and fuse block,
and the keyed connector panel (yellow XT90 anti-spark socket, knurled motor plug socket, two
coded M12 sockets, vent plug and a lit green ready light). Beside it sit the named reference
250 W geared hub motor (two spoke flanges, side covers, axle nuts, speed sensor magnet ring and
Hall pickup on a small bracket), the yellow twin-channel e-stop station with its red mushroom
head, the key and throttle pod and the pair of brake interlock switches. Context is a compact
bench top and a simplified harness with mated plugs.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.
A research prototype, not certified to any machinery or vehicle standard.

Every main dimension and interface comes from PARAMS in model.py: enclosure 220 x 140 x 60 mm
with 3 mm walls and 11 fins per side, 3 mm lid, four isolation pads on the 180 x 100 mm pattern,
the connector panel and its four connectors at their model.py positions, the internal envelopes,
the hub motor (190 mm diameter, 90 mm wide, 180 mm axle, flange radius +6 mm) and the e-stop
station (76 mm box, 62 mm high, 48 mm head). Axes as model.py: X along the module (connector
panel on +X), Y across the fins, front toward -Y, Z up, bench top at Z = 0, module centered on
the origin. For a compact render the kit devices are drawn closer to the module than in
model.py (MOTOR_X, ESTOP_XY, POD_SHIFT, BRAKE_SHIFT below) and the motor is raised 6 mm so its
flanges rest on the bench. See docs/REVIEW.md, session 2026-09-26.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from math import cos, radians, sin
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build123d import (Axis, Box, Compound, Cylinder, Plane, Pos, RegularPolygon, Rot, Solid, Sphere, Vector,
                       extrude, fillet)
from model import PARAMS, envelope  # noqa: F401  (envelope kept for callers that want it)

TITLE = "MotionCore: drive controller and safety module with e-stop and reference hub motor"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "accessory", "context"], "explode": False, "el": 30, "az": -40,
     "note": "Product render from the front right and above (about 30 deg elevation); reference hub motor at left, "
             "finned controller and safety module at center with its connector panel toward the camera, key and "
             "throttle pod (front) and e-stop station (behind) at right, brake switches in front"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): lid, window and screws; "
             "safety supervisor, motor controller, contactor and precharge and fuse block; finned body and pads; "
             "connector panel; e-stop head and collar; speed sensor ring and pickup on the hub motor"},
    {"name": "detail", "groups": ["shell", "internal"], "explode": False, "el": 32, "az": -35,
     "note": "Detail from the front right and above (about 32 deg elevation): the module alone, with the "
             "supervisor, contactor and fuse block behind the clear window and the green ready light lit"},
]

# Render layout (not the model.py bench layout): devices drawn closer to the module.
MOTOR_X = -300.0            # hub motor axle X (model.py: -380)
ESTOP_XY = (255.0, 60.0)    # e-stop station centre (model.py: 300, 150)
POD_SHIFT = (-100.0, -40.0)  # key and throttle pod moved by this from its model.py position
BRAKE_SHIFT = (-310.0, 20.0)  # brake switches moved by this from their model.py position
BENCH = (-430.0, 335.0, -175.0, 120.0, 25.0)   # x0, x1, y0, y1, thickness

# Colours (restrained product palette; kit accent)
C_ALU = "#C3C8CE"
C_ALU_LID = "#CFD4D9"
C_DARK = "#2B2F36"
C_BLACK = "#1C1F24"
C_PANEL = "#23272E"
C_ACCENT = "#0F766E"
C_WINDOW = "#DCEBF5"
C_STEEL = "#B8BEC6"
C_RUBBER = "#26292E"
C_LABEL = "#F4F4F2"
C_PCB = "#166534"
C_PCB_CTRL = "#1E3A5F"
C_CHIP = "#111827"
C_BRASS = "#C9A227"
C_COPPER = "#B87333"
C_XT90 = "#E3B505"
C_YELLOW = "#E1B000"
C_YELLOW2 = "#F0C94A"
C_RED = "#C62828"
C_LED_G = "#22C55E"
C_LED_R = "#5E1C1C"
C_HUB = "#2A2E35"
C_HUB_COVER = "#9AA1A9"
C_POD = "#343840"
C_BENCH = "#D8CFC0"
C_CABLE = "#1F2329"


def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _box(cx, cy, cz, sx, sy, sz):
    return Pos(cx, cy, cz) * Box(sx, sy, sz)


def _bx(x0, x1, y0, y1, z0, z1):
    return _box((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2, x1 - x0, y1 - y0, z1 - z0)


def _rbx(x0, x1, y0, y1, z0, z1, r, top=None):
    """Box with rounded vertical edges (radius r) and optionally rounded top edges."""
    s = _bx(x0, x1, y0, y1, z0, z1)
    s = _fillet_try(s, s.edges().filter_by(Axis.Z), [r, r * 0.7, r * 0.4])
    if top:
        s = _fillet_try(s, _top(s), [top, top * 0.6, top * 0.3])
    return s


def _zcyl(x, y, z, r, h):
    return Pos(x, y, z) * Cylinder(r, h)


def _ycyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(90, 0, 0) * Cylinder(r, h)


def _xcyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(0, 90, 0) * Cylinder(r, h)


def _pipe(points, r):
    """Round cable through `points` with spherical joints (clean bends)."""
    out = None
    for a, c in zip(points, points[1:]):
        a, c = Vector(*a), Vector(*c)
        d = c - a
        seg = Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))
        out = seg if out is None else out + seg
    for q in points[1:-1]:
        out += Pos(*q) * Sphere(r)
    return out


def _top(s):
    return s.faces().sort_by(Axis.Z)[-1].edges()


def _bottom(s):
    return s.faces().sort_by(Axis.Z)[0].edges()


def _xmax(s):
    return s.faces().sort_by(Axis.X)[-1].edges()


def _xmin(s):
    return s.faces().sort_by(Axis.X)[0].edges()


def _ymin(s):
    return s.faces().sort_by(Axis.Y)[0].edges()


def _hex_x(x, y, z, af, length):
    """Hex prism along X (across flats `af`), centred on x."""
    return Pos(x - length / 2, y, z) * extrude(Plane.YZ * RegularPolygon(af / 1.732, 6), amount=length)


def _hex_y(x, y, z, af, length):
    return Pos(x, y + length / 2, z) * extrude(Plane.XZ * RegularPolygon(af / 1.732, 6), amount=length)


def _hex_z(x, y, z, af, h):
    return Pos(x, y, z - h / 2) * extrude(RegularPolygon(af / 1.732, 6), amount=h)


def _union(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def product_parts(P=PARAMS):
    L, W, H, T = P["body_l"], P["body_w"], P["body_h"], P["wall"]
    z0 = P["pad_h"]                 # body underside
    fl = z0 + T                     # inside floor
    top = z0 + H                    # body top, lid underside
    lt = P["lid_t"]
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    # ------------------------------------------------------------ enclosure body (BOM 6)
    R_OUT = 6.0
    outer = _rbx(-L / 2, L / 2, -W / 2, W / 2, z0, top, R_OUT)
    outer = _fillet_try(outer, _bottom(outer), [1.5, 1.0])
    inner = _rbx(-L / 2 + T, L / 2 - T, -W / 2 + T, W / 2 - T, fl, top + 1, R_OUT - T)
    body = outer - inner
    # gasket parting line: shallow groove round the top outer edge
    groove = _bx(-L / 2 - 2, L / 2 + 2, -W / 2 - 2, W / 2 + 2, top - 1.0, top + 0.01) \
        - _rbx(-L / 2 + 0.6, L / 2 - 0.6, -W / 2 + 0.6, W / 2 - 0.6, top - 2, top + 1, R_OUT - 0.6)
    body -= groove
    # fins (11 per side), rounded tips
    n, pitch, ft, fd = P["fin_n"], P["fin_pitch"], P["fin_t"], P["fin_depth"]
    fin0 = _bx(-ft / 2, ft / 2, W / 2 - 0.5, W / 2 + fd, z0 + P["fin_z0"], z0 + P["fin_z1"])
    fin0 = _fillet_try(fin0, fin0.faces().sort_by(Axis.Y)[-1].edges(), [1.6, 1.0, 0.6])
    fins = []
    for i in range(n):
        x = (i - (n - 1) / 2) * pitch
        fins.append(Pos(x, 0, 0) * fin0)
        fins.append(Pos(x, 0, 0) * Rot(0, 0, 180) * fin0)
    body += _union(fins)
    # M6 bosses and insert bores (host interface, as model.py)
    mx, my = P["mount_px"] / 2, P["mount_py"] / 2
    for sx in (-1, 1):
        for sy in (-1, 1):
            body += _zcyl(sx * mx, sy * my, fl + 4, 6, 8)
            body -= _zcyl(sx * mx, sy * my, z0 + 5, 2.5, 12)
    add("Enclosure body, finned aluminum", body, C_ALU, "metal", 6, "shell", (0, 0, 0))

    gasket = _rbx(-L / 2 + 0.6, L / 2 - 0.6, -W / 2 + 0.6, W / 2 - 0.6, top - 0.9, top, R_OUT - 0.6) \
        - _rbx(-L / 2 + T, L / 2 - T, -W / 2 + T, W / 2 - T, top - 2, top + 1, R_OUT - T)
    add("Lid gasket (visible edge)", gasket, C_RUBBER, "rubber", 7, "shell", (0, 0, 95))

    pads = None
    for sx in (-1, 1):
        for sy in (-1, 1):
            c = _zcyl(sx * mx, sy * my, z0 / 2, P["pad_d"] / 2, z0)
            c = _fillet_try(c, _bottom(c), [0.8, 0.5])
            pads = c if pads is None else pads + c
    add("Isolation pads", pads, C_RUBBER, "rubber", 14, "shell", (0, 0, -40))

    # ------------------------------------------------------------ lid (BOM 7) with inspection window
    EL = (0, 0, 150)
    lid = _rbx(-L / 2, L / 2, -W / 2, W / 2, top, top + lt, R_OUT, top=1.2)
    lid += _bx(-L / 2 + T + 1, L / 2 - T - 1, -W / 2 + T + 1, W / 2 - T - 1, top - 3, top)   # gasket lip
    wx0, wx1, wy0, wy1 = -85.0, 90.0, -42.0, 42.0
    lid -= _rbx(wx0 - 3, wx1 + 3, wy0 - 3, wy1 + 3, top + lt - 1.5, top + lt + 1, 7.0)       # pane recess
    lid -= _rbx(wx0, wx1, wy0, wy1, top - 4, top + lt + 1, 5.0)                              # window opening
    add("Enclosure lid", lid, C_ALU_LID, "metal", 7, "shell", EL)
    pane = _rbx(wx0 - 2.6, wx1 + 2.6, wy0 - 2.6, wy1 + 2.6, top + lt - 1.4, top + lt - 0.2, 6.6)
    add("Clear polycarbonate inspection window", pane, C_WINDOW, "clear", 7, "shell", (0, 0, 175))

    zt = top + lt
    scr = []
    for (x, y) in [(-100, -60), (-100, 60), (100, -60), (100, 60), (-100, 0), (100, 0)]:
        s = _zcyl(x, y, zt + 0.6, 3.0, 1.2)
        s = _fillet_try(s, _top(s), [0.6, 0.3])
        s -= _box(x, y, zt + 1.2, 3.6, 0.8, 1.0) + _box(x, y, zt + 1.2, 0.8, 3.6, 1.0)
        scr.append(s)
    add("Lid screws, stainless", _union(scr), C_STEEL, "metal", 7, "shell", (0, 0, 210))

    plate = _rbx(-55, 55, -57, -46, zt, zt + 0.5, 1.5)
    add("Name plate", plate, C_ACCENT, "painted", 14, "shell", EL)
    ink = _bx(-50, -12, -53.5, -49.5, zt + 0.5, zt + 0.8) + _bx(20, 50, -52.5, -50.5, zt + 0.5, zt + 0.8)
    add("Name plate print", ink, C_LABEL, "paper", 14, "shell", EL)
    rl = _rbx(-60, 20, 46, 57, zt, zt + 0.4, 1.0)
    add("Rating label", rl, C_LABEL, "paper", 14, "shell", EL)
    rink = _bx(-56, -30, 52, 55, zt + 0.4, zt + 0.6) + _bx(-56, 10, 48, 50, zt + 0.4, zt + 0.6) \
        + _bx(-24, 14, 52, 55, zt + 0.4, zt + 0.6)
    add("Rating label print", rink, C_DARK, "paper", 14, "shell", EL)

    # ------------------------------------------------------------ internals (BOM 2 to 5)
    # 2 motor controller on the floor: heat plate, board, bus capacitors, FETs
    cx0, cx1, cy0, cy1, czb, chh = P["controller"]
    EC = (0, 0, 45)
    add("Controller heat plate", _bx(cx0, cx1, cy0, cy1, fl, fl + 3), "#9EA5AD", "metal", 2, "internal", EC)
    pcb = _rbx(cx0 + 1, cx1 - 1, cy0 + 1, cy1 - 1, fl + 3, fl + 4.6, 2.0)
    add("Motor controller board", pcb, C_PCB_CTRL, "plastic", 2, "internal", EC)
    caps = _union([_zcyl(x, cy1 - 9, fl + 4.6 + 9, 5.5, 18) for x in (-60, -47, -34)])
    add("Bus capacitors", caps, C_BLACK, "plastic", 2, "internal", EC)
    ctop = _union([_zcyl(x, cy1 - 9, fl + 4.6 + 18.3, 5.0, 0.6) for x in (-60, -47, -34)])
    add("Bus capacitor vents", ctop, C_STEEL, "metal", 2, "internal", EC)
    fets = _union([_bx(-28 + 7 * k, -23 + 7 * k, cy0 + 4, cy0 + 12, fl + 4.6, fl + 6.2) for k in range(4)])
    fets += _bx(-90, -72, -20, -2, fl + 4.6, fl + 6.0) + _bx(-18, -4, 0, 12, fl + 4.6, fl + 10)
    add("Controller semiconductors", fets, C_CHIP, "plastic", 2, "internal", EC)
    phase = _union([_bx(-6, -1, -26 + 11 * k, -19 + 11 * k, fl + 4.6, fl + 7) for k in range(3)])
    add("Phase terminals", phase, C_COPPER, "metal", 2, "internal", EC)

    # 3 safety supervisor board on four brass standoffs
    sx0, sx1, sy0, sy1, szb, sh = P["supervisor"]
    ES = (0, 0, 110)
    sz = fl + szb
    stand = _union([_hex_z(x, y, (fl + sz) / 2, 6.0, sz - fl) for x in (sx0 + 7, sx1 - 7) for y in (sy0 + 7, sy1 - 7)])
    add("Supervisor standoffs", stand, C_BRASS, "metal", 3, "internal", (0, 0, 80))
    sb = _rbx(sx0, sx1, sy0, sy1, sz, sz + 1.6, 2.0)
    for x in (sx0 + 7, sx1 - 7):
        for y in (sy0 + 7, sy1 - 7):
            sb -= _zcyl(x, y, sz + 0.8, 1.7, 3)
    add("Safety supervisor board", sb, C_PCB, "plastic", 3, "internal", ES)
    s1 = sz + 1.6
    chips = (_bx(-60, -48, -6, 6, s1, s1 + 1.6) + _bx(-40, -33, 8, 13, s1, s1 + 1.4) + _bx(-40, -33, -13, -8, s1, s1 + 1.4)
             + _bx(-85, -70, 10, 24, s1, s1 + 6) + _bx(-30, -18, -26, -16, s1, s1 + 3))
    add("Supervisor MCU, CAN transceivers and buck", chips, C_CHIP, "plastic", 3, "internal", ES)
    usb = _bx(-95.5, -87, -5, 5, s1, s1 + 3.2)
    usb = _fillet_try(usb, usb.edges().filter_by(Axis.X), [1.2, 0.8])
    add("Supervisor USB fault-log port", usb, C_STEEL, "metal", 3, "internal", ES)
    hdr = _bx(-25, -13, 18, 26, s1, s1 + 7)
    add("Supervisor header", hdr, C_BLACK, "plastic", 3, "internal", ES)
    sled = _bx(-66, -63, -22, -19, s1, s1 + 1.0)
    add("Supervisor heartbeat LED (lit)", sled, C_LED_G, "emissive", 3, "internal", ES)

    # 4 main DC contactor with terminal studs
    kx0, kx1, ky0, ky1, kzb, kh = P["contactor"]
    EK = (0, 0, 80)
    kbody = _rbx(kx0, kx1, ky0, ky1, fl + 2, fl + kh, 6.0, top=2.0)
    kbody += _rbx(kx0 + 7, kx1 - 7, ky0 - 8, ky0 + 1, fl + 30, fl + 42, 2.0, top=1.0)
    add("Main DC contactor", kbody, C_BLACK, "plastic", 4, "internal", EK)
    kfoot = _rbx(kx0 - 5, kx1 + 5, -16, 16, fl, fl + 2, 3.0)
    add("Contactor mounting foot", kfoot, C_STEEL, "metal", 4, "internal", EK)
    studs = []
    for x in (kx0 + 13, kx1 - 13):
        studs.append(_zcyl(x, ky0 - 4, fl + 45, 3.0, 6))
        studs.append(_hex_z(x, ky0 - 4, fl + 43.5, 10.0, 3.0))
    add("Contactor terminal studs and nuts", _union(studs), C_COPPER, "metal", 4, "internal", EK)
    klab = _bx(kx0 + 8, kx1 - 8, -12, 12, fl + kh, fl + kh + 0.4)
    add("Contactor label", klab, C_LABEL, "paper", 4, "internal", EK)

    # 5 precharge resistor and fuse holder with blade fuse
    fx0, fx1, fy0, fy1, fzb, fh = P["fuseblock"]
    EF = (0, 0, 55)
    res = _bx(fx0 + 1, fx1 - 1, fy0 + 1, -5, fl, fl + 14)
    for k in range(4):
        res -= _bx(fx0, fx1, fy0 + 1 - 0.1, fy0 + 3, fl + 3 + 3 * k, fl + 4.2 + 3 * k)
        res -= _bx(fx0, fx1, -7, -4.9, fl + 3 + 3 * k, fl + 4.2 + 3 * k)
    add("Precharge resistor, aluminum clad", res, C_BRASS, "metal", 5, "internal", EF)
    fh_ = _rbx(fx0 + 1, fx1 - 1, 1, fy1 - 1, fl, fl + fh - 6, 2.0, top=1.0)
    add("Fuse holder", fh_, C_BLACK, "plastic", 5, "internal", EF)
    fuse = _rbx(fx0 + 8, fx1 - 8, 9, 17, fl + fh - 6, fl + fh, 1.0)
    add("Main blade fuse", fuse, C_YELLOW2, "plastic", 5, "internal", EF)

    # ------------------------------------------------------------ connector panel (BOM 8)
    PX = L / 2
    pt, cln, cz = P["panel_t"], P["conn_len"], z0 + P["conn_z"]
    EP = (70, 0, 0)
    pw = P["panel_w"]
    panel = _bx(PX, PX + pt, -pw / 2, pw / 2, z0 + P["panel_z0"], z0 + P["panel_z1"])
    panel = _fillet_try(panel, panel.edges().filter_by(Axis.X), [3.0, 2.0])
    panel = _fillet_try(panel, _xmax(panel), [0.8, 0.5])
    add("Connector panel plate", panel, C_PANEL, "painted", 8, "shell", EP)
    xf = PX + pt
    pscr = []
    for y in (-pw / 2 + 5, pw / 2 - 5):
        for z in (z0 + P["panel_z0"] + 5, z0 + P["panel_z1"] - 5):
            s = _xcyl(xf + 0.5, y, z, 2.2, 1.0)
            s -= _box(xf + 1.0, y, z, 1.0, 3.0, 0.6)
            pscr.append(s)
    add("Panel screws", _union(pscr), C_STEEL, "metal", 8, "shell", EP)

    y, w, h = P["xt90"]
    xt = _bx(xf, xf + cln, y - w / 2, y + w / 2, cz - h / 2, cz + h / 2)
    xt = _fillet_try(xt, xt.edges().filter_by(Axis.X), [2.0, 1.5])
    xt += _bx(xf, xf + 2.5, y - w / 2 - 3, y + w / 2 + 3, cz - h / 2 - 2, cz + h / 2 + 2)
    for dy in (-5.5, 5.5):
        xt -= _xcyl(xf + cln - 3, y + dy, cz, 3.6, 7)
    add("XT90 anti-spark socket", xt, C_XT90, "plastic", 8, "shell", EP)
    xpins = _union([_xcyl(xf + cln - 4.5, y + dy, cz, 2.2, 5) for dy in (-5.5, 5.5)])
    add("XT90 contacts", xpins, C_BRASS, "metal", 8, "shell", EP)

    (_, ym, rm), (_, ys, rs), (_, yc, rc) = P["conns"]
    # motor plug socket, knurled coupling ring
    mo = _hex_x(xf + 1.5, ym, cz, 19.0, 3.0) + _xcyl(xf + 3 + (cln - 3) / 2, ym, cz, rm, cln - 3)
    for k in range(18):
        mo -= Pos(xf + 11, ym, cz) * Rot(360 / 18 * k, 0, 0) * Pos(0, 0, rm) * Box(12, 1.2, 1.4)
    mo -= _xcyl(xf + cln - 1.5, ym, cz, rm - 3, 3.1)
    add("Motor plug socket, 9-pin", mo, C_BLACK, "plastic", 8, "shell", EP)
    add("Motor socket insert", _xcyl(xf + cln - 2.5, ym, cz, rm - 3, 1.0), C_DARK, "plastic", 8, "shell", EP)

    def m12(yy, r):
        s = _hex_x(xf + 2, yy, cz, 17.0, 4.0) + _xcyl(xf + 4 + (cln - 4) / 2, yy, cz, r, cln - 4)
        for k in range(5):
            s -= _xcyl(xf + 7 + 2 * k, yy, cz, r + 1, 0.7) - _xcyl(xf + 7 + 2 * k, yy, cz, r - 0.6, 1)
        s -= _xcyl(xf + cln - 2, yy, cz, r - 2.5, 4.1)
        return s
    add("M12 safety-loop socket, A-coded", m12(ys, rs), C_STEEL, "metal", 8, "shell", EP)
    add("M12 command socket, B-coded", m12(yc, rc), C_STEEL, "metal", 8, "shell", EP)
    ins = _xcyl(xf + cln - 3.5, ys, cz, rs - 2.5, 1.0) + _xcyl(xf + cln - 3.5, yc, cz, rc - 2.5, 1.0)
    add("M12 socket inserts", ins, C_BLACK, "plastic", 8, "shell", EP)
    add("Safety-loop coding ring", _xcyl(xf + 4.8, ys, cz, rs + 0.5, 1.6), C_YELLOW, "painted", 8, "shell", EP)
    add("Command coding ring", _xcyl(xf + 4.8, yc, cz, rc + 0.5, 1.6), C_ACCENT, "painted", 8, "shell", EP)

    vz = z0 + P["panel_z1"] - 7
    vent = _hex_x(xf + 1.5, -36, vz, 10.0, 3.0) + (Pos(xf + 3, -36, vz) * Sphere(4.0) & _bx(xf + 3, xf + 8, -41, -31, vz - 5, vz + 5))
    add("Pressure-equalizing vent plug", vent, C_DARK, "plastic", 8, "shell", EP)

    for yy, col, mat, nm in [(18.0, C_LED_G, "emissive", "Ready light, green (lit)"),
                             (30.0, C_LED_R, "plastic", "Fault light, red")]:
        bez = _xcyl(xf + 0.7, yy, vz, 3.4, 1.4)
        add(nm.split(",")[0] + " bezel", bez, C_BLACK, "plastic", 3, "shell", EP)
        dome = _xcyl(xf + 1.6, yy, vz, 2.4, 1.2) + (Pos(xf + 2.2, yy, vz) * Sphere(2.4) & _bx(xf + 2.2, xf + 5, yy - 3, yy + 3, vz - 3, vz + 3))
        add(nm, dome, col, mat, 3, "shell", EP)

    lz = z0 + P["panel_z0"] + 3.5
    legend = _union([_bx(xf, xf + 0.3, yy - 5, yy + 5, lz - 0.8, lz + 0.8) for yy in (y, ym, ys, yc)])
    add("Panel legends", legend, C_LABEL, "paper", 8, "shell", EP)

    # ------------------------------------------------------------ reference hub motor (BOM 1)
    MR, MW = P["motor_d"] / 2, P["motor_w"]
    MX, MZ = MOTOR_X, MR + 6.0          # flanges (radius MR + 6) rest on the bench
    shell = _ycyl(MX, 0, MZ, MR, MW)
    shell = _fillet_try(shell, shell.edges(), [10.0, 7.0, 4.0])
    add("Hub motor shell", shell, C_HUB, "painted", 1, "accessory", (0, 0, 0))
    fl_ = []
    for yy in (-MW / 2 + 12, MW / 2 - 12):
        f = _ycyl(MX, yy, MZ, MR + 6, 4.0) - _ycyl(MX, yy, MZ, MR - 6, 5.0)
        for k in range(18):
            a = radians(360 / 18 * k + (10 if yy > 0 else 0))
            f -= _ycyl(MX + (MR + 2.5) * cos(a), yy, MZ + (MR + 2.5) * sin(a), 1.3, 6)
        fl_.append(f)
    add("Hub spoke flanges", _union(fl_), C_HUB_COVER, "metal", 1, "accessory", (0, 0, 0))
    covers, cbolts = [], []
    for sgn in (-1, 1):
        yy = sgn * (MW / 2 + 0.7)
        covers.append(_ycyl(MX, yy, MZ, MR - 20, 1.6))
        for k in range(6):
            a = radians(60 * k + 30)
            b = _ycyl(MX + 62 * cos(a), sgn * (MW / 2 + 2.0), MZ + 62 * sin(a), 3.0, 1.2)
            cbolts.append(b)
    covers.append(_ycyl(MX, -MW / 2 - 4, MZ, 16, 8))       # bearing boss inside the magnet ring
    add("Hub side covers", _union(covers), C_HUB_COVER, "metal", 1, "accessory", (0, 0, 0))
    add("Side cover screws", _union(cbolts), C_STEEL, "metal", 1, "accessory", (0, 0, 0))
    axle = _ycyl(MX, 0, MZ, 6, P["axle_l"])
    for sgn in (-1, 1):
        for sx in (-1, 1):
            axle -= _box(MX + sx * 9, sgn * (P["axle_l"] / 2 - 12), MZ, 8, 26, 20)
    add("Axle with flats", axle, C_STEEL, "metal", 1, "accessory", (0, 0, 0))
    nuts = []
    for sgn in (-1, 1):
        nuts.append(_ycyl(MX, sgn * (MW / 2 + 9), MZ, 10.0, 2.0))
        nuts.append(_hex_y(MX, sgn * (MW / 2 + 19), MZ, 15.0, 7.0))
    add("Axle nuts and washers", _union(nuts), C_STEEL, "metal", 1, "accessory", (0, 0, 0))

    # 12 independent speed sensor: magnet ring on the -Y side and Hall pickup on a bracket
    ring = _ycyl(MX, -MW / 2 - 4, MZ, 40, 5) - _ycyl(MX, -MW / 2 - 4, MZ, 18, 6)
    add("Speed sensor magnet ring", ring, C_BLACK, "plastic", 12, "accessory", (0, -45, 0))
    mags = _union([_ycyl(MX + 30 * cos(radians(45 * k)), -MW / 2 - 6.8, MZ + 30 * sin(radians(45 * k)), 3.5, 1.2)
                   for k in range(8)])
    add("Speed sensor magnets", mags, "#8E949B", "metal", 12, "accessory", (0, -45, 0))
    hall = _rbx(MX + 44, MX + 64, -MW / 2 - 16, -MW / 2 - 2, MZ - 10, MZ + 10, 2.0)
    hall = _fillet_try(hall, _ymin(hall), [1.5, 1.0])
    add("Hall speed pickup", hall, C_DARK, "plastic", 12, "accessory", (0, -75, 0))
    brk = _bx(MX, MX + 50, -MW / 2 - 13, -MW / 2 - 10, MZ - 5, MZ + 5)
    brk = _fillet_try(brk, brk.edges().filter_by(Axis.Y), [2.0, 1.0])
    brk -= _ycyl(MX, -MW / 2 - 11.5, MZ, 6.2, 5)
    add("Pickup bracket", brk, C_STEEL, "metal", 12, "accessory", (0, -75, 0))

    # ------------------------------------------------------------ e-stop station (BOM 9)
    EX, EY = ESTOP_XY
    e = P["estop_box"] / 2
    eh = P["estop_h"]
    ebox = _rbx(EX - e, EX + e, EY - e, EY + e, 0, eh, 6.0, top=3.0)
    ebox -= _bx(EX - e - 2, EX + e + 2, EY - e - 2, EY + e + 2, eh - 12.8, eh - 12) \
        - _rbx(EX - e + 0.7, EX + e - 0.7, EY - e + 0.7, EY + e - 0.7, eh - 14, eh - 11, 5.3)
    add("E-stop enclosure", ebox, C_YELLOW, "plastic", 9, "accessory", (0, 0, 0))
    escr = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            s = _zcyl(EX + sx * (e - 8), EY + sy * (e - 8), eh + 0.5, 2.6, 1.0)
            s -= _box(EX + sx * (e - 8), EY + sy * (e - 8), eh + 1.0, 3.4, 0.7, 0.8)
            escr.append(s)
    add("E-stop lid screws", _union(escr), C_STEEL, "metal", 9, "accessory", (0, 0, 20))
    legend = _zcyl(EX, EY, eh + 0.3, 29.0, 0.6) - _zcyl(EX, EY, eh + 0.3, 15.0, 1)
    add("E-stop legend disc", legend, C_YELLOW2, "painted", 9, "accessory", (0, 0, 20))
    ticks = _union([Pos(EX, EY, eh + 0.75) * Rot(0, 0, 30 * k) * Pos(22, 0, 0) * Box(8, 2.2, 0.3)
                    for k in range(12) if k not in (3, 9)])
    add("E-stop legend print", ticks, C_DARK, "paper", 9, "accessory", (0, 0, 20))
    collar = _zcyl(EX, EY, eh + 6, 14, 12)
    collar = _fillet_try(collar, _top(collar), [1.5, 1.0])
    add("E-stop collar", collar, "#3A3F46", "metal", 9, "accessory", (0, 0, 35))
    head = _zcyl(EX, EY, eh + 12 + 9, P["estop_head_d"] / 2, 18)
    head = _fillet_try(head, _top(head), [8.0, 6.0, 4.0])
    head = _fillet_try(head, _bottom(head), [1.5, 1.0])
    add("E-stop mushroom head", head, C_RED, "plastic", 9, "accessory", (0, 0, 60))
    eg = _hex_x(EX - e - 2, EY, 16, 18.0, 4.0) + _xcyl(EX - e - 8, EY, 16, 7.5, 8)
    eg = _fillet_try(eg, _xmin(eg), [2.0, 1.0])
    add("E-stop cable gland", eg, C_DARK, "plastic", 9, "accessory", (-25, 0, 0))

    # ------------------------------------------------------------ key switch and throttle pod (BOM 11)
    dx, dy = POD_SHIFT
    pod = _rbx(320 + dx, 380 + dx, -40 + dy, 0 + dy, 0, 34, 6.0, top=4.0)
    add("Key and throttle pod", pod, C_POD, "plastic", 11, "accessory", (0, 0, 0))
    kxp, kyp = 335 + dx, -20 + dy
    kb = _zcyl(kxp, kyp, 34 + 2, 9.0, 4.0)
    kb = _fillet_try(kb, _top(kb), [1.2, 0.8])
    kb += _zcyl(kxp, kyp, 34 + 7, 7.0, 6.0)
    add("Key switch bezel and cylinder", kb, C_STEEL, "metal", 11, "accessory", (0, 0, 30))
    key = _box(kxp, kyp, 34 + 13, 2.2, 10, 6) + _ycyl(kxp, kyp, 34 + 24, 9, 2.2) - _ycyl(kxp, kyp, 34 + 27, 2.2, 4)
    add("Enable key", key, "#A7ADB5", "metal", 11, "accessory", (0, 0, 55))
    kring = _zcyl(kxp, kyp, 34.2, 13.5, 0.4) - _zcyl(kxp, kyp, 34.2, 9.5, 1)
    add("Key position legend", kring, C_LABEL, "paper", 11, "accessory", (0, 0, 0))
    thr = _rbx(360 + dx, 395 + dx, -30 + dy, -10 + dy, 10, 24, 3.0, top=2.0)
    for k in range(5):
        thr -= _bx(372 + dx + 4.5 * k, 374 + dx + 4.5 * k, -31 + dy, -9 + dy, 22.8, 25)
    add("Thumb throttle lever", thr, C_BLACK, "rubber", 11, "accessory", (35, 0, 0))
    pg = _hex_x(320 + dx - 2, -20 + dy, 14, 14.0, 4.0) + _xcyl(320 + dx - 7, -20 + dy, 14, 5.5, 6)
    add("Pod cable gland", pg, C_DARK, "plastic", 11, "accessory", (-20, 0, 0))

    # ------------------------------------------------------------ brake interlock switches (BOM 10)
    bdx, bdy = BRAKE_SHIFT
    bodies, levers, plung = [], [], []
    for x0, x1, lx0, lx1 in [(250, 300, 290, 330), (360, 410, 400, 440)]:
        b = _rbx(x0 + bdx, x1 + bdx, -170 + bdy, -150 + bdy, 0, 22, 4.0, top=2.5)
        bodies.append(b)
        lv = _bx(lx0 + bdx, lx1 + bdx, -165 + bdy, -155 + bdy, 22, 30)
        lv = _fillet_try(lv, lv.edges().filter_by(Axis.Y), [3.0, 2.0])
        levers.append(lv)
        plung.append(_zcyl(x0 + bdx + 12, -160 + bdy, 23.5, 3.0, 3.0))
    add("Brake switch bodies", _union(bodies), C_DARK, "plastic", 10, "accessory", (0, -30, 0))
    add("Brake switch levers", _union(levers), C_STEEL, "metal", 10, "accessory", (0, -30, 25))
    add("Brake switch plungers", _union(plung), C_RED, "rubber", 10, "accessory", (0, -30, 12))

    # ------------------------------------------------------------ context: bench and harness
    x0, x1, y0, y1, bt = BENCH
    bench = _bx(x0, x1, y0, y1, -bt, 0)
    bench = _fillet_try(bench, bench.edges().filter_by(Axis.X), [3.0, 2.0])
    add("Bench top", bench, C_BENCH, "wood", None, "context", (0, 0, 0))

    xe = xf + cln
    boots = (_bx(xe, xe + 16, y - w / 2, y + w / 2, cz - h / 2, cz + h / 2)
             + _xcyl(xe + 7, ym, cz, rm - 0.5, 14)
             + _xcyl(xe + 5, ys, cz, rs + 0.5, 10) + _xcyl(xe + 14, ys, cz, rs - 1.5, 10)
             + _xcyl(xe + 5, yc, cz, rc + 0.5, 10) + _xcyl(xe + 14, yc, cz, rc - 1.5, 10))
    add("Mated harness plugs", boots, C_CABLE, "plastic", 13, "context", (0, 0, 0))
    pack_plug = _rbx(172, 188, -160, -138, 1, 13, 2.0)
    add("Pack lead XT90 plug", pack_plug, C_XT90, "plastic", 13, "context", (0, 0, 0))
    hx = xe + 16
    cables = [_pipe([(hx, y, cz), (hx + 12, y, cz), (hx + 22, y, 8), (180, -110, 6), (180, -138, 7)], 4.5)]
    cables.append(_pipe([(xe + 14, ym, cz), (hx + 4, ym, cz), (hx + 10, ym, 6), (150, -106, 4.5), (-190, -106, 4.5),
                    (MX + 20, -82, 4.5), (MX + 2, -MW / 2 - 30, 30), (MX, -MW / 2 - 24, MZ - 8)], 4.0))
    cables.append(_pipe([(xe + 19, ys, cz), (hx + 6, ys, cz), (hx + 14, ys, 5), (EX - e - 26, EY - 12, 5),
                    (EX - e - 12, EY, 16)], 3.5))
    cables.append(_pipe([(xe + 19, yc, cz), (hx + 6, yc, cz), (hx + 16, yc, 5), (320 + dx - 30, -20 + dy, 5),
                    (320 + dx - 10, -20 + dy, 14)], 3.5))
    cables.append(_pipe([(MX + 54, -MW / 2 - 9, MZ - 10), (MX + 58, -MW / 2 - 9, 20), (MX + 70, -95, 4), (-190, -106, 4.5)], 2.5))
    cables.append(_pipe([(250 + bdx, -160 + bdy, 8), (238 + bdx, -160 + bdy, 4), (238 + bdx, -122 + bdy, 4),
                    (100, -106, 4.5)], 2.5))
    cables.append(_pipe([(360 + bdx, -160 + bdy, 8), (348 + bdx, -160 + bdy, 4), (348 + bdx, -120 + bdy, 4)], 2.5))
    add("Wiring harness, keyed connectors", Compound(cables), C_CABLE, "rubber", 13, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:44s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:9.2f} cm3")
