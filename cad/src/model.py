"""MotionCore parametric model (build123d), TRL 3, constructable design (MTC-DDR-003).

Run from the repo root:
    python cad/src/model.py            export STEP and STL, print envelopes and run the checks
    python cad/src/model.py --check    constructability checks only (overlaps, contacts, clearances)

The prototype is the MotionCore module bolted to a plywood bench board through its host mounting
interface, with the reference hub motor held by its axle in two slotted uprights (wheel off the
board), the e-stop station screwed to the board and the brake levers and the key and throttle pod
clamped on a short handlebar stub. Every component can be cut, drilled, bent or bought, and every
joint has a fixing (MTC-DDR-003 lists the changes from the concept model).

Axes: X along the module length (connector end on +X), Y across the fins, Z up. Units mm.
Bench board top at Z = 0. The module is centred on the origin in X and Y.
"""
from __future__ import annotations

import math
import sys
from dataclasses import dataclass
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # Enclosure (MTC-PRC-001, R12). body_h = floor plate + finned tube.
    "body_l": 220.0, "body_w": 140.0, "body_h": 59.0, "wall": 3.0,
    "floor_t": 3.0,              # 6061 plate under the tube, thermally conductive sealant film between
    "lid_t": 3.0, "gasket_t": 1.0,
    "fin_n": 11, "fin_pitch": 19.0, "fin_t": 3.0, "fin_depth": 14.0,
    "fin_z0": 3.0, "fin_z1": 59.0,          # fin span from the body underside: the full tube height
    "port_r": 4.5, "port_hole": 3.3,        # screw ports in the tube's inside corners, tapped M4
    # Host mounting interface: four M6 closed-end rivet nuts in the floor plate on rubber pads
    "mount_px": 180.0, "mount_py": 100.0, "pad_d": 16.0, "pad_h": 3.0, "rivnut_flange": (13.0, 1.0),
    "rivnut_body": (9.0, 13.0),             # diameter, height above the floor
    # Connectors in the +X end wall (interface v0.1, plus the speed sensor socket)
    "panel_t": 0.0, "panel_w": 102.0, "panel_z0": 14.0, "panel_z1": 52.0,
    "conn_len": 18.0, "conn_z": 31.5,       # protrusion outside the wall; centre height above the body underside
    "xt90": (-42.0, 11.0, 21.0),            # y, width (Y), height (Z): XT90 stood on end in a panel frame 18 x 34
    "conns": [("motor", -14.0, 10.0), ("safety", 13.0, 8.0), ("command", 39.0, 8.0)],
    "motor_flange": 13.0, "motor_nut_af": 24.0, "m12_flange": 20.0,
    "speed_socket": (-85.5, 21.0),          # x on the -Y wall between two fins; height above the body underside
    "vent_z": 46.0,                         # adhesive membrane vent on the -X end wall
    # Internal parts (x0, x1, y0, y1, z0 above the floor top, height)
    "controller": (-100.0, 0.0, -35.0, 25.0, 1.0, 24.0),   # VESC class, 75 V stage, on a 1 mm thermal pad
    "supervisor": (-95.0, -10.0, -50.0, 58.0, 35.0, 10.0),  # board on 35 mm standoffs, outside the controller; 20 mm longer on +Y for the economizer (MTC-DEC-001, 2026-10-02)
    "economizer": (-86.0, -62.0, 41.0, 55.0, 8.0),          # coil economizer module on the carrier board: x0, x1, y0, y1, height above the board
    "sup_standoffs": [(-80.0, -44.0), (-20.0, -44.0), (-80.0, 32.0), (-20.0, 32.0)],
    "contactor": (15.0, 65.0, -22.0, 22.0, 3.0, 45.0),     # on a 3 mm mounting foot
    "contactor_foot": (5.0, 75.0, -12.0, 12.0),
    "fuseblock": (15.0, 67.0, 32.0, 62.0, 0.0, 22.0),      # precharge resistor and fuse holder, beside the contactor
    # Bench rig (prototype only, BOM line 15)
    "board": (-520.0, 440.0, -240.0, 240.0, 18.0),
    "motor_x": -380.0, "motor_d": 190.0, "motor_w": 90.0, "axle_l": 180.0, "axle_z": 120.0, "axle_flats": 10.0,
    "upright": (60.0, 6.0, 150.0), "upright_gap": 135.0,  # flat bar width, thickness, height; inside spacing
    "foot": (40.0, 4.0, 60.0),               # equal angle leg, thickness, length
    "ring": (18.0, 40.0, 5.0), "ring_pcd": 44.0,
    "hall": (20.0, 11.0, 20.0), "hall_gap": 3.5,
    "bar": (22.2, 270.0, 140.0, -160.0, 70.0),   # handlebar stub OD, length, x start, y, z
    "post": (40.0, 6.0, 90.0), "post_x": (160.0, 390.0),
    "pod_x": (255.0, 290.0), "levers_x": (180.0, 370.0),
    "estop_xy": (300.0, 150.0), "estop_box": 76.0, "estop_h": 62.0, "estop_head_d": 48.0,
}


@dataclass
class Comp:
    """One component: a single made or bought piece (or a matched set of fixings)."""
    name: str
    shape: object
    bom: int | None
    kind: str            # "made", "bought" or "fixing"
    color: str


# ------------------------------------------------------------------ geometry helpers
def _b3d():
    import build123d as b
    return b


def bx(x0, x1, y0, y1, z0, z1):
    b = _b3d()
    return b.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * b.Box(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0))


def zcyl(x, y, z, r, h):
    b = _b3d()
    return b.Pos(x, y, z) * b.Cylinder(r, h)


def ycyl(x, y, z, r, h):
    b = _b3d()
    return b.Pos(x, y, z) * b.Rot(90, 0, 0) * b.Cylinder(r, h)


def xcyl(x, y, z, r, h):
    b = _b3d()
    return b.Pos(x, y, z) * b.Rot(0, 90, 0) * b.Cylinder(r, h)


def hexprism(axis, x, y, z, af, h):
    b = _b3d()
    s = b.extrude(b.RegularPolygon(af / math.sqrt(3), 6), h / 2, both=True)
    rot = {"z": b.Rot(0, 0, 0), "y": b.Rot(90, 0, 0), "x": b.Rot(0, 90, 0)}[axis]
    return b.Pos(x, y, z) * rot * s


def fuse(shapes):
    out = None
    for s in shapes:
        if s is None:
            continue
        out = s if out is None else out + s
    return out


def _tube(a, c, r):
    b = _b3d()
    a = b.Vector(*a); c = b.Vector(*c); d = c - a
    return b.Solid.make_cylinder(r, d.length, b.Plane(origin=a, z_dir=d.normalized()))


def _path(points, r):
    """A cable: straight runs with a ball at each bend so the runs join."""
    b = _b3d()
    s = None
    for a, c in zip(points, points[1:]):
        t = _tube(a, c, r)
        s = t if s is None else s + t
    for q in points[1:-1]:
        s = s + b.Pos(*q) * b.Sphere(r)
    return s


# ------------------------------------------------------------------ derived dimensions
def derived(p=PARAMS):
    L, W = p["body_l"], p["body_w"]
    z_pad = p["pad_h"]
    z_floor = z_pad + p["rivnut_flange"][1]          # floor plate underside
    z_tube = z_floor + p["floor_t"]                  # floor top = tube bottom
    z_top = z_floor + p["body_h"]                    # tube top
    z_lid = z_top + p["gasket_t"]
    px, py = L / 2 - p["wall"] - p["port_r"], W / 2 - p["wall"] - p["port_r"]
    return {
        "z_floor": z_floor, "z_tube": z_tube, "z_top": z_top, "z_lid": z_lid, "z_lid_top": z_lid + p["lid_t"],
        "cz": z_floor + p["conn_z"], "ports": [(sx * px, sy * py) for sx in (-1, 1) for sy in (-1, 1)],
        "mounts": [(sx * p["mount_px"] / 2, sy * p["mount_py"] / 2) for sx in (-1, 1) for sy in (-1, 1)],
        "fin_x": [(i - (p["fin_n"] - 1) / 2) * p["fin_pitch"] for i in range(p["fin_n"])],
        "inner_x": L / 2 - p["wall"], "inner_y": W / 2 - p["wall"],
        "tube_h": p["body_h"] - p["floor_t"],
    }


def envelope(p=PARAMS):
    """Overall module envelope (length, width, height) in mm, from the parameters alone:
    connectors on +X, the vent patch on -X, fins on both long sides, pads under and the lid on top."""
    length = p["body_l"] + p["conn_len"] + 1.5
    width = p["body_w"] + 2 * p["fin_depth"]
    height = p["pad_h"] + p["rivnut_flange"][1] + p["body_h"] + p["gasket_t"] + p["lid_t"] + 2.2   # lid screw heads
    return length, width, height


def inner_box(p, key):
    D = derived(p)
    x0, x1, y0, y1, zb, h = p[key]
    return bx(x0, x1, y0, y1, D["z_tube"] + zb, D["z_tube"] + zb + h)


def floor_holes(p=PARAMS):
    """Every hole in the floor plate: (x, y, diameter, what). Taken by the making sketch and the plan."""
    D = derived(p)
    out = [(x, y, 9.0, "rivet nut") for x, y in D["mounts"]]
    out += [(x, y, 4.5, "floor screw, countersunk") for x, y in D["ports"]]
    x0, x1, y0, y1, _, _ = p["controller"]
    out += [(x, y, 2.5, "controller, M3 tapped") for x in (x0 + 4, x1 - 4) for y in (y0 + 4, y1 - 4)]
    out += [(x, y, 2.5, "supervisor standoff, M3 tapped") for x, y in p["sup_standoffs"]]
    fx0, fx1 = p["contactor_foot"][0], p["contactor_foot"][1]
    out += [(x, 0.0, 3.3, "contactor foot, M4 tapped") for x in (fx0 + 5, fx1 - 5)]
    q = p["fuseblock"]
    out += [(x, (q[2] + q[3]) / 2, 3.3, "fuse block, M4 tapped") for x in (q[0] + 5, q[1] - 5)]
    return out


# ------------------------------------------------------------------ components
COL = {"tube": "#A8B0B8", "floor": "#8B949E", "lid": "#D1D5DB", "gasket": "#111827", "ctrl": "#0F766E",
       "sup": "#15803D", "stand": "#B8860B", "cont": "#C2410C", "fuse": "#B45309", "conn": "#1F2937",
       "xt90": "#D4A017", "vent": "#F9FAFB", "rivnut": "#6B7280", "pad": "#374151", "motor": "#374151",
       "ring": "#0EA5E9", "hall": "#0369A1", "estop": "#D4A017", "lever": "#2563EB", "pod": "#7C3AED",
       "harness": "#111827", "board": "#D6C3A1", "upright": "#94A3B8", "foot": "#64748B", "bar": "#9CA3AF",
       "post": "#94A3B8", "bolt": "#111827", "bracket": "#475569"}


def build_components(p=PARAMS):
    """All components of the prototype, in build order, as {key: Comp}."""
    b = _b3d()
    D = derived(p)
    L, W, T = p["body_l"], p["body_w"], p["wall"]
    zf, zt, ztop, zl = D["z_floor"], D["z_tube"], D["z_top"], D["z_lid"]
    ix, iy = D["inner_x"], D["inner_y"]
    cz = D["cz"]
    C = {}

    def add(key, name, shape, bom, kind, color):
        C[key] = Comp(name, shape, bom, kind, color)

    # ---- 1 floor plate, with its holes
    floor = bx(-L / 2, L / 2, -W / 2, W / 2, zf, zt)
    for x, y, d, _ in floor_holes(p):
        floor = floor - zcyl(x, y, (zf + zt) / 2, d / 2, p["floor_t"] + 2)
    add("floor", "Floor plate", floor, 6, "made", COL["floor"])

    # ---- 2 finned tube, cut from an extrusion, with the end wall and side wall holes
    tube = bx(-L / 2, L / 2, -W / 2, W / 2, zt, ztop) - bx(-ix, ix, -iy, iy, zt - 1, ztop + 1)
    for x in D["fin_x"]:
        for s in (-1, 1):
            tube = tube + bx(x - p["fin_t"] / 2, x + p["fin_t"] / 2, min(s * W / 2, s * (W / 2 + p["fin_depth"])),
                             max(s * W / 2, s * (W / 2 + p["fin_depth"])), zt, ztop)
    for x, y in D["ports"]:
        sx, sy = (1 if x > 0 else -1), (1 if y > 0 else -1)
        tube = tube + zcyl(x, y, (zt + ztop) / 2, p["port_r"], ztop - zt) + bx(x, sx * ix, y, sy * iy, zt, ztop)
        tube = tube - zcyl(x, y, (zt + ztop) / 2, p["port_hole"] / 2, ztop - zt + 2)
    for k, (cut, _) in connector_holes(p).items():
        tube = tube - cut
    add("tube", "Finned tube", tube, 6, "made", COL["tube"])

    # ---- 3 rivet nuts, set in the floor (from below) before the tube goes on
    fd, ft = p["rivnut_flange"]
    rd, rh = p["rivnut_body"]
    rv = fuse([zcyl(x, y, zf - ft / 2, fd / 2, ft) + zcyl(x, y, zf + rh / 2, rd / 2, rh) -
               zcyl(x, y, zf + rh / 2 - 2, 3.0, rh) for x, y in D["mounts"]])
    add("rivnuts", "M6 closed-end rivet nuts (4)", rv, 14, "bought", COL["rivnut"])

    # ---- 4 floor screws (countersunk, from below, into the corner ports)
    fs = fuse([zcyl(x, y, zf + p["floor_t"] / 2, 2.25, p["floor_t"]) + zcyl(x, y, zt + 5, p["port_hole"] / 2, 10)
               for x, y in D["ports"]])
    add("floor_screws", "M4 floor screws (4)", fs, 14, "fixing", COL["bolt"])

    # ---- 5 controller on its thermal pad, four M3 screws
    x0, x1, y0, y1, zb, h = p["controller"]
    pad = bx(x0 + 2, x1 - 2, y0 + 2, y1 - 2, zt, zt + zb)
    ctrl = inner_box(p, "controller") + pad
    add("ctrl", "Motor controller", ctrl, 2, "bought", COL["ctrl"])

    # ---- 6 supervisor standoffs and board
    sx0, sx1, sy0, sy1, szb, sh = p["supervisor"]
    so = fuse([hexprism("z", x, y, zt + szb / 2, 5.5, szb) for x, y in p["sup_standoffs"]])
    add("standoffs", "Supervisor standoffs, 35 mm (4)", so, 14, "bought", COL["stand"])
    ex0, ex1, ey0, ey1, eh = p["economizer"]
    sup = (bx(sx0, sx1, sy0, sy1, zt + szb, zt + szb + 1.6) + bx(sx0 + 6, sx1 - 6, sy0 + 10, sy1 - 30, zt + szb + 1.6, zt + szb + sh)
           + bx(ex0, ex1, ey0, ey1, zt + szb + 1.6, zt + szb + 1.6 + eh))
    add("sup", "Safety supervisor board", sup, 3, "made", COL["sup"])

    # ---- 7 contactor on its foot
    fx0, fx1, fy0, fy1 = p["contactor_foot"]
    cont = bx(fx0, fx1, fy0, fy1, zt, zt + 3) + inner_box(p, "contactor")
    kx0, kx1, ky0 = p["contactor"][0], p["contactor"][1], p["contactor"][2]
    cont = cont + bx(kx0 + 7, kx1 - 7, ky0 - 8, ky0, zt + 30, zt + 42)
    add("cont", "Main DC contactor", cont, 4, "bought", COL["cont"])

    # ---- 8 precharge and fuse block
    add("fuse", "Precharge and fuse block", inner_box(p, "fuseblock"), 5, "bought", COL["fuse"])

    # ---- 9 connectors in the +X end wall and the speed socket in the -Y wall
    conn, xt = connector_parts(p)
    add("conns", "Motor, safety loop and command sockets", conn, 8, "bought", COL["conn"])
    add("xt90", "Power socket (XT90 in panel frame)", xt, 8, "bought", COL["xt90"])
    add("speed_socket", "Speed sensor socket (M8)", speed_socket(p), 8, "bought", COL["conn"])
    vz = zf + p["vent_z"]
    vent = xcyl(-L / 2 - 0.75, 0, vz, 10, 1.5)
    add("vent", "Membrane vent patch", vent, 8, "bought", COL["vent"])

    # ---- 10 lid gasket, lid and lid screws
    gk = (bx(-L / 2, L / 2, -W / 2, W / 2, ztop, zl) - bx(-ix, ix, -iy, iy, ztop - 1, zl + 1))
    for x, y in D["ports"]:
        sx, sy = (1 if x > 0 else -1), (1 if y > 0 else -1)
        gk = gk + zcyl(x, y, (ztop + zl) / 2, p["port_r"] + 1.5, p["gasket_t"]) + bx(x, sx * ix, y, sy * iy, ztop, zl)
        gk = gk - zcyl(x, y, (ztop + zl) / 2, 2.25, p["gasket_t"] + 2)
    add("gasket", "Lid gasket", gk, 7, "made", COL["gasket"])
    lid = bx(-L / 2, L / 2, -W / 2, W / 2, zl, zl + p["lid_t"])
    for x, y in D["ports"]:
        lid = lid - zcyl(x, y, zl + p["lid_t"] / 2, 2.25, p["lid_t"] + 2)
    add("lid", "Lid", lid, 7, "made", COL["lid"])
    ls = fuse([zcyl(x, y, zl + p["lid_t"] + 1.1, 3.8, 2.2) + zcyl(x, y, zl + p["lid_t"] - 5, 2.0, 10) for x, y in D["ports"]])
    add("lid_screws", "M4 button-head lid screws with sealing washers (4)", ls, 14, "fixing", COL["bolt"])

    # ---- 11 bench board, pads and module bolts
    bx0, bx1, by0, by1, bt = p["board"]
    board = bx(bx0, bx1, by0, by1, -bt, 0)
    for x, y in D["mounts"]:
        board = board - zcyl(x, y, -bt / 2, 3.25, bt + 2)
    for x, y in board_foot_holes(p):
        board = board - zcyl(x, y, -bt / 2, 3.3, bt + 2)
    add("board", "Bench board", board, 15, "made", COL["board"])
    pads = fuse([zcyl(x, y, p["pad_h"] / 2, p["pad_d"] / 2, p["pad_h"]) - zcyl(x, y, p["pad_h"] / 2, 3.25, p["pad_h"] + 2)
                 for x, y in D["mounts"]])
    add("pads", "Rubber isolation pads (4)", pads, 14, "bought", COL["pad"])
    mb = fuse([zcyl(x, y, -bt - 1, 6.5, 2) + hexprism("z", x, y, -bt - 4.5, 10, 4) + zcyl(x, y, -bt + (bt + zf + 9) / 2 - 2, 3.0, bt + zf + 9 - 4)
               for x, y in D["mounts"]])
    add("mount_bolts", "M6 mounting bolts with washers (4)", mb, 14, "fixing", COL["bolt"])

    # ---- 12 motor stand: uprights, feet, motor, speed ring, Hall bracket and pickup
    up, ft_, bolts = motor_stand(p)
    add("uprights", "Motor uprights (2)", up, 15, "made", COL["upright"])
    add("feet", "Upright feet (4, angle)", ft_, 15, "made", COL["foot"])
    add("stand_bolts", "Stand bolts (M6)", bolts, 15, "fixing", COL["bolt"])
    motor, axle_nuts = hub_motor(p)
    add("motor", "Reference hub motor", motor, 1, "bought", COL["motor"])
    add("axle_nuts", "Axle nuts and washers", axle_nuts, 1, "fixing", COL["bolt"])
    ring, hb, hall = speed_parts(p)
    add("ring", "Speed sensor magnet ring", ring, 12, "bought", COL["ring"])
    add("hall_bracket", "Hall pickup bracket", hb, 15, "made", COL["bracket"])
    add("hall", "Hall pickup", hall, 12, "bought", COL["hall"])

    # ---- 13 control station: posts, bar, levers, pod, e-stop
    posts, bar, levers, pod = bar_stand(p)
    add("posts", "Bar posts (2)", posts, 15, "made", COL["post"])
    add("bar", "Handlebar stub", bar, 15, "made", COL["bar"])
    add("levers", "Brake levers with switches (2)", levers, 10, "bought", COL["lever"])
    add("pod", "Key switch and throttle pod", pod, 11, "bought", COL["pod"])
    add("estop", "E-stop station", estop(p), 9, "bought", COL["estop"])

    # ---- 14 harness
    add("harness", "Wiring harness", harness(p), 13, "made", COL["harness"])
    return C


def board_foot_holes(p=PARAMS):
    """Bolt holes in the bench board for the motor upright feet and the bar post feet."""
    MX = p["motor_x"]
    g = p["upright_gap"] / 2 + p["upright"][1] + 25
    out = [(x, s * g) for x in (MX - 18, MX + 18) for s in (-1, 1)]
    pt = p["post"][1]
    out += [(x + s * (pt / 2 + 25), p["bar"][3]) for x, s in zip(p["post_x"], (-1, 1))]
    return out


def connector_holes(p=PARAMS):
    """Cutters for the end-wall and side-wall holes: {name: (cutter, (y or x, z, size text))}."""
    D = derived(p)
    L, W = p["body_l"], p["body_w"]
    cz = D["cz"]
    zf = D["z_floor"]
    out = {}
    y, w, h = p["xt90"]
    out["xt90"] = (bx(L / 2 - 5, L / 2 + 1, y - w / 2 - 0.5, y + w / 2 + 0.5, cz - h / 2 - 0.5, cz + h / 2 + 0.5)
                   + xcyl(L / 2 - 1.5, y, cz - 14.5, 1.6, 6) + xcyl(L / 2 - 1.5, y, cz + 14.5, 1.6, 6), (y, cz, "12 x 22 slot"))
    for name, yc, r in p["conns"]:
        d = 20.5 if name == "motor" else 16.5
        cut = xcyl(L / 2 - 1.5, yc, cz, d / 2, 6)
        if name != "motor":
            for dy in (-7.5, 7.5):
                for dz in (-7.5, 7.5):
                    cut = cut + xcyl(L / 2 - 1.5, yc + dy, cz + dz, 1.6, 6)
        out[name] = (cut, (yc, cz, f"{d:g} hole"))
    sx, sz = p["speed_socket"]
    out["speed"] = (ycyl(sx, -W / 2 + 1.5, zf + sz, 4.25, 6), (sx, zf + sz, "8.5 hole"))
    out["vent"] = (xcyl(-L / 2 + 1.5, 0, zf + p["vent_z"], 2.5, 6), (0, zf + p["vent_z"], "5 hole"))
    return out


def connector_parts(p=PARAMS):
    """Sockets fitted through the +X end wall: flange or frame outside, body and nut inside."""
    D = derived(p)
    L = p["body_l"]
    xo, cl = L / 2, p["conn_len"]
    cz = D["cz"]
    xi = L / 2 - p["wall"]                       # inside face of the end wall
    parts = []
    for name, yc, r in p["conns"]:
        if name == "motor":
            fl = xcyl(xo + 1.5, yc, cz, p["motor_flange"], 3)
            body = xcyl(xo + 3 + (cl - 3) / 2, yc, cz, r, cl - 3)
            rear = xcyl(xi - 9, yc, cz, r, 18)
            nut = hexprism("x", xi - 2, yc, cz, p["motor_nut_af"], 4)
            parts.append(fl + body + rear + nut)
        else:
            f = p["m12_flange"]
            fl = bx(xo, xo + 2.5, yc - f / 2, yc + f / 2, cz - f / 2, cz + f / 2)
            body = xcyl(xo + 2.5 + (cl - 2.5) / 2, yc, cz, r, cl - 2.5)
            rear = xcyl(xi - 7, yc, cz, r, 14)
            nuts = fuse([hexprism("x", xi - 1.2, yc + dy, cz + dz, 5.5, 2.4) for dy in (-7.5, 7.5) for dz in (-7.5, 7.5)])
            parts.append(fl + body + rear + nuts)
    y, w, h = p["xt90"]
    frame = bx(xo, xo + 3, y - 9, y + 9, cz - 17, cz + 17)
    plug = bx(xo + 3, xo + cl, y - w / 2, y + w / 2, cz - h / 2, cz + h / 2)
    rear = bx(xi - 16, xo, y - w / 2, y + w / 2, cz - h / 2, cz + h / 2)
    nuts = fuse([hexprism("x", xi - 1.2, y, cz + dz, 5.5, 2.4) for dz in (-14.5, 14.5)])
    return fuse(parts), frame + plug + rear + nuts


def speed_socket(p=PARAMS):
    D = derived(p)
    W = p["body_w"]
    sx, sz = p["speed_socket"]
    z = D["z_floor"] + sz
    yo, yi = -W / 2, -W / 2 + p["wall"]
    return (ycyl(sx, yo - 1, z, 6.0, 2) + ycyl(sx, yo - 2 - 5, z, 4.5, 10) + ycyl(sx, yi + 5, z, 4.0, 10)
            + hexprism("y", sx, yi + 1.5, z, 11, 3))


def motor_stand(p=PARAMS):
    MX, AZ = p["motor_x"], p["axle_z"]
    uw, ut, uh = p["upright"]
    g = p["upright_gap"] / 2
    fl, fth, flen = p["foot"]
    ups, feet, bolts = [], [], []
    for s in (-1, 1):
        y0, y1 = s * g, s * (g + ut)
        u = bx(MX - uw / 2, MX + uw / 2, min(y0, y1), max(y0, y1), 0, uh)
        slot_w = p["axle_flats"] + 0.2
        u = u - bx(MX - slot_w / 2, MX + slot_w / 2, min(y0, y1) - 1, max(y0, y1) + 1, AZ - 6, uh + 1)
        for bxp in (MX - 18, MX + 18):
            u = u - ycyl(bxp, (y0 + y1) / 2, 20, 3.3, ut + 2)
        if s < 0:
            for hx in (MX + 12, MX + 20):
                u = u - ycyl(hx, (y0 + y1) / 2, AZ, 2.2, ut + 2)
        ups.append(u)
        ya, yb = s * (g + ut), s * (g + ut + fth)       # vertical leg against the outside face
        yc = s * (g + ut + fl)
        f = bx(MX - flen / 2, MX + flen / 2, min(ya, yb), max(ya, yb), 0, fl) + \
            bx(MX - flen / 2, MX + flen / 2, min(ya, yc), max(ya, yc), 0, fth)
        for bxp in (MX - 18, MX + 18):
            f = f - ycyl(bxp, (ya + yb) / 2, 20, 3.3, fth + 2) - zcyl(bxp, s * (g + ut + 25), fth / 2, 3.3, fth + 2)
        feet.append(f)
        for bxp in (MX - 18, MX + 18):
            yy = s * (g + ut + fth)
            bolts.append(ycyl(bxp, yy + s * 2, 20, 5.0, 4) + ycyl(bxp, (s * (g - 2) + yy) / 2, 20, 2.9, abs(yy - s * (g - 2))))
            bolts.append(zcyl(bxp, s * (g + ut + 25), fth + 2, 5.0, 4) + zcyl(bxp, s * (g + ut + 25), (fth - p["board"][4]) / 2, 2.9, fth + p["board"][4]))
    return fuse(ups), fuse(feet), fuse(bolts)


def hub_motor(p=PARAMS):
    MX, AZ = p["motor_x"], p["axle_z"]
    MR, MW = p["motor_d"] / 2, p["motor_w"]
    g = p["upright_gap"] / 2 + p["upright"][1]
    shell = ycyl(MX, 0, AZ, MR, MW) + ycyl(MX, 0, AZ, MR + 6, 6)
    axle = ycyl(MX, 0, AZ, 6, 2 * (p["upright_gap"] / 2 - 1))
    fl = p["axle_flats"] / 2
    for s in (-1, 1):
        ya, yb = s * (p["upright_gap"] / 2 - 1), s * p["axle_l"] / 2
        seg = ycyl(MX, (ya + yb) / 2, AZ, 6, abs(yb - ya)) & bx(MX - fl, MX + fl, min(ya, yb), max(ya, yb), AZ - 7, AZ + 7)
        axle = axle + seg
    nuts = fuse([ycyl(MX, s * (g + 1), AZ, 10, 2) + hexprism("y", MX, s * (g + 2 + 4), AZ, 17, 8) for s in (-1, 1)])
    return shell + axle, nuts


def speed_parts(p=PARAMS):
    MX, AZ = p["motor_x"], p["axle_z"]
    MW = p["motor_w"]
    r0, r1, t = p["ring"]
    ring = ycyl(MX, -MW / 2 - t / 2, AZ, r1, t) - ycyl(MX, -MW / 2 - t / 2, AZ, r0, t + 2)
    for k in range(6):
        a = math.radians(30 + 60 * k)
        ring = ring - ycyl(MX + p["ring_pcd"] / 2 * math.cos(a), -MW / 2 - t / 2, AZ + p["ring_pcd"] / 2 * math.sin(a), 2.75, t + 2)
    hw, hd, hh = p["hall"]
    yface = -MW / 2 - t - p["hall_gap"]
    g = p["upright_gap"] / 2
    hx = MX + 34
    hall = bx(hx - hw / 2, hx + hw / 2, yface - hd, yface, AZ - hh / 2, AZ + hh / 2)
    # bracket: 20 x 3 flat bar on the inside face of the -Y upright, carrying the pickup
    hb = bx(MX + 8, MX + 50, -g, -g + 3, AZ - 10, AZ + 10)
    for hxx in (MX + 12, MX + 20):
        hb = hb - ycyl(hxx, -g + 1.5, AZ, 2.2, 5)
    return ring, hb, hall


def bar_stand(p=PARAMS):
    od, blen, bx0, by, bz = p["bar"]
    pw, pt, ph = p["post"]
    fl, fth, _ = p["foot"]
    posts = []
    for i, x in enumerate(p["post_x"]):
        s = -1 if i == 0 else 1
        post = bx(x - pt / 2, x + pt / 2, by - pw / 2, by + pw / 2, 0, ph) - xcyl(x, by, bz, 11.25, pt + 2)
        post = post - zcyl(x, by, (bz + ph) / 2, 2.1, ph - bz)          # M5 grub screw, tapped down into the bar hole
        for z in (12.0,):
            post = post - xcyl(x, by - 10, z, 3.3, pt + 2) - xcyl(x, by + 10, z, 3.3, pt + 2)
        xa, xb = x + s * pt / 2, x + s * (pt / 2 + fth)
        xc = x + s * (pt / 2 + fl)
        foot = bx(min(xa, xb), max(xa, xb), by - pw / 2, by + pw / 2, 0, fl) + bx(min(xa, xc), max(xa, xc), by - pw / 2, by + pw / 2, 0, fth)
        foot = foot - xcyl((xa + xb) / 2, by - 10, 12, 3.3, fth + 2) - xcyl((xa + xb) / 2, by + 10, 12, 3.3, fth + 2)
        foot = foot - zcyl(x + s * (pt / 2 + 25), by, fth / 2, 3.3, fth + 2)
        posts.append(post + foot)
    bar = xcyl(bx0 + blen / 2, by, bz, od / 2, blen)
    levers = []
    for i, c in enumerate(p["levers_x"]):
        s = 1 if i == 0 else -1
        clamp = bx(c - 10, c + 10, by - 18, by + 18, bz - 18, bz + 18) - xcyl(c, by, bz, od / 2, 22)
        blade = bx(min(c, c + s * 70), max(c, c + s * 70), by - 48, by - 38, bz - 5, bz + 5) + bx(c - 6, c + 6, by - 38, by - 18, bz - 5, bz + 5)
        levers.append(clamp + blade)
    x0, x1 = p["pod_x"]
    pod = bx(x0, x1, by - 20, by + 20, bz - 18, bz + 18) - xcyl((x0 + x1) / 2, by, bz, od / 2, x1 - x0 + 2)
    pod = pod + zcyl((x0 + x1) / 2, by + 8, bz + 24, 7, 12) + bx(x0 + 8, x1 - 8, by - 34, by - 20, bz - 6, bz + 6)
    return fuse(posts), bar, fuse(levers), pod


def estop(p=PARAMS):
    EX, EY = p["estop_xy"]
    e = p["estop_box"] / 2
    eh = p["estop_h"]
    return (bx(EX - e, EX + e, EY - e, EY + e, 0, eh) + zcyl(EX, EY, eh + 6, 14, 12)
            + zcyl(EX, EY, eh + 12 + 9, p["estop_head_d"] / 2, 18))


def harness_points(p=PARAMS):
    D = derived(p)
    L = p["body_l"]
    cz = D["cz"]
    xe = L / 2 + p["conn_len"]
    MX, AZ = p["motor_x"], p["axle_z"]
    g = p["upright_gap"] / 2 + p["upright"][1]
    yc = {n: y for n, y, _ in p["conns"]}
    od, blen, bx0, by, bz = p["bar"]
    EX, EY = p["estop_xy"]
    e = p["estop_box"] / 2
    sx, sz = p["speed_socket"]
    pod_c = sum(p["pod_x"]) / 2
    return {
        "motor": ([(xe, yc["motor"], cz), (xe + 22, yc["motor"], 6), (xe + 22, -125, 6), (MX, -125, 6),
                   (MX, -100, 40), (MX, -p["axle_l"] / 2 + 2, AZ - 8)], 4.0),
        "safety": ([(xe, yc["safety"], cz), (xe + 18, yc["safety"], 6), (xe + 18, EY, 6), (EX - e, EY, 6)], 3.5),
        "safety_bar": ([(EX - 10, EY - e, 6), (EX - 10, -95, 6), (205, -95, 6), (p["levers_x"][0], by - 18, bz - 14)], 3.0),
        "safety_bar2": ([(205, -95, 6), (p["levers_x"][1] - 30, -95, 6), (p["levers_x"][1], by + 18, bz - 14)], 2.5),
        "key": ([(pod_c - 25, -95, 6), (pod_c, by + 20, bz - 10)], 2.5),
        "command": ([(xe, yc["command"], cz), (xe + 12, yc["command"], 6), (xe + 12, 75, 6), (230, 75, 6),
                     (230, -80, 6), (pod_c + 5, by + 20, bz)], 3.0),
        "speed": ([(sx, -p["body_w"] / 2 - 12, D["z_floor"] + sz), (sx, -100, 6), (MX + 34, -100, 6),
                   (MX + 34, -g + 12, 6), (MX + 34, -g + 12, AZ - 12)], 2.5),
    }


def harness(p=PARAMS):
    return fuse([_path(pts, r) for pts, r in harness_points(p).values()])


# ------------------------------------------------------------------ BOM grouping and exports
NAMES = {1: "Reference hub motor, 250 W geared", 2: "Motor controller, VESC class", 3: "Safety supervisor board",
         4: "Main DC contactor", 5: "Precharge and main fuse block", 6: "Enclosure: finned tube and floor plate",
         7: "Lid and lid gasket", 8: "Connector set and vent", 9: "E-stop station, twin NC",
         10: "Brake levers with interlock switches (pair)", 11: "Key switch and throttle pod",
         12: "Independent speed sensor", 13: "Wiring harness, keyed connectors",
         14: "Pads, rivet nuts, standoffs and fixings", 15: "Bench rig (prototype only)"}
BOM_COL = {1: "#374151", 2: "#0F766E", 3: "#15803D", 4: "#C2410C", 5: "#B45309", 6: "#A8B0B8", 7: "#D1D5DB",
           8: "#1F2937", 9: "#D4A017", 10: "#2563EB", 11: "#7C3AED", 12: "#0EA5E9", 13: "#111827", 14: "#4B5563",
           15: "#D6C3A1"}
EXPLODE = {1: (-60, -260, 120), 2: (0, -40, 160), 3: (0, 0, 250), 4: (40, -20, 170), 5: (110, 40, 110),
           6: (0, 0, 0), 7: (-150, 60, 330), 8: (170, 0, 30), 9: (60, 90, 40), 10: (-40, -170, 40),
           11: (60, -190, 110), 12: (60, -300, 120), 13: (0, 160, 0), 14: (-90, -90, -30), 15: (0, 0, -140)}
MODULE_ITEMS = (2, 3, 4, 5, 6, 7, 8, 14)


def build_parts(p=PARAMS):
    """Return a list of (name, shape, colour, bom_item, explode_offset), one per BOM line.
    Used by the concept media. Fixings are grouped with their BOM line."""
    C = build_components(p)
    groups = {}
    for k, c in C.items():
        if c.bom is None:
            continue
        if c.bom == 14 and k in ("mount_bolts",):
            continue
        groups.setdefault(c.bom, []).append(c.shape)
    return [(NAMES[n], fuse(groups[n]), BOM_COL[n], n, EXPLODE[n]) for n in sorted(groups)]


def assemblies(parts=None):
    from build123d import Compound
    C = build_components()
    module_keys = [k for k, c in C.items() if c.bom in MODULE_ITEMS and k not in ("mount_bolts", "standoffs") or k in ("standoffs",)]
    module_keys = [k for k in module_keys if C[k].bom in MODULE_ITEMS]
    return {
        "motioncore-module": Compound([C[k].shape for k in module_keys if k != "mount_bolts"]),
        "motioncore-enclosure": Compound([C[k].shape for k in ("floor", "tube", "gasket", "lid")]),
        "motioncore-kit": Compound([c.shape for c in C.values()]),
    }


# ------------------------------------------------------------------ constructability checks
def _vol(a, c):
    try:
        s = a & c
        return s.volume if s is not None else 0.0
    except Exception:
        return float("nan")


def _gap(a, c):
    return a.distance_to(c)


def checks(p=PARAMS):
    """Pairs that must touch, and pairs that must stay apart by a clearance (mm).
    Returns a list of (description, overlap mm3, gap mm, expectation, ok)."""
    C = build_components(p)
    S = lambda k: C[k].shape  # noqa: E731
    rows = []

    def chk(desc, a, c, expect):
        v = _vol(a, c)
        gp = _gap(a, c)
        if expect == "touch":
            ok = v < 1e-2 and gp < 0.05
        elif expect == "fit":
            ok = v < 1e-2 and gp < 0.5
        else:
            ok = v < 1e-2 and gp >= expect - 1e-6
        rows.append((desc, v, gp, expect, ok))

    # enclosure
    chk("Tube on the floor plate (sealant joint)", S("tube"), S("floor"), "touch")
    chk("Rivet nuts set in the floor plate", S("rivnuts"), S("floor"), "touch")
    chk("Rivet nuts clear of the tube", S("rivnuts"), S("tube"), 3.0)
    chk("Floor screws in the corner ports", S("floor_screws"), S("tube"), "touch")
    chk("Gasket on the tube", S("gasket"), S("tube"), "touch")
    chk("Lid on the gasket", S("lid"), S("gasket"), "touch")
    chk("Lid screws in the lid", S("lid_screws"), S("lid"), "touch")
    # internals on the floor and clear of everything else
    inside = ("ctrl", "standoffs", "sup", "cont", "fuse")
    chk("Controller on the floor plate (thermal pad)", S("ctrl"), S("floor"), "touch")
    chk("Standoffs on the floor plate", S("standoffs"), S("floor"), "touch")
    chk("Supervisor board on its standoffs", S("sup"), S("standoffs"), "touch")
    chk("Contactor foot on the floor plate", S("cont"), S("floor"), "touch")
    chk("Fuse block on the floor plate", S("fuse"), S("floor"), "touch")
    chk("Supervisor standoffs clear of the controller", S("standoffs"), S("ctrl"), 3.0)
    chk("Supervisor board clear of the controller", S("sup"), S("ctrl"), 5.0)
    D_ = derived(p)
    ex0, ex1, ey0, ey1, eh = p["economizer"]
    szb_ = p["supervisor"][4]
    econ = bx(ex0, ex1, ey0, ey1, D_["z_tube"] + szb_ + 1.6, D_["z_tube"] + szb_ + 1.6 + eh)
    sx0_, sx1_, sy0_, sy1_ = p["supervisor"][:4]
    board_ = bx(sx0_, sx1_, sy0_, sy1_, D_["z_tube"] + szb_, D_["z_tube"] + szb_ + 1.6)
    chk("Coil economizer module sits on the carrier board", econ, board_, "touch")
    chk("Coil economizer module clear of the tube walls", econ, S("tube"), 5.0)
    chk("Coil economizer module clear of the lid", econ, S("lid") + S("gasket"), 5.0)
    chk("Coil economizer module clear of the contactor", econ, S("cont"), 5.0)
    chk("Coil economizer module clear of the standoffs", econ, S("standoffs"), 3.0)
    for i, a in enumerate(("ctrl", "sup", "cont", "fuse")):
        chk(f"{C[a].name} clear of the tube walls", S(a), S("tube"), 3.0)
        chk(f"{C[a].name} clear of the lid", S(a), S("lid") + S("gasket"), 5.0)
        chk(f"{C[a].name} clear of the rivet nuts", S(a), S("rivnuts"), 3.0)
        for c2 in ("ctrl", "sup", "cont", "fuse")[i + 1:]:
            chk(f"{C[a].name} clear of the {C[c2].name.lower()}", S(a), S(c2), 5.0)
    chk("Standoffs clear of the rivet nuts", S("standoffs"), S("rivnuts"), 2.0)
    # connectors
    for k in ("conns", "xt90", "speed_socket", "vent"):
        chk(f"{C[k].name} fitted in its wall", S(k), S("tube"), "touch")
        for a in inside:
            chk(f"{C[k].name} clear of the {C[a].name.lower()}", S(k), S(a), 3.0)
        chk(f"{C[k].name} clear of the rivet nuts", S(k), S("rivnuts"), 2.0)
        chk(f"{C[k].name} clear of the lid", S(k), S("lid") + S("gasket"), 2.0)
    chk("XT90 frame clear of the other sockets", S("xt90"), S("conns"), 3.0)
    chk("Speed socket clear of the floor screws", S("speed_socket"), S("floor_screws"), 3.0)
    # mounting
    chk("Pads under the rivet nut flanges", S("pads"), S("rivnuts"), "touch")
    chk("Pads on the bench board", S("pads"), S("board"), "touch")
    chk("Mounting bolts in the rivet nuts", S("mount_bolts"), S("rivnuts"), "touch")
    chk("Floor plate clear of the board (pads take the load)", S("floor"), S("board"), 3.0)
    # motor stand
    chk("Uprights on the board", S("uprights"), S("board"), "touch")
    chk("Feet on the board", S("feet"), S("board"), "touch")
    chk("Feet against the uprights", S("feet"), S("uprights"), "touch")
    chk("Axle flats in the upright slots", S("motor"), S("uprights"), "touch")
    chk("Axle nuts against the uprights", S("axle_nuts"), S("uprights"), "touch")
    chk("Motor shell clear of the board", S("motor") - S("uprights"), S("board"), 15.0)
    chk("Magnet ring on the motor side cover", S("ring"), S("motor"), "touch")
    chk("Hall bracket on the upright", S("hall_bracket"), S("uprights"), "touch")
    chk("Hall pickup on its bracket", S("hall"), S("hall_bracket"), "touch")
    chk("Hall pickup to magnet ring (sensing gap)", S("hall"), S("ring"), p["hall_gap"] - 0.01)
    chk("Hall pickup clear of the motor shell", S("hall"), S("motor"), 3.0)
    chk("Ring clear of the uprights", S("ring"), S("uprights"), 5.0)
    chk("Motor clear of the feet", S("motor"), S("feet"), 10.0)
    # control station
    chk("Posts on the board", S("posts"), S("board"), "touch")
    chk("Stand bolts through the board holes (clearance)", S("stand_bolts"), S("board"), "fit")
    chk("Handlebar through the post holes (sliding fit)", S("bar"), S("posts"), "fit")
    chk("Brake levers clamped on the bar", S("levers"), S("bar"), "touch")
    chk("Pod clamped on the bar", S("pod"), S("bar"), "touch")
    chk("Brake levers clear of the pod", S("levers"), S("pod"), 5.0)
    chk("Brake levers clear of the posts", S("levers"), S("posts"), 5.0)
    chk("Brake levers clear of the board", S("levers"), S("board"), 20.0)
    chk("E-stop station on the board", S("estop"), S("board"), "touch")
    # layout: nothing on the board overlaps anything else
    big = ("tube", "lid", "estop", "posts", "uprights", "feet", "motor")
    for i, a in enumerate(big):
        for c2 in big[i + 1:]:
            if {a, c2} in ({"uprights", "feet"}, {"uprights", "motor"}, {"tube", "lid"}):
                continue
            chk(f"{C[a].name} clear of the {C[c2].name.lower()}", S(a), S(c2), 10.0)
    return rows


def print_checks(p=PARAMS):
    rows = checks(p)
    bad = 0
    for desc, v, gp, exp, ok in rows:
        e = exp if exp in ("touch", "fit") else f">= {exp:g} mm"
        print(f"  {'ok ' if ok else 'BAD'}  {desc:64s} overlap {v:8.3f} mm3  gap {gp:7.2f} mm  ({e})")
        bad += not ok
    print(f"constructability checks: {len(rows) - bad} of {len(rows)} pass")
    return bad


def masses(p=PARAMS):
    """Volumes (mm3) of the made aluminium parts of the module, from the solids."""
    C = build_components(p)
    return {k: C[k].shape.volume for k in ("floor", "tube", "lid", "gasket")}


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(1 if print_checks() else 0)
    from build123d import export_step, export_stl
    root = Path(__file__).resolve().parents[1]
    (root / "step").mkdir(exist_ok=True); (root / "stl").mkdir(exist_ok=True)
    for name, shape in assemblies().items():
        export_step(shape, str(root / "step" / f"{name}.step"))
        export_stl(shape, str(root / "stl" / f"{name}.stl"), tolerance=0.2, angular_tolerance=0.3)
        bb = shape.bounding_box()
        print(f"{name}: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm")
    print("module envelope from parameters: %.1f x %.0f x %.0f mm" % envelope())
    print("aluminium volumes, mm3:", {k: round(v) for k, v in masses().items()})
    print_checks()
