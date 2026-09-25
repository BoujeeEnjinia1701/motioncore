"""MotionCore concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

The reference kit is shown laid out on a workbench: the drive and safety module
(finned enclosure with controller, safety supervisor, contactor and precharge inside),
a 250 W geared hub motor, the e-stop station, brake interlock switches, the key and
throttle pod, the independent speed sensor and the harness. Coordinates in mm,
bench top at Z = 0, module centered on the origin.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Pos, Rot, Solid, Plane, Vector
from concept import Part, render_all

# Module enclosure, outside dimensions (body 220 x 140 mm; about 250 x 170 x 66 mm with fins, lid and connectors)
L, W, H, T = 220.0, 140.0, 60.0, 4.0


def box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def tube3(a, b, r):
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def path(points, r=5.0):
    s = None
    for a, b in zip(points, points[1:]):
        t = tube3(a, b, r)
        s = t if s is None else s + t
    return s


# 6 Enclosure body: extruded aluminum box with heat-sink fins on both long sides
body = box(-L / 2, L / 2, -W / 2, W / 2, 0, H) - box(-L / 2 + T, L / 2 - T, -W / 2 + T, W / 2 - T, T, H + 1)
for x in range(-95, 100, 19):
    for s in (-1, 1):
        y0 = s * W / 2
        body = body + box(x - 2.5, x + 2.5, min(y0, y0 + s * 14), max(y0, y0 + s * 14), 6, H - 6)

# 7 Lid with gasket lip
lid = box(-L / 2, L / 2, -W / 2, W / 2, H, H + 6)

# 2 Motor controller (VESC class, 75 V MOSFET stage) on the floor, thermal pad to the body
controller = box(-100, 0, -35, 25, T, T + 25)
# 3 Safety supervisor board on standoffs above the controller
supervisor = box(-95, -10, -30, 30, 38, 48)
for x in (-88, -17):
    for y in (-23, 23):
        supervisor = supervisor + box(x - 3, x + 3, y - 3, y + 3, T + 25, 38)
# 4 Main DC contactor (60 V class, 100 A continuous), coil in the e-stop loop
contactor = box(15, 65, -22, 22, T, T + 48) + box(22, 58, -30, -22, T + 30, T + 42)
# 5 Precharge resistor and main fuse block
fuseblock = box(72, 102, -26, 26, T, T + 22)

# 8 Connector panel on the +X end: power in, motor phases, sensor, safety loop, command
PX = L / 2
panel = box(PX, PX + 5, -52, 52, 8, 52)
for y, r in ((-36, 9), (-12, 8), (12, 7), (36, 7)):
    panel = panel + Pos(PX + 5 + 9, y, 30) * Rot(0, 90, 0) * Cylinder(r, 18)

# 1 Reference hub motor: 250 W geared, about 190 mm diameter, standing on its rim, axle along Y
MX, MR, MW = -380.0, 95.0, 90.0
motor = (Pos(MX, 0, MR) * Rot(90, 0, 0) * Cylinder(MR, MW)
         + Pos(MX, 0, MR) * Rot(90, 0, 0) * Cylinder(MR + 6, 6)
         + Pos(MX, 0, MR) * Rot(90, 0, 0) * Cylinder(6, MW + 90))

# 12 Independent speed sensor: magnet ring on the motor side face plus Hall pickup
ring = Pos(MX, -MW / 2 - 4, MR) * Rot(90, 0, 0) * (Cylinder(40, 5) - Cylinder(18, 6))
hall = box(MX + 44, MX + 64, -MW / 2 - 16, -MW / 2 - 2, MR - 10, MR + 10)
speed = ring + hall

# 9 E-stop station: yellow box, red mushroom head, twin NC contact blocks
EX, EY = 300.0, 150.0
estop_box = box(EX - 38, EX + 38, EY - 38, EY + 38, 0, 62)
estop_head = Pos(EX, EY, 62 + 6) * Cylinder(14, 12) + Pos(EX, EY, 62 + 12 + 9) * Cylinder(24, 18)

# 10 Brake interlock switches (pair), lever-clamp style
brakes = (box(250, 300, -170, -150, 0, 22) + box(290, 330, -165, -155, 22, 30)
          + box(360, 410, -170, -150, 0, 22) + box(400, 440, -165, -155, 22, 30))

# 11 Key switch and throttle pod (command input)
pod = box(320, 380, -40, 0, 0, 34) + Pos(335, -20, 34 + 6) * Cylinder(8, 12) + box(360, 395, -30, -10, 10, 24)

# 13 Wiring harness from the connector panel to each device
harness = (path([(PX + 32, -36, 30), (200, -36, 8), (200, -90, 8), (MX + 120, -150, 8), (MX, -150, 8), (MX, -60, MR - 40)], 6)
           + path([(PX + 32, 12, 30), (200, 40, 8), (EX - 38, EY - 10, 8)], 4)
           + path([(PX + 32, 36, 30), (240, 60, 8), (320, 20, 8), (350, 0, 8)], 4)
           + path([(PX + 32, -12, 30), (220, -60, 8), (275, -145, 8)], 3.5)
           + path([(275, -150, 6), (385, -150, 6)], 3.5)
           + path([(MX + 54, -MW / 2 - 16, MR - 10), (MX + 90, -120, 8)], 3))

parts = [
    Part("Reference hub motor, 250 W geared", motor, "#374151", 1, (60, -380, -120)),
    Part("Motor controller, VESC class", controller, "#0F766E", 2, (0, -40, 160)),
    Part("Safety supervisor board", supervisor, "#15803D", 3, (0, 0, 250)),
    Part("Main DC contactor", contactor, "#C2410C", 4, (40, -20, 170)),
    Part("Precharge and main fuse block", fuseblock, "#B45309", 5, (110, 20, 110)),
    Part("Enclosure body, finned aluminum", body, "#A8B0B8", 6, (0, 0, -60)),
    Part("Enclosure lid", lid, "#D1D5DB", 7, (-150, 60, 330)),
    Part("Connector panel, keyed", panel, "#1F2937", 8, (110, 0, 0)),
    Part("E-stop station, twin NC", estop_box + estop_head, "#D4A017", 9, (60, 90, 0)),
    Part("Brake interlock switches (pair)", brakes, "#2563EB", 10, (40, -90, 0)),
    Part("Key switch and throttle pod", pod, "#7C3AED", 11, (140, -30, 0)),
    Part("Independent speed sensor", speed, "#0EA5E9", 12, (60, -600, -120)),
    Part("Wiring harness, keyed connectors", harness, "#111827", 13, (0, 0, -40)),
]

# Context for scale: bench top and a phone lying next to the kit
bench = box(-560, 520, -260, 280, -30, 0)
phone = box(-60, 15, -250, -175, 0, 9)
context = [Part("Bench top", bench, "#C8CDD3"), Part("phone", phone, "#6B7280")]

render_all(
    parts, project="MotionCore", title="Drive and safety module concept", dwg_no="MTC-DWG-010",
    key_figures=["Input 20 to 58 V DC: 24, 36 and 48 V packs incl. SwapCell",
                 "250 W continuous reference; 500 W option (thermal at risk)",
                 "Hardwired twin-channel e-stop opens contactor, <100 ms (est.)",
                 "Speed limit twice: controller plus independent supervisor",
                 "Module about 250 x 170 x 66 mm, about 1.3 kg (est.)",
                 "Reference kit about $325 in parts (indicative)"],
    scale_figure=False, context=context,
    cut_exclude=("Reference hub motor, 250 W geared", "E-stop station, twin NC", "Brake interlock switches (pair)",
                 "Key switch and throttle pod", "Independent speed sensor", "Wiring harness, keyed connectors",
                 "Connector panel, keyed"),
    flow={"title": "power flow at 250 W rated output, 48 V pack, W (all values are estimates)", "unit": "W",
          "stages": [("Pack output", 333), ("Controller input", 328), ("Controller output", 312),
                     ("Motor shaft", 250)],
          "losses": [(0, "Supervisor, wiring (est.)", 5), (1, "Controller loss (est.)", 16),
                     (2, "Motor and gear loss (est.)", 62)]},
)
