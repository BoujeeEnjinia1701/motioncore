"""MotionCore concept media (TRL 3), generated from the parametric model.

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

The reference kit is shown laid out on a workbench: the drive and safety module
(finned enclosure with controller, safety supervisor, contactor and precharge inside),
the reference 250 W geared hub motor, the e-stop station, brake interlock switches, the key
and throttle pod, the independent speed sensor and the harness. Geometry comes from
cad/src/model.py, so the media match the STEP files and drawing MTC-DWG-001. Flow values
are printed by docs/04-calcs/sizing.py (MTC-CAL-001). Bench top at Z = 0, module centered
on the origin so that the cutaway cuts through it.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build123d import Box, Pos
from concept import Part, render_all
from model import build_parts

parts = [Part(n, shape, colour, bom, ex) for n, shape, colour, bom, ex in build_parts()]


def box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


# Context for scale: bench top and a phone lying next to the kit
bench = box(-560, 520, -260, 280, -30, 0)
phone = box(-60, 15, -250, -175, 0, 9)
context = [Part("Bench top", bench, "#C8CDD3"), Part("phone", phone, "#6B7280")]

render_all(
    parts, project="MotionCore", title="Drive and safety module concept", dwg_no="MTC-DWG-010", date="2026-09-25", rev="P2",
    key_figures=["Input 20 to 58 V DC: 24, 36 and 48 V packs incl. SwapCell",
                 "250 W reference; 350 W on 24 V (thermal at risk)",
                 "Hardwired twin-channel e-stop: 67 ms worst case (est.)",
                 "Speed limit twice: controller plus independent supervisor",
                 "Module 243 x 168 x 66 mm, about 1.9 kg (R12 not met)",
                 "Kit $265 in parts; reference motor $70 to host (est.)"],
    scale_figure=False, context=context,
    cut_exclude=("Reference hub motor, 250 W geared", "E-stop station, twin NC", "Brake interlock switches (pair)",
                 "Key switch and throttle pod", "Independent speed sensor", "Wiring harness, keyed connectors",
                 "Connector panel, keyed", "Isolation pads and mounting hardware"),
    flow={"title": "power flow at 250 W shaft output, SwapCell pack, W (estimates, MTC-CAL-001)", "unit": "W",
          "stages": [("Pack output", 322), ("Controller input", 316), ("Motor input", 312),
                     ("Motor shaft", 250)],
          "losses": [(0, "Supervisor, coil, path (est.)", 6), (1, "Controller loss (est.)", 4),
                     (2, "Motor and gear loss (est.)", 62)]},
)
