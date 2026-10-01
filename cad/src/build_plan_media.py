"""MotionCore prototype build plan pictures (MTC-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|layouts|joints|steps|wiring ...]
With no argument it draws everything. Every picture is drawn from cad/src/model.py
(build_components), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/MTC-DWG-101 to 110        making sketches for the made components
    docs/05-build-plan/floor-holes.png     floor plate hole positions
    docs/05-build-plan/wall-holes.png      end wall and side wall hole positions on the finned tube
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
    docs/05-build-plan/wiring.png          block-level wiring with wire sizes (matplotlib)
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from model import PARAMS as P, build_components, derived, floor_holes, connector_holes, bx, fuse  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-01"
D = derived(P)
C = build_components(P)
L, W = P["body_l"], P["body_w"]


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def S(*keys):
    return fuse([C[k].shape for k in keys])


def pc(key, name=None, explode=(0, 0, 0)):
    c = C[key]
    return part(name or c.name, c.shape, c.color, explode)


def mv(p, e):
    return Part(p.name, p.shape, p.color, None, tuple(e), p.alpha)


# ----------------------------------------------------------------- overview
def overview():
    order = [("floor", "Floor plate", (0, 0, 90)), ("rivnuts", "Rivet nuts (4)", (0, 0, 50)),
             ("tube", "Finned tube", (0, 0, 230)), ("conns", "Sockets: motor, safety loop, command", (120, 20, 230)),
             ("xt90", "Power socket (XT90 in its frame)", (140, -90, 320)), ("ctrl", "Motor controller", (0, 0, 140)),
             ("cont", "Contactor", (0, 0, 150)), ("fuse", "Precharge and fuse block", (0, 60, 150)),
             ("standoffs", "Supervisor standoffs (4)", (0, 0, 330)), ("sup", "Supervisor board", (0, 0, 410)),
             ("gasket", "Lid gasket", (0, 0, 470)), ("lid", "Lid", (0, 0, 520)), ("pads", "Rubber pads (4)", (-70, -60, 0)),
             ("board", "Bench board", (0, 0, -60)), ("uprights", "Motor uprights (2)", (0, 0, 0)),
             ("feet", "Upright feet (2)", (0, 0, -50)), ("ring", "Magnet ring", (0, -150, 180)),
             ("motor", "Reference hub motor", (0, 0, 220)), ("hall_bracket", "Hall bracket and pickup", (0, -150, 0)),
             ("posts", "Bar posts with feet (2)", (0, -40, 0)), ("bar", "Handlebar stub", (0, -120, 20)),
             ("levers", "Brake levers (2)", (0, -200, 30)), ("pod", "Key and throttle pod", (0, -200, 30)),
             ("estop", "E-stop station", (60, 120, 60)), ("harness", "Wiring harness", (220, 120, 0))]
    parts = []
    for k, n, e in order:
        sh = C[k].shape if k != "hall_bracket" else S("hall_bracket", "hall")
        parts.append(part(n, sh, C[k].color, e))
    return bv.overview(parts, OUT / "overview.png", "MotionCore prototype: every component, pulled apart",
                       subtitle="Numbered in build order: the module (1 to 12), the bench rig and devices (13 to 25). "
                                "Seen from the connector end and above", elev=30, azim=-55, size=(12, 8), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
def sheets():
    import build123d as b
    base = dict(project="MotionCore", date=DATE)
    out = []
    zf, zt = D["z_floor"], D["z_tube"]
    module_ctx = [pc("tube"), pc("rivnuts"), pc("pads")]

    out.append(bv.component_sheet(
        pc("floor"), module_ctx, dwg_no="MTC-DWG-101", title="MotionCore floor plate: making sketch",
        material="Aluminum plate 3 mm, 6061-T6", view_shape=b.Pos(0, 0, -zf) * C["floor"].shape, inset_view=(-35, -60),
        notes=["Cut 220 x 140 mm from 3 mm 6061 plate; square, deburr, corners left square.",
               "Mark from the far end (opposite the sockets) and the socket side;",
               "  the floor holes picture gives every position.",
               "Rivet nut holes 9.0 mm at 20 and 200 from the far end, 20 and 120",
               "  from the socket side (the 180 x 100 mounting pattern).",
               "Corner screw holes 4.5 mm, 7.5 from each edge; countersink from",
               "  below to 8.4 mm so the M4 heads sit flush.",
               "Tapped holes through the plate: M3 (2.5 drill) for the controller (4)",
               "  and the supervisor standoffs (4); M4 (3.3 drill) for the contactor",
               "  foot (2) and the fuse block (2).",
               "Fit: the tube sits on its top face on a film of thermally conductive",
               "  sealant; four M4 countersunk screws go up into the corner ports.",
               "Check: lay the tube on it; the four corner holes line up with the ports."],
        **base))

    tube = C["tube"].shape
    out.append(bv.component_sheet(
        pc("tube"), [pc("floor"), pc("lid"), pc("conns"), pc("xt90")], dwg_no="MTC-DWG-102",
        title="MotionCore finned tube: making sketch", material="Bought finned enclosure extrusion, 220 x 140 mm, 3 mm walls",
        view_shape=b.Pos(0, 0, -zt) * tube, inset_view=(28, -40),
        notes=["Cut 56 mm off the extrusion, square to its length, so the fins stand",
               "  upright. Face both cut ends flat; deburr; keep the ports clean.",
               "The four corner ports are part of the extrusion; tap them M4 from",
               "  both ends, 12 mm deep (they take the floor and lid screws).",
               "Connector end wall (short wall, holes 28.5 above the bottom edge,",
               "  measured from the socket side's outer face): XT90 slot 12 x 22 at",
               "  28 with two 3.2 holes 14.5 above and below; motor 20.5 hole at 56;",
               "  safety loop 16.5 hole at 83 and command 16.5 hole at 109, each with",
               "  four 3.2 holes on a 15 mm square.",
               "Socket side: speed socket 8.5 hole between the 1st and 2nd fins from",
               "  the far end, 24.5 from that end, 18 above the bottom edge.",
               "Far end wall: vent hole 5 mm on the centre line, 43 above the bottom.",
               "Check: each socket seats flat; nothing fouls a port or a fin."],
        **base))

    sx0, sx1, sy0, sy1, szb, _ = P["supervisor"]
    pcb = bx(sx0, sx1, sy0, sy1, zt + szb, zt + szb + 1.6)
    for x, y in P["sup_standoffs"]:
        pcb = pcb - b.Pos(x, y, zt + szb + 0.8) * b.Cylinder(1.6, 4)
    sup = pcb
    out.append(bv.component_sheet(
        pc("sup", "Supervisor carrier board"), [pc("standoffs"), pc("ctrl"), pc("floor")], dwg_no="MTC-DWG-103",
        title="MotionCore supervisor carrier board: making sketch", material="FR4 perforated board 1.6 mm, 2.54 mm pitch",
        view_shape=b.Pos(0, 0, -(zt + 35)) * sup, inset_view=(35, -50),
        notes=["Cut 85 x 88 mm from 1.6 mm FR4 perforated board.",
               "Four 3.2 mm holes for the standoffs: 15 and 75 mm from the edge",
               "  nearest the far end, 6 and 82 mm from the socket-side edge.",
               "The prototype supervisor is built from modules on this board (see",
               "  the wiring picture): microcontroller board with two CAN controllers,",
               "  two CAN transceivers, 18 to 75 V in, 12 V out buck, coil switch,",
               "  precharge switch, input conditioning for the speed, brake and",
               "  e-stop B signals, and a USB socket for the fault log.",
               "Keep all modules inside a 73 x 68 mm area in the middle so the",
               "  modules clear the lid by 10 mm and the four standoff screws.",
               "Fit: four M3 screws into 35 mm hex standoffs; the board sits over",
               "  the controller with 10 mm of air between them.",
               "Check: board flat; no solder tail longer than 2 mm underneath."],
        **base))

    out.append(bv.component_sheet(
        pc("lid"), [pc("tube"), pc("gasket"), pc("floor")], dwg_no="MTC-DWG-104",
        title="MotionCore lid and lid gasket: making sketch", material="Aluminum sheet 3 mm, 5052 or 6061; EPDM sheet 1 mm",
        view_shape=b.Pos(0, 0, -D["z_lid"]) * C["lid"].shape, inset_view=(35, -60),
        notes=["Lid: cut 220 x 140 mm from 3 mm sheet; deburr; round the corners",
               "  to about 1 mm. Four 4.5 mm holes, 7.5 mm in from each end and side.",
               "Gasket: cut from 1 mm closed-cell EPDM sheet, 220 x 140 mm outside,",
               "  a 3 mm wide frame (the wall thickness), with a 12 mm round pad at",
               "  each corner over the port and a 4.5 mm hole through each pad.",
               "Use the lid as the template for the gasket's four holes.",
               "Fit: gasket on the top of the tube, lid on the gasket, four M4 x 10",
               "  button-head screws with bonded sealing washers into the ports.",
               "Tighten evenly in a cross pattern until the gasket is squeezed",
               "  to about two-thirds of its thickness; do not crush it.",
               "Check: lid sits flat; no gap you can see round the edge."],
        **base))

    out.append(bv.component_sheet(
        pc("board"), [pc("tube"), pc("uprights"), pc("posts"), pc("estop"), pc("motor")], dwg_no="MTC-DWG-105",
        title="MotionCore bench board: making sketch", material="Plywood 18 mm, exterior grade",
        view_shape=b.Pos(0, 0, P["board"][4] / 2) * C["board"].shape, inset_view=(35, -60),
        notes=["Cut 960 x 480 mm from 18 mm plywood; sand the edges; mark the",
               "  left end (motor end) and the front edge (the brake lever side).",
               "Module bolts: four 6.5 mm holes on a 180 x 100 mm rectangle, centred",
               "  520 mm from the left end and 240 mm from the front edge.",
               "Motor upright feet: four 6.6 mm holes at 122 and 158 mm from the",
               "  left end, 141.5 and 338.5 mm from the front edge.",
               "Bar post feet: two 6.6 mm holes 80 mm from the front edge, at 652",
               "  and 938 mm from the left end.",
               "E-stop station: fixed with wood screws through its base, centred",
               "  820 mm from the left end and 390 mm from the front edge.",
               "Counterbore the bolt holes from below 13 mm, 3 mm deep, so the",
               "  board sits flat on the bench.",
               "Check: the module's rubber pads land on the four 6.5 mm holes."],
        **base))

    up = C["uprights"].shape & bx(P["motor_x"] - 40, P["motor_x"] + 40, -80, -60, -1, 160)
    out.append(bv.component_sheet(
        part("Motor upright", up, C["uprights"].color), [pc("motor"), pc("feet"), pc("hall_bracket")],
        dwg_no="MTC-DWG-106", title="MotionCore motor upright (make 2): making sketch",
        material="Aluminum flat bar 60 x 6 mm, 6082 or 6061", inset_view=(20, -35),
        view_shape=up,
        notes=["Cut two 150 mm lengths of 60 x 6 mm bar; square and deburr.",
               "Axle slot: 10.2 mm wide on the centre line, 36 mm deep from the top",
               "  end, flat bottom. The axle flats (10 mm) slide in from above and",
               "  its centre sits 120 mm above the board. Saw both sides, file square.",
               "Foot bolt holes: two 6.6 mm, 20 mm up, 18 mm each side of centre.",
               "The upright on the socket side of the motor (the one nearer the",
               "  front edge) also gets two 4.4 mm holes for the Hall bracket,",
               "  120 mm up, 12 and 20 mm from centre toward the module.",
               "Fit: inside faces 135 mm apart (the motor's axle width); feet bolted",
               "  to the outside faces; axle nut and washer outside each upright.",
               "Check: the motor's axle drops into both slots by hand and cannot turn."],
        **base))

    foot = C["feet"].shape & bx(P["motor_x"] - 40, P["motor_x"] + 40, -120, -70, -1, 50)
    out.append(bv.component_sheet(
        part("Upright foot", foot, C["feet"].color), [pc("uprights"), pc("motor")], dwg_no="MTC-DWG-107",
        title="MotionCore upright foot (make 4: two 60 mm, two 40 mm): making sketch",
        material="Aluminum equal angle 40 x 40 x 4 mm", inset_view=(25, -35), view_shape=foot,
        notes=["Cut two 60 mm lengths (motor uprights) and two 40 mm lengths (bar",
               "  posts) of 40 x 40 x 4 angle; square and deburr.",
               "60 mm feet, upright leg: two 6.6 mm holes 20 mm up from the board",
               "  side, 18 mm each side of centre. Flat leg: two 6.6 mm holes",
               "  25 mm from the outside corner, 18 mm each side of centre.",
               "40 mm feet, upright leg: two 6.6 mm holes 12 mm up, 10 mm each side",
               "  of centre. Flat leg: one 6.6 mm hole 25 mm from the outside",
               "  corner, on the centre.",
               "Drill each foot clamped to its upright or post so the holes match.",
               "Fit: the upright leg lies flat on the outside face of the upright or",
               "  post; the flat leg lies on the board and points away from it;",
               "  M6 bolts with washers and nyloc nuts, the board bolts from below.",
               "Check: upright or post stands square to the board."],
        **base))

    out.append(bv.component_sheet(
        pc("hall_bracket"), [part("Upright", C["uprights"].shape & bx(-450, -300, -80, -60, -1, 160), C["uprights"].color), pc("hall"), pc("ring")], dwg_no="MTC-DWG-108",
        title="MotionCore Hall pickup bracket: making sketch", material="Aluminum flat bar 20 x 3 mm",
        inset_view=(55, -120),
        notes=["Cut 42 mm of 20 x 3 mm flat bar; deburr.",
               "Two 4.4 mm holes on the centre line, 4 and 12 mm from one end:",
               "  these bolt to the socket-side upright with M4 bolts.",
               "The Hall pickup sits on the other end, its centre 26 mm from the",
               "  bolted end; mark its lug holes through the pickup and drill to",
               "  suit (usually two M3).",
               "Fit: the bracket lies flat on the inside face of the upright,",
               "  level with the axle, and reaches toward the module. The pickup's",
               "  face is 3.5 mm from the magnet ring, at the ring's magnet circle",
               "  (34 mm from the axle centre).",
               "Check: spin the wheel by hand; the ring passes the pickup without",
               "  touching and the gap is 3 to 4 mm all round."],
        **base))

    post = C["posts"].shape & bx(150, 170, -190, -130, -1, 100)
    post = post & bx(157.01, 162.99, -190, -130, -1, 100)
    out.append(bv.component_sheet(
        part("Bar post", post, C["posts"].color), [pc("bar"), pc("levers"), pc("pod")], dwg_no="MTC-DWG-109",
        title="MotionCore bar post (make 2): making sketch", material="Aluminum flat bar 40 x 6 mm, 6082 or 6061",
        inset_view=(25, -60), view_shape=post,
        notes=["Cut two 90 mm lengths of 40 x 6 mm bar; square and deburr.",
               "Bar hole: 22.5 mm on the centre line, centre 70 mm up from the",
               "  board end. Drill a pilot, open with a step drill or hole saw,",
               "  file to a sliding fit on the 22.2 mm handlebar.",
               "Grub screw: drill 4.2 mm down the centre line from the top end",
               "  into the bar hole and tap M5; an M5 grub screw locks the bar.",
               "Foot bolt holes: two 6.6 mm, 12 mm up, 10 mm each side of centre.",
               "Fit: a 40 mm foot bolts to the outside face of each post; the posts",
               "  stand 230 mm apart (centres) with the bar through both.",
               "Check: the bar slides through both posts by hand and locks with",
               "  the grub screws."],
        **base))

    out.append(bv.component_sheet(
        pc("bar"), [pc("posts"), pc("levers"), pc("pod")], dwg_no="MTC-DWG-110",
        title="MotionCore handlebar stub: making sketch", material="Aluminum tube 22.2 mm outside, 2 mm wall",
        inset_view=(25, -60),
        notes=["Cut 270 mm of 22.2 mm (7/8 in) aluminum tube, square.",
               "Deburr inside and out and chamfer both outside edges 0.5 mm so",
               "  the lever and pod clamps slide on without scoring.",
               "Fit: through both bar posts, 70 mm above the board, ends standing",
               "  10 mm out from each post. From the left: brake lever, pod, brake",
               "  lever, each clamped with its own screw.",
               "Lock it with the two M5 grub screws in the posts.",
               "Check: the clamps tighten without the bar turning in the posts."],
        **base))
    return out


# ----------------------------------------------------------------- hole layouts
def layouts():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    INK, MUT, AC = "#111827", "#4B5563", "#0F766E"
    res = []
    # floor plate, seen from above, far end on the left, socket side at the bottom
    fig = plt.figure(figsize=(11, 8), dpi=150)
    ax = fig.add_axes([0.06, 0.1, 0.62, 0.78]); ax.set_aspect("equal"); ax.set_axis_off()
    ax.add_patch(Rectangle((0, 0), L, W, fc="#F3F4F6", ec=INK, lw=1.2))
    kinds = {"rivet nut": ("#1D4ED8", "Rivet nut, 9.0 drill (4)"),
             "floor screw, countersunk": ("#111827", "Corner screw, 4.5, countersunk below (4)"),
             "controller, M3 tapped": ("#0F766E", "Controller, M3 tapped, 2.5 drill (4)"),
             "supervisor standoff, M3 tapped": ("#15803D", "Supervisor standoff, M3 tapped (4)"),
             "contactor foot, M4 tapped": ("#C2410C", "Contactor foot, M4 tapped, 3.3 drill (2)"),
             "fuse block, M4 tapped": ("#B45309", "Fuse block, M4 tapped, 3.3 drill (2)")}
    xs, ys = set(), set()
    for x, y, d, k in floor_holes(P):
        u, v = x + L / 2, y + W / 2
        ax.add_patch(plt.Circle((u, v), max(d / 2, 1.6), fc="white", ec=kinds[k][0], lw=1.4))
        ax.plot([u - d / 2 - 2, u + d / 2 + 2], [v, v], color=MUT, lw=0.4); ax.plot([u, u], [v - d / 2 - 2, v + d / 2 + 2], color=MUT, lw=0.4)
        xs.add(round(u, 1)); ys.add(round(v, 1))
    for i, u in enumerate(sorted(xs)):
        yl = -6 - 7 * (i % 2)
        ax.plot([u, u], [0, yl + 2], color=AC, lw=0.4, ls=":")
        ax.text(u, yl, f"{u:g}", ha="center", va="top", fontsize=7, color=AC)
    ax.text(L / 2, -22, "from the far end (opposite the sockets), mm", ha="center", fontsize=8, color=MUT)
    for i, v in enumerate(sorted(ys)):
        xl = -4 - 13 * (i % 2)
        ax.plot([xl + 1, 0], [v, v], color=AC, lw=0.4, ls=":")
        ax.text(xl, v, f"{v:g}", ha="right", va="center", fontsize=7, color=AC)
    ax.text(-33, W / 2, "from the socket side, mm", rotation=90, ha="center", va="center", fontsize=8, color=MUT)
    ax.text(L + 3, W / 2, "connector\nend", ha="left", va="center", fontsize=8, color=MUT)
    ax.text(L / 2, W + 4, "plain side", ha="center", va="bottom", fontsize=8, color=MUT)
    ax.set_xlim(-38, L + 25); ax.set_ylim(-26, W + 12)
    fig.text(0.04, 0.965, "Floor plate: hole positions", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.04, 0.93, "Seen from above (the face the tube sits on). Figures in mm, taken from the model.", fontsize=8.5, color=MUT, va="top")
    fig.text(0.70, 0.84, "What each hole is", fontsize=9, fontweight="bold", color=INK, va="top")
    for i, (col, t) in enumerate(kinds.values()):
        fig.patches.append(plt.Circle((0.712, 0.807 - i * 0.04), 0.007, transform=fig.transFigure, fc="white", ec=col, lw=1.4))
        fig.text(0.725, 0.807 - i * 0.04, t, fontsize=8, color=INK, va="center")
    fig.text(0.70, 0.54, "Tapped holes go right through the 3 mm\nplate; a drop of thread sealant on each\nscrew keeps the floor sealed.",
             fontsize=8, color=MUT, va="top")
    fig.text(0.04, 0.015, bv.BANNER, fontsize=7, color="#B45309")
    fig.text(0.96, 0.015, "github.com/BoujeeEnjinia1701/motioncore", fontsize=7, color=AC, ha="right", family="monospace")
    fig.savefig(OUT / "floor-holes.png", facecolor="white"); plt.close(fig); res.append(OUT / "floor-holes.png")

    # connector end wall, seen from outside, and the speed socket in the socket side wall
    fig = plt.figure(figsize=(11, 6.5), dpi=150)
    ax = fig.add_axes([0.04, 0.12, 0.6, 0.72]); ax.set_aspect("equal"); ax.set_axis_off()
    th = D["tube_h"]
    ax.add_patch(Rectangle((0, 0), W, th, fc="#F3F4F6", ec=INK, lw=1.2))
    z0 = D["z_tube"]
    H = connector_holes(P)
    lab = {"xt90": "XT90 slot 12 x 22,\n2 x 3.2 at +-14.5", "motor": "Motor\n20.5", "safety": "Safety loop\n16.5, 4 x 3.2",
           "command": "Command\n16.5, 4 x 3.2"}
    for k in ("xt90", "motor", "safety", "command"):
        y, z, _ = H[k][1]
        u, v = W / 2 + y, z - z0          # seen from outside: socket side (-Y) on the left
        if k == "xt90":
            ax.add_patch(Rectangle((u - 6, v - 11), 12, 22, fc="white", ec=INK, lw=1.1))
            for dz in (-14.5, 14.5):
                ax.add_patch(plt.Circle((u, v + dz), 1.6, fc="white", ec=INK, lw=0.9))
        else:
            d = 20.5 if k == "motor" else 16.5
            ax.add_patch(plt.Circle((u, v), d / 2, fc="white", ec=INK, lw=1.1))
            if k != "motor":
                for dy in (-7.5, 7.5):
                    for dz in (-7.5, 7.5):
                        ax.add_patch(plt.Circle((u + dy, v + dz), 1.6, fc="white", ec=INK, lw=0.9))
        ax.plot([u, u], [-2, -9], color=AC, lw=0.4, ls=":")
        ax.text(u, -10, f"{W / 2 + y:g}", ha="center", va="top", fontsize=7.5, color=AC)
        ax.text(u, th + 2, lab[k], ha="center", va="bottom", fontsize=7, color=INK, linespacing=1.15)
    vh = H["motor"][1][1] - z0
    ax.plot([W + 2, W + 9], [vh, vh], color=AC, lw=0.4, ls=":")
    ax.text(W + 10, vh, f"{vh:g} up", va="center", fontsize=7.5, color=AC)
    ax.text(W / 2, -22, "from the socket side's outer face, mm (seen from outside, socket side on the left)", ha="center", fontsize=8, color=MUT)
    ax.set_xlim(-6, W + 30); ax.set_ylim(-28, th + 22)
    # side wall inset
    ax2 = fig.add_axes([0.68, 0.2, 0.3, 0.5]); ax2.set_aspect("equal"); ax2.set_axis_off()
    ax2.add_patch(Rectangle((0, 0), 60, th, fc="#F3F4F6", ec=INK, lw=1.0))
    for fx in D["fin_x"][:3]:
        u = fx + L / 2
        ax2.add_patch(Rectangle((u - P["fin_t"] / 2, 0), P["fin_t"], th, fc="#D1D5DB", ec=MUT, lw=0.5))
    sx, sz = P["speed_socket"]
    u, v = sx + L / 2, sz - P["floor_t"]
    ax2.add_patch(plt.Circle((u, v), 4.25, fc="white", ec=INK, lw=1.1))
    ax2.text(30, th + 3, f"Speed socket: 8.5 hole, {u:g} from the far end, {v:g} up", ha="center", va="bottom", fontsize=7.5, color=INK)
    ax2.annotate("", xy=(u, v + 4.5), xytext=(u, th + 2.5), arrowprops=dict(arrowstyle="-", color=MUT, lw=0.6))
    ax2.text(-2, th / 2, "far\nend", ha="right", va="center", fontsize=7.5, color=MUT)
    ax2.set_xlim(-14, 64); ax2.set_ylim(-6, th + 14)
    ax2.text(30, -4, "socket side, far end, seen from outside", ha="center", va="top", fontsize=7.5, color=MUT)
    fig.text(0.04, 0.965, "Finned tube: socket holes", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.04, 0.925, "Connector end wall (left) and the speed socket between the first two fins of the socket side (right). "
             "Heights from the tube's bottom edge, mm.", fontsize=8.5, color=MUT, va="top")
    fig.text(0.04, 0.015, bv.BANNER, fontsize=7, color="#B45309")
    fig.text(0.96, 0.015, "github.com/BoujeeEnjinia1701/motioncore", fontsize=7, color=AC, ha="right", family="monospace")
    fig.savefig(OUT / "wall-holes.png", facecolor="white"); plt.close(fig); res.append(OUT / "wall-holes.png")
    return res


# ----------------------------------------------------------------- joints
def joints():
    out = []

    def win(key, box_):
        return C[key].shape & bx(*box_)

    zf, zt, ztop, zl = D["z_floor"], D["z_tube"], D["z_top"], D["z_lid"]
    # 01 floor to tube at a corner port, cut through the port
    px, py = D["ports"][3]
    box_ = (px - 25, px + 10, py - 25, py, zf - 2, zt + 22)
    out.append(bv.joint([
        part("Floor plate", win("floor", box_), C["floor"].color),
        part("Finned tube wall and corner port", win("tube", box_), C["tube"].color),
        part("M4 countersunk screw from below", win("floor_screws", box_), C["floor_screws"].color)],
        OUT / "joint-01.png", "Joint 1: floor plate to finned tube (connector end, plain side corner)",
        subtitle="Cut through the corner port, seen from inside. Conductive sealant film between the faces; the screw pulls them together",
        elev=15, azim=115, size=(8, 6)))
    # 02 rivet nut, pad, board and bolt, cut through the mounting point
    mx, my = D["mounts"][3]
    box_ = (mx - 22, mx, my - 22, my + 22, -P["board"][4] - 9, zt + 15)
    out.append(bv.joint([
        part("Bench board", win("board", box_), C["board"].color),
        part("Rubber pad", win("pads", box_), "#1F2937"),
        part("Rivet nut (closed end)", win("rivnuts", box_), "#B45309"),
        part("Floor plate", win("floor", box_), C["floor"].color),
        part("M6 bolt and washer from below", win("mount_bolts", box_), "#9CA3AF")],
        OUT / "joint-02.png", "Joint 2: host mounting point (one of four), cut open",
        subtitle="Cut through the bolt centre. The closed-end rivet nut keeps the floor sealed; the pad sits under its flange",
        elev=12, azim=8, size=(8, 6)))
    # 03 controller, standoffs and board over it, cut through a standoff
    box_ = (-108, -5, -44, 30, zf - 1, zt + 48)
    out.append(bv.joint([
        part("Floor plate", win("floor", (-108, -5, -44, -20, zf - 1, zt)), C["floor"].color),
        part("Controller on its thermal pad", win("ctrl", box_), C["ctrl"].color),
        part("35 mm standoffs (cut), beside the controller", win("standoffs", box_), C["standoffs"].color),
        part("Supervisor board", win("sup", box_), C["sup"].color)],
        OUT / "joint-03.png", "Joint 3: supervisor board over the controller (cut through two standoffs)",
        subtitle="Seen from the socket side. The standoffs stand on the floor beside the controller, 10 mm of air above it",
        elev=5, azim=-75, size=(8, 6)))
    # 04 sockets in the end wall, seen from inside
    box_ = (60, 140, -70, 70, zf - 1, ztop + 1)
    out.append(bv.joint([
        part("End wall (cut)", win("tube", (95, 111, -70, 70, zt, ztop)), C["tube"].color),
        part("Motor socket and its nut", win("conns", (60, 140, -30, 2, zf, ztop)), C["conns"].color),
        part("Safety loop and command sockets", win("conns", (60, 140, 2, 70, zf, ztop)), "#334155"),
        part("XT90 in its frame", win("xt90", box_), C["xt90"].color),
        part("Floor plate", win("floor", box_), C["floor"].color)],
        OUT / "joint-04.png", "Joint 4: sockets in the connector end wall, seen from inside",
        subtitle="Frames and flanges outside, nuts inside on the wall; every hole is sealed by the socket's own O-ring",
        elev=20, azim=-160, size=(8, 6)))
    # 05 lid corner
    box_ = (px - 25, px + 10, py - 25, py, ztop - 15, zl + 6)
    out.append(bv.joint([
        part("Finned tube and corner port", win("tube", box_), C["tube"].color),
        part("Lid gasket", win("gasket", box_), "#374151"),
        part("Lid", win("lid", box_), C["lid"].color),
        part("M4 button-head screw, sealing washer", win("lid_screws", box_), C["lid_screws"].color)],
        OUT / "joint-05.png", "Joint 5: lid, gasket and corner screw (cut through the port)",
        subtitle="The gasket frame covers the wall top and the port; the lid screw goes into the same port as the floor screw",
        elev=15, azim=115, size=(8, 6)))
    # 06 axle in the upright slot
    MX, AZ = P["motor_x"], P["axle_z"]
    box_ = (MX - 45, MX + 45, -110, -40, -18, AZ + 40)
    out.append(bv.joint([
        part("Upright (socket side)", win("uprights", box_), C["uprights"].color),
        part("Foot", win("feet", box_), C["feet"].color),
        part("Axle end: flats in the slot", win("motor", (MX - 20, MX + 20, -100, -60, AZ - 20, AZ + 20)), "#B45309"),
        part("Bench board", win("board", box_), C["board"].color),
        part("M6 bolts", win("stand_bolts", box_), C["stand_bolts"].color)],
        OUT / "joint-06.png", "Joint 6: motor axle in its upright (socket side, seen from outside)",
        subtitle="Shown before the nut goes on. The axle's flats drop into the 10.2 mm slot so it cannot turn; washer and nut then clamp the upright",
        elev=15, azim=-70, size=(8, 6)))
    # 07 Hall pickup and magnet ring: cut level with the axle, seen from above
    box_ = (MX - 50, MX + 60, -80, -38, AZ - 12, AZ)
    out.append(bv.joint([
        part("Magnet ring on the disc mount", win("ring", box_), C["ring"].color),
        part("Hall pickup", win("hall", box_), "#C2410C"),
        part("Hall bracket", win("hall_bracket", box_), "#475569"),
        part("Upright (socket side)", win("uprights", box_), C["uprights"].color),
        part("Motor side cover", win("motor", (MX - 50, MX + 60, -46, -38, AZ - 12, AZ)), C["motor"].color)],
        OUT / "joint-07.png", "Joint 7: speed sensor, cut level with the axle and seen from above",
        subtitle="Pickup face 3.5 mm from the ring, over the magnet circle 34 mm from the axle centre; bracket flat on the upright",
        elev=80, azim=-90, size=(8, 6)))
    # 08 bar, post, lever and pod
    od, blen, bx0, by, bz = P["bar"]
    box_ = (140, 300, by - 60, by + 25, -5, 100)
    out.append(bv.joint([
        part("Bar post and foot", win("posts", box_), C["posts"].color),
        part("Handlebar stub", win("bar", box_), C["bar"].color),
        part("Brake lever with switch", win("levers", box_), C["levers"].color),
        part("Key and throttle pod", win("pod", box_), C["pod"].color),
        part("Bench board", win("board", box_), C["board"].color)],
        OUT / "joint-08.png", "Joint 8: handlebar stub in its post, with a brake lever and the pod",
        subtitle="The bar slides through the post and is locked by a grub screw from the top; the clamps grip the bar",
        elev=20, azim=-60, size=(8, 6)))
    return out


# ----------------------------------------------------------------- assembly steps
def steps():
    out = []

    def st(n, done, new, title, sub, **kw):
        out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))

    fl = pc("floor")
    st(1, [fl], [pc("rivnuts", "Rivet nuts (4), set from below", (0, 0, -60))], "rivet nuts into the floor plate",
       "Flange underneath; set each with a rivet nut tool so it pulls tight on the 3 mm plate", elev=-25, azim=-60)
    st(2, [pc("tube")], [pc("conns", "Motor, safety and command sockets", (70, 0, 0)), pc("xt90", "XT90 in its frame", (90, 0, 0)),
                         pc("speed_socket", "Speed socket (M8)", (0, -50, 0)), pc("vent", "Vent patch", (-40, 0, 0))],
       "sockets and vent into the finned tube", "Flanges and frames outside, nuts inside; vent patch on the far end wall",
       elev=22, azim=-35)
    st(3, [fl, pc("rivnuts")], [part("Finned tube with its sockets", S("tube", "conns", "xt90", "speed_socket", "vent"), C["tube"].color, (0, 0, 90)),
                                pc("floor_screws", "M4 countersunk screws (4), from below", (0, 0, -40))],
       "finned tube onto the floor plate", "Film of conductive sealant on the floor edge; four M4 screws up into the ports; wipe off the excess",
       elev=18, azim=-55, label_done=False)
    box_ = [fl, pc("rivnuts"), pc("tube"), pc("conns"), pc("xt90"), pc("speed_socket")]
    st(4, box_, [pc("ctrl", "Controller on its thermal pad", (0, 0, 90))], "controller onto the floor",
       "Thermal pad under it; four M3 screws into the tapped floor holes, thread sealant", elev=55, azim=-70, label_done=False)
    st(5, box_ + [pc("ctrl")], [pc("cont", "Contactor", (0, 0, 80)), part("Precharge and fuse block", C["fuse"].shape, "#CA8A04", (0, 70, 150))],
       "contactor and precharge and fuse block", "Two M4 screws each into the tapped floor holes; then the power wiring (wiring picture)",
       elev=55, azim=-70, label_done=False)
    inside = box_ + [pc("ctrl"), pc("cont"), pc("fuse")]
    st(6, inside, [pc("standoffs", "Standoffs (4)", (0, 0, 60)), pc("sup", "Supervisor board", (0, 0, 110))],
       "standoffs and supervisor board", "Standoffs on M3 screws into the floor; board on four M3 screws; then the signal wiring",
       elev=55, azim=-70, label_done=False)
    full = inside + [pc("standoffs"), pc("sup")]
    st(7, full, [pc("gasket", "Lid gasket", (0, 0, 60)), pc("lid", "Lid", (0, 0, 110)),
                 pc("lid_screws", "M4 screws with sealing washers", (0, 0, 150))],
       "gasket and lid", "Gasket on the wall tops, lid on the gasket; four screws, tightened evenly in a cross pattern",
       elev=30, azim=-60, label_done=False)
    module = [part("MotionCore module", S("floor", "rivnuts", "tube", "conns", "xt90", "speed_socket", "gasket", "lid", "lid_screws"),
                   C["tube"].color)]
    brd = pc("board")
    crop = part("Bench board (part shown)", C["board"].shape & bx(-170, 170, -110, 110, -20, 1), C["board"].color)
    st(8, [crop], [pc("pads", "Rubber pads (4)", (0, 0, 40)), part("MotionCore module", module[0].shape, "#64748B", (0, 0, 110)),
                   pc("mount_bolts", "M6 bolts and washers (4), from below", (0, 0, -60))],
       "module onto the bench board", "Seen from slightly below. Pads over the four holes; module on the pads; bolts up into the rivet nuts, snug",
       elev=-12, azim=-60, label_done=True)
    mcrop = part("Bench board (motor end)", C["board"].shape & bx(-480, -280, -130, 130, -20, 1), C["board"].color)
    bcrop = part("Bench board (control end)", C["board"].shape & bx(100, 440, -240, 240, -20, 1), C["board"].color)
    st(9, [mcrop], [pc("uprights", "Motor uprights (2)", (0, 0, 120)), pc("feet", "Feet (2 of 60 mm)", (0, 0, 60))],
       "motor uprights onto the board", "Feet bolted to the outside of each upright, then to the board from below; inside faces 135 mm apart",
       elev=25, azim=-60, label_done=False)
    st(10, [pc("motor")], [pc("ring", "Magnet ring", (0, -60, 0))], "magnet ring onto the motor",
       "Six M5 screws into the motor's six-bolt disc mount, medium threadlocker",
       elev=10, azim=-120, label_done=False)
    stand = [mcrop, pc("uprights"), pc("feet")]
    st(11, stand, [pc("hall_bracket", "Hall bracket", (0, 60, 30)), pc("hall", "Hall pickup", (0, 90, 60))],
       "Hall bracket and pickup onto the upright", "Seen from the inside. Bracket on the inside face of the socket-side upright, two M4 bolts; pickup on the bracket",
       elev=40, azim=115, label_done=False)
    st(12, stand + [pc("hall_bracket"), pc("hall")], [part("Motor with its ring", S("motor", "ring"), C["motor"].color, (0, 0, 120)),
                   pc("axle_nuts", "Axle nuts and washers", (0, 0, 120))],
       "motor into the uprights", "Axle flats down into both slots, ring toward the pickup; washers and nuts outside, tight; gap 3.5 mm",
       elev=22, azim=-60, label_done=False)
    st(13, [bcrop], [pc("posts", "Bar posts with feet (2)", (0, 0, 100)), pc("bar", "Handlebar stub", (-160, 0, 0))],
       "bar posts and handlebar stub", "Posts bolted to the board from below; slide the bar through, centred, grub screws snug",
       elev=25, azim=-60, label_done=False)
    st(14, [bcrop, pc("posts"), pc("bar")], [pc("levers", "Brake levers (2)", (0, -60, 60)), pc("pod", "Key and throttle pod", (0, -60, 60))],
       "brake levers and pod onto the bar", "From the left: lever, pod, lever; each clamp screw to the maker's torque",
       elev=25, azim=-60, label_done=False)
    st(15, [bcrop, pc("posts"), pc("bar"), pc("levers"), pc("pod")], [pc("estop", "E-stop station", (0, 0, 120))],
       "e-stop station onto the board", "Four wood screws through the base inside the station; head toward the operator",
       elev=25, azim=-60, label_done=False)
    on_board = [brd, pc("pads")] + module
    rig = on_board + [pc("uprights"), pc("feet"), pc("motor"), pc("ring"), pc("hall_bracket"), pc("hall")]
    allp = rig + [pc("posts"), pc("bar"), pc("levers"), pc("pod"), pc("estop")]
    st(16, allp, [pc("harness", "Wiring harness", (0, 0, 80))], "harness",
       "Plug each lead into its socket; clip the leads to the board; nothing near the motor shell",
       elev=40, azim=-60, label_done=False)
    return out


# ----------------------------------------------------------------- wiring
def wiring():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    fig = plt.figure(figsize=(13, 8), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 130); ax.set_ylim(0, 80); ax.set_axis_off()
    INK, MUT = "#111827", "#4B5563"
    ax.text(2, 78, "MotionCore prototype: block-level wiring", fontsize=13, fontweight="bold", color=INK, va="top")
    ax.text(2, 74.6, "Inside the module (dashed outline) and the harness to the devices. Stranded copper; ferrules or crimp lugs on every terminal.",
            fontsize=8.5, color=MUT, va="top")
    ax.text(2, 1.5, bv.BANNER, fontsize=7, color="#B45309")
    ax.text(128, 1.5, "github.com/BoujeeEnjinia1701/motioncore", fontsize=7, color="#0F766E", ha="right", family="monospace")
    ax.add_patch(FancyBboxPatch((22, 14), 70, 56, boxstyle="round,pad=0.4", fc="#F8FAFC", ec="#94A3B8", lw=1, ls="--"))
    ax.text(23.5, 70, "Inside the MotionCore module", fontsize=8, color=MUT, va="top")

    def blk(x, y, w, h, title, sub, color):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", fc="white", ec=color, lw=1.8))
        ax.text(x + w / 2, y + h - 1.2, title, ha="center", va="top", fontsize=8.5, fontweight="bold", color=INK)
        ax.text(x + w / 2, y + h - 3.9, sub, ha="center", va="top", fontsize=6.9, color=MUT, linespacing=1.3)

    def wire(pts, color, lw=2.0, ls="-"):
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=color, lw=lw, ls=ls, solid_capstyle="round", zorder=1)

    def lab(x, y, text, color, ha="left"):
        ax.text(x, y, text, fontsize=6.9, color=color, ha=ha, va="center", zorder=3,
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))
    RED, BLK, BLU, GRY, ORG = "#B91C1C", "#111827", "#1D4ED8", "#6B7280", "#C2410C"
    # outside the module
    blk(2, 54, 14, 9, "Battery pack", "20 to 60 V, with BMS\n(host or bench)", "#374151")
    blk(2, 34, 14, 10, "Hub motor", "3 phases, Hall\nsensors, temperature", "#374151")
    blk(2, 16, 14, 9, "Speed sensor", "magnet ring and\nHall pickup", "#0EA5E9")
    blk(108, 54, 20, 9, "E-stop station", "channel A (NC) and\nchannel B (NC)", "#D4A017")
    blk(108, 38, 20, 9, "Brake levers (2)", "NC switches A and B", "#2563EB")
    blk(108, 16, 20, 12, "Key and throttle pod", "key: enable and reset\nthrottle 0.8 to 4.2 V", "#7C3AED")
    # inside
    blk(25, 54, 12, 9, "Main fuse", "20 A or 40 A,\n60 V DC, 1 kA", "#B45309")
    blk(44, 54, 16, 9, "Contactor", "100 A; 12 V coil,\n24 V Zener across it", "#C2410C")
    blk(44, 43, 16, 7, "Precharge", "100 ohm and switch", "#B45309")
    blk(68, 44, 18, 19, "Motor controller", "VESC class, 75 V:\nB+ and B-, phases,\nHall, temperature,\nCAN", "#0F766E")
    blk(26, 17, 60, 16, "Safety supervisor board",
        "microcontroller with two CAN buses; 18 to 75 V in, 12 V out buck; coil switch (in series with\n"
        "the loop); precharge switch; speed, brake and e-stop B inputs; throttle input; USB fault log", "#15803D")
    # power path
    wire([(16, 59), (25, 59)], RED, 2.6); wire([(37, 59), (44, 59)], RED, 2.6); wire([(60, 59), (68, 59)], RED, 2.6)
    lab(20.5, 61.3, "4 mm²", RED, "center"); lab(64, 61.3, "4 mm²", RED, "center")
    wire([(40.5, 59), (40.5, 46.5), (44, 46.5)], RED, 1.2); wire([(60, 46.5), (64, 46.5), (64, 59)], RED, 1.2)
    lab(40.0, 49.5, "1 mm²", RED, "right")
    wire([(16, 56), (19, 56), (19, 52), (68, 52)], BLK, 2.6); lab(33, 52.0, "pack negative to B-, 4 mm²", BLK)
    wire([(16, 39), (73, 39), (73, 44)], ORG, 2.6); lab(23, 40.8, "3 phases 4 mm²; Hall and temperature 0.25 mm²", ORG)
    wire([(31, 54), (31, 33)], RED, 1.0, "--"); lab(31.6, 36.3, "supply 0.5 mm²", RED)
    wire([(52, 33), (52, 43)], GRY, 1.0); lab(52.6, 36.3, "precharge switch", GRY)
    wire([(80, 33), (80, 44)], BLU, 1.2); lab(80.6, 36.3, "internal CAN", BLU)
    # coil loop: supervisor 12 V out, e-stop A, key, back to the coil and the supervisor's coil switch
    wire([(52, 63), (52, 66), (100, 66), (100, 60.5), (108, 60.5)], GRY, 1.4)
    lab(76, 67.5, "coil loop: e-stop A, the key and the coil switch in series, 0.5 mm²", GRY, "center")
    wire([(108, 22), (104, 22), (104, 51.5), (118, 51.5), (118, 54)], GRY, 1.2, ":"); lab(104.6, 31, "key in\nthe loop", GRY)
    wire([(108, 57), (97, 57), (97, 30), (86, 30)], BLU, 1.2); lab(97.6, 54.5, "e-stop B", BLU)
    wire([(108, 42.5), (94, 42.5), (94, 26.5), (86, 26.5)], BLU, 1.2); lab(94.6, 40.4, "brakes A, B", BLU)
    wire([(108, 19), (86, 19)], BLU, 1.2); lab(97, 17.3, "throttle, CAN, 5 V", BLU, "center")
    wire([(16, 20.5), (26, 20.5)], BLU, 1.2); lab(21, 22.3, "speed", BLU, "center")
    for (x, y, t, ha) in ((22, 57.3, "XT90", "center"), (22, 37.3, "9-pin", "center"), (22, 18.6, "M8", "center"),
                          (101, 68.2, "M12 A safety loop", "left"), (91, 21.0, "M12 B command", "center")):
        ax.text(x, y, t, fontsize=6.3, color=INK, ha=ha, va="center", fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.12", fc="#E5E7EB", ec="none"))
    ax.text(23, 9.5, "Safety: e-stop channel A opens the coil circuit with no software in the path. Keep the main fuse out and the pack unplugged until the stop points of section 6.",
            fontsize=7.4, color="#B45309", fontweight="bold")
    ax.text(23, 6.2, "Red: power. Black: pack negative. Orange: motor. Blue: signal. Grey: coil loop and control. Connector pins as Table 3 of the build plan.",
            fontsize=7, color=MUT)
    OUT.mkdir(parents=True, exist_ok=True)
    out = OUT / "wiring.png"
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


if __name__ == "__main__":
    what = sys.argv[1:] or ["overview", "sheets", "layouts", "joints", "steps", "wiring"]
    fns = {"overview": overview, "sheets": sheets, "layouts": layouts, "joints": joints, "steps": steps, "wiring": wiring}
    for w in what:
        r = fns[w]()
        print(w, "->", r)
