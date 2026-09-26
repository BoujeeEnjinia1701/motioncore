"""MotionCore parametric model (build123d), TRL 3.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl and prints the main envelopes.

Massing-plus detail: correct interfaces (connector panel with the four interface v0.1
connectors, host mounting pattern, heat-sink fins) and main dimensions of the drive and
safety module, plus the reference kit devices laid out on a bench. Not fabrication detail.

Axes: X along the module length (connector panel on the +X end), Y across the fins,
Z up. Units mm. Bench top at Z = 0; the module stands on four isolation pads.
The module is centered on the origin in X and Y so that the kit's cutaway cuts through it.
"""
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # Enclosure body (MTC-PRC-001 v0.3, R12)
    "body_l": 220.0, "body_w": 140.0, "body_h": 60.0, "wall": 3.0,
    "lid_t": 3.0,               # lid plate; a 3 mm gasket lip sits inside the body
    "fin_n": 11, "fin_pitch": 19.0, "fin_t": 4.0, "fin_depth": 14.0,
    "fin_z0": 6.0, "fin_z1": 54.0,          # fin span, measured from the body underside
    # Host mounting interface: four M6 inserts in the floor on isolation pads
    "mount_px": 180.0, "mount_py": 100.0, "pad_d": 16.0, "pad_h": 3.0,
    # Connector panel on the +X end (interface v0.1)
    "panel_t": 5.0, "panel_w": 104.0, "panel_z0": 8.0, "panel_z1": 52.0,
    "conn_len": 18.0, "conn_z": 30.0,
    # (name, y position, radius) for round connectors; XT90 is modeled as a block
    "xt90": (-36.0, 22.0, 12.0),             # y, width (Y), height (Z)
    "conns": [("motor", -12.0, 8.0), ("safety", 12.0, 8.0), ("command", 36.0, 8.0)],
    # Internal envelopes (x0, x1, y0, y1, z0 above the floor, height)
    "controller": (-100.0, 0.0, -35.0, 25.0, 0.0, 25.0),   # VESC class, 75 V stage
    "supervisor": (-95.0, -10.0, -30.0, 30.0, 34.0, 10.0),  # on standoffs above the controller
    "contactor": (15.0, 65.0, -22.0, 22.0, 0.0, 48.0),     # 100 A sealed DC contactor
    "fuseblock": (72.0, 102.0, -26.0, 26.0, 0.0, 22.0),    # precharge resistor, bypass, main fuse
    # Reference kit devices on the bench
    "motor_x": -380.0, "motor_d": 190.0, "motor_w": 90.0, "axle_l": 180.0,
    "estop_xy": (300.0, 150.0), "estop_box": 76.0, "estop_h": 62.0, "estop_head_d": 48.0,
}


def _box(x0, x1, y0, y1, z0, z1):
    from build123d import Box, Pos
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def _tube(a, b, r):
    from build123d import Plane, Solid, Vector
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def _path(points, r):
    s = None
    for a, b in zip(points, points[1:]):
        t = _tube(a, b, r)
        s = t if s is None else s + t
    return s


def envelope(p=PARAMS):
    """Overall module envelope (length, width, height) in mm, from the parameters alone."""
    length = p["body_l"] + p["panel_t"] + p["conn_len"]
    width = p["body_w"] + 2 * p["fin_depth"]
    height = p["pad_h"] + p["body_h"] + p["lid_t"]
    return length, width, height


def build_parts(p=PARAMS):
    """Return a list of (name, shape, colour, bom_item, explode_offset)."""
    from build123d import Cylinder, Pos, Rot
    b = _box
    L, W, H, T = p["body_l"], p["body_w"], p["body_h"], p["wall"]
    z0 = p["pad_h"]                       # body underside
    fl = z0 + T                           # inside floor

    # 6 Enclosure body: extruded aluminum box, fins on both long sides, M6 bosses in the floor
    body = b(-L / 2, L / 2, -W / 2, W / 2, z0, z0 + H) - b(-L / 2 + T, L / 2 - T, -W / 2 + T, W / 2 - T, fl, z0 + H + 1)
    n, pitch = p["fin_n"], p["fin_pitch"]
    for i in range(n):
        x = (i - (n - 1) / 2) * pitch
        for s in (-1, 1):
            y0 = s * W / 2
            y1 = y0 + s * p["fin_depth"]
            body = body + b(x - p["fin_t"] / 2, x + p["fin_t"] / 2, min(y0, y1), max(y0, y1),
                            z0 + p["fin_z0"], z0 + p["fin_z1"])
    mx, my = p["mount_px"] / 2, p["mount_py"] / 2
    for sx in (-1, 1):
        for sy in (-1, 1):
            body = body + Pos(sx * mx, sy * my, fl + 4) * Cylinder(6, 8)
            body = body - Pos(sx * mx, sy * my, z0 + 5) * Cylinder(2.5, 12)     # M6 insert bore
    # Isolation pads under the mounting points (host interface)
    pads = None
    for sx in (-1, 1):
        for sy in (-1, 1):
            c = Pos(sx * mx, sy * my, z0 / 2) * Cylinder(p["pad_d"] / 2, z0)
            pads = c if pads is None else pads + c

    # 7 Lid with gasket lip
    top = z0 + H
    lid = b(-L / 2, L / 2, -W / 2, W / 2, top, top + p["lid_t"]) + b(-L / 2 + T + 1, L / 2 - T - 1, -W / 2 + T + 1,
                                                                     W / 2 - T - 1, top - 3, top)

    def inner(key):
        x0, x1, y0, y1, zb, h = p[key]
        return b(x0, x1, y0, y1, fl + zb, fl + zb + h)

    # 2 Motor controller on the floor, thermal pad to the body
    controller = inner("controller")
    # 3 Safety supervisor board on four standoffs
    sx0, sx1, sy0, sy1, szb, sh = p["supervisor"]
    supervisor = inner("supervisor")
    for x in (sx0 + 7, sx1 - 7):
        for y in (sy0 + 7, sy1 - 7):
            supervisor = supervisor + b(x - 3, x + 3, y - 3, y + 3, fl, fl + szb)
    # 4 Main DC contactor with its terminal bosses
    contactor = inner("contactor")
    cx0, cx1, cy0 = p["contactor"][0], p["contactor"][1], p["contactor"][2]
    contactor = contactor + b(cx0 + 7, cx1 - 7, cy0 - 8, cy0, fl + 30, fl + 42)
    # 5 Precharge resistor, bypass and main fuse block
    fuseblock = inner("fuseblock")

    # 8 Connector panel on the +X end: XT90 power in, motor plug, M12 safety loop, M12 command
    PX = L / 2
    pt, cl, cz = p["panel_t"], p["conn_len"], z0 + p["conn_z"]
    panel = b(PX, PX + pt, -p["panel_w"] / 2, p["panel_w"] / 2, z0 + p["panel_z0"], z0 + p["panel_z1"])
    y, w, h = p["xt90"]
    panel = panel + b(PX + pt, PX + pt + cl, y - w / 2, y + w / 2, cz - h / 2, cz + h / 2)
    for _, yc, r in p["conns"]:
        panel = panel + Pos(PX + pt + cl / 2, yc, cz) * Rot(0, 90, 0) * Cylinder(r, cl)

    # 1 Reference hub motor: 250 W geared, standing on its rim, axle along Y
    MX, MR, MW = p["motor_x"], p["motor_d"] / 2, p["motor_w"]
    motor = (Pos(MX, 0, MR) * Rot(90, 0, 0) * Cylinder(MR, MW)
             + Pos(MX, 0, MR) * Rot(90, 0, 0) * Cylinder(MR + 6, 6)
             + Pos(MX, 0, MR) * Rot(90, 0, 0) * Cylinder(6, p["axle_l"]))
    # 12 Independent speed sensor: magnet ring on the hub shell plus Hall pickup
    ring = Pos(MX, -MW / 2 - 4, MR) * Rot(90, 0, 0) * (Cylinder(40, 5) - Cylinder(18, 6))
    hall = b(MX + 44, MX + 64, -MW / 2 - 16, -MW / 2 - 2, MR - 10, MR + 10)
    speed = ring + hall

    # 9 E-stop station: yellow box, red mushroom head, twin NC contact blocks
    EX, EY = p["estop_xy"]
    e = p["estop_box"] / 2
    eh = p["estop_h"]
    estop = (b(EX - e, EX + e, EY - e, EY + e, 0, eh) + Pos(EX, EY, eh + 6) * Cylinder(14, 12)
             + Pos(EX, EY, eh + 12 + 9) * Cylinder(p["estop_head_d"] / 2, 18))
    # 10 Brake interlock switches (pair), lever-clamp style
    brakes = (b(250, 300, -170, -150, 0, 22) + b(290, 330, -165, -155, 22, 30)
              + b(360, 410, -170, -150, 0, 22) + b(400, 440, -165, -155, 22, 30))
    # 11 Key switch and throttle pod
    pod = b(320, 380, -40, 0, 0, 34) + Pos(335, -20, 40) * Cylinder(8, 12) + b(360, 395, -30, -10, 10, 24)
    # 13 Wiring harness from the connector panel to each device
    xe = PX + pt + cl
    harness = (_path([(xe, -36, cz), (200, -36, 8), (200, -90, 8), (MX + 120, -150, 8), (MX, -150, 8),
                      (MX, -60, MR - 40)], 6)
               + _path([(xe, 12, cz), (200, 40, 8), (EX - e, EY - 10, 8)], 4)
               + _path([(xe, 36, cz), (240, 60, 8), (320, 20, 8), (350, 0, 8)], 4)
               + _path([(xe, -12, cz), (220, -60, 8), (275, -145, 8)], 3.5)
               + _path([(275, -150, 6), (385, -150, 6)], 3.5)
               + _path([(MX + 54, -MW / 2 - 16, MR - 10), (MX + 90, -120, 8)], 3))

    return [
        ("Reference hub motor, 250 W geared", motor, "#374151", 1, (60, -380, -120)),
        ("Motor controller, VESC class", controller, "#0F766E", 2, (0, -40, 160)),
        ("Safety supervisor board", supervisor, "#15803D", 3, (0, 0, 250)),
        ("Main DC contactor", contactor, "#C2410C", 4, (40, -20, 170)),
        ("Precharge and main fuse block", fuseblock, "#B45309", 5, (110, 20, 110)),
        ("Enclosure body, finned aluminum", body, "#A8B0B8", 6, (0, 0, -60)),
        ("Enclosure lid", lid, "#D1D5DB", 7, (-150, 60, 330)),
        ("Connector panel, keyed", panel, "#1F2937", 8, (110, 0, 0)),
        ("E-stop station, twin NC", estop, "#D4A017", 9, (60, 90, 0)),
        ("Brake interlock switches (pair)", brakes, "#2563EB", 10, (40, -90, 0)),
        ("Key switch and throttle pod", pod, "#7C3AED", 11, (140, -30, 0)),
        ("Independent speed sensor", speed, "#0EA5E9", 12, (60, -600, -120)),
        ("Wiring harness, keyed connectors", harness, "#111827", 13, (0, 0, -40)),
        ("Isolation pads and mounting hardware", pads, "#4B5563", 14, (0, 0, -90)),
    ]


MODULE_ITEMS = (2, 3, 4, 5, 6, 7, 8, 14)


def assemblies(parts=None):
    from build123d import Compound
    parts = parts or build_parts()
    by = {bom: s for _, s, _, bom, _ in parts if bom}
    return {
        "motioncore-module": Compound([by[i] for i in MODULE_ITEMS]),
        "motioncore-enclosure": Compound([by[6], by[7], by[8]]),
        "motioncore-kit": Compound([s for _, s, _, _, _ in parts]),
    }


if __name__ == "__main__":
    from build123d import export_step, export_stl
    root = Path(__file__).resolve().parents[1]
    (root / "step").mkdir(exist_ok=True); (root / "stl").mkdir(exist_ok=True)
    parts = build_parts()
    for name, shape in assemblies(parts).items():
        export_step(shape, str(root / "step" / f"{name}.step"))
        export_stl(shape, str(root / "stl" / f"{name}.stl"))
        bb = shape.bounding_box()
        print(f"{name}: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm")
    print("module envelope from parameters: %.0f x %.0f x %.0f mm" % envelope())
