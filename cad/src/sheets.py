"""MotionCore general arrangement drawing MTC-DWG-001 (Rev P1).

Run from the repo root:  python cad/src/sheets.py
Builds cad/drawings/MTC-DWG-001.svg, .pdf and .png from the parametric model (module only).
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from drawing import Sheet, project_views  # noqa: E402
from model import PARAMS as P, assemblies, build_parts, envelope  # noqa: E402

parts = build_parts()
module = assemblies(parts)["motioncore-module"]
work = ROOT / "cad/drawings/_views"
views = project_views(module, work)
L, Wd, H = envelope()

s = Sheet(project="MotionCore", title="General arrangement, drive and safety module", dwg_no="MTC-DWG-001",
          rev="P1", author="Amish Chadha", date="2026-09-25", concept=True,
          material="Body and lid: extruded Al, clear anodized. Parts per bom/bom.csv",
          revisions=[("P1", "Preliminary GA, interface v0.1 (MTC-CAL-001)", "2026-09-25", "AC")])
s.add_ortho(views, ["front", "top", "right"])
s.add_svg(views["iso"], 276, 30, 140, 76, label="Isometric view", sublabel="Not to scale")
s.add_notes("Key dimensions and interfaces (mm)", [
    f"Overall {L:.0f} x {Wd:.0f} x {H:.0f} incl. pads and connectors",
    f"Body {P['body_l']:.0f} x {P['body_w']:.0f} x {P['body_h']:.0f}, wall {P['wall']:.0f}, lid {P['lid_t']:.0f}",
    f"Fins {P['fin_n']} per side, {P['fin_t']:.0f} x {P['fin_depth']:.0f} x {P['fin_z1'] - P['fin_z0']:.0f}, pitch {P['fin_pitch']:.0f}",
    f"Mounting: 4 x M6 on {P['mount_px']:.0f} x {P['mount_py']:.0f}, pads D{P['pad_d']:.0f} x {P['pad_h']:.0f}",
    "+X panel, from -Y: XT90 power in (anti-spark),",
    "  9-pin motor plug, M12 8-pin A safety loop,",
    "  M12 5-pin B command and CAN (250 kbit/s)",
    "Input 20 to 58 V DC; fuse 20 A (36, 48 V) or 40 A (24 V)",
    "Contactor 100 A, breaks 50 A at 60 V DC, 50 ms max",
    "Precharge 100 ohm, close at 0.6 s (MTC-CAL-001)",
    "Module about 1.94 kg (R12 target 1.5 kg not met)",
    "PRELIMINARY, NOT FOR FABRICATION",
], x=276, y=126, width=140)
s.save(ROOT / "cad/drawings/MTC-DWG-001")
shutil.rmtree(work, ignore_errors=True)
print("wrote cad/drawings/MTC-DWG-001.svg, .pdf, .png")
