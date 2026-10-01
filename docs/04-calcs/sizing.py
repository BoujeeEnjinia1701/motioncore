"""MotionCore sizing calculations, MTC-CAL-001 v0.3 (TRL 3, constructable design MTC-DDR-003).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number quoted in docs/04-calcs/01-sizing.md and writes docs/04-calcs/results.csv.
First-principles paper estimates; nothing here is measured. Geometry comes from
cad/src/model.py (parameters only; build123d is not imported) and costs from bom/bom.csv.
"""
import csv
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad/src"))
from model import PARAMS as P, envelope  # noqa: E402

# ---------------------------------------------------------------- 1. Assumptions
# Host packs: (name, nominal V, minimum V, maximum V, pack resistance ohm, host pack current limit A or None)
PACKS = {
    "swapcell": ("SwapCell 13S Li-ion (interface v0.3)", 46.8, 39.0, 54.6, 0.110, 35.0),
    "cargomule": ("CargoMule 12S LiFePO4", 38.4, 30.0, 43.8, 0.060, 15.0),
    "lfp8s": ("8S LiFePO4 (PalletPilot, StepClimber class)", 25.6, 20.0, 29.2, 0.030, None),
}
V_RANGE = (20.0, 60.0)              # R1, upper bound raised from 58 V (MTC-DDR-002)
CELLGUARD_16S_MAX = 58.4            # V, CellGuard 16S LiFePO4 full charge (16 x 3.65 V)
M_LIMIT = 2.0                       # kg, R12 module mass, relaxed from 1.5 kg (MTC-DDR-002)
V_TRANSIENT = 75.0                  # R1 withstand, controller MOSFET class
ETA_MOTOR = 0.80                    # geared hub at rated load
ETA_MOTOR_PEAK = 0.75               # at 3x rated torque, 10 s
K_PH = 1.2                          # phase rms current / bus current, winding matched to host speed
# Controller (VESC class, 75 V stage) loss model
R_LEG = 0.0039                      # ohm per phase: MOSFET 2.4 mOhm hot + shunt 0.5 + copper 1.0
T_SW, F_SW = 100e-9, 30e3           # s rise plus fall, Hz switching frequency
P_CTRL0 = 1.5                       # W, logic, gate drive, internal supply
# Power path inside the module (ohm): contactor contacts, busbars and internal leads, XT90 pair
R_CONTACTOR, R_INTERNAL, R_XT90 = 0.0005, 0.0015, 0.0006
R_FUSE = {20: 0.0035, 40: 0.0015}   # blade-type fuse, cold resistance, typical
# Auxiliary supply (wide-input buck to 12 V on the supervisor board)
P_COIL, V_COIL = 4.0, 12.0          # W and V, contactor coil without economizer
P_SUP = 0.6                         # W, supervisor MCU, two CAN transceivers, sensors
ETA_AUX = 0.85
# Thermal
T_AMB = 40.0
EMISS = 0.80                        # clear anodized aluminum
ALPHA_SUN = 0.35                    # clear anodized aluminum, solar absorptance
G_SUN = 1000.0                      # W/m2 on the lid, informational case
FIN_CHANNEL = 0.8                   # convection on fin faces relative to a free plate (14 mm gaps)
SIGMA = 5.670e-8
RTH_FET = 0.5 + 4.0                 # K/W, junction to case plus case to body through PCB and pad
N_FET = 6
# E-stop chain
T_BOUNCE = 10e-3                    # s, first opening of the NC contact block plus bounce allowance
L_COIL = 0.30                       # H, assumed coil inductance
R_COIL = V_COIL ** 2 / P_COIL       # ohm
I_DROP_FRAC = 0.10                  # release at 10 % of nominal coil current
T_MECH, T_ARC = 10e-3, 5e-3         # s, armature travel and contact opening; arc at up to 60 V DC
T_RELEASE_SPEC = 50e-3              # s, maximum release time the contactor must meet with its suppressor
V_ZENER, V_DIODE = 24.0, 0.8
V_UV = 18.0                         # V, controller undervoltage cut-off, 8S setting
V_OV = 66.0                         # V, controller overvoltage fault setting (60 V before MTC-DDR-002)
# Precharge
C_BUS = 1000e-6                     # F, controller bus capacitance (to confirm from the chosen part)
R_PRE = 100.0                       # ohm, 10 W aluminum-clad wirewound
N_TAU_CLOSE = 6                     # close the contactor after 6 time constants
R_LOOP_EXTRA = 0.010 + 0.013        # ohm, capacitor ESR plus 3 m of 4 mm2 lead
# Speed sensing
N_MAG = 8
WHEELS = {"20 in (CargoMule)": 1.57, "700C or 28 in (SunSpoke)": 2.15, "200 mm hub (walk-behind)": 0.63}
V_PAS, V_WALK = 25 / 3.6, 1.5       # m/s speed limits
OVERSPEED, PERSIST = 0.10, 0.5
MAG_JITTER = 0.02                   # period error from magnet placement, fraction
# Wiring
RHO_CU = 0.0172                     # ohm mm2/m
LEAD_LEN = 1.5                      # m, pack to module, one way
# Mass (kg)
RHO_AL = 2.70e-6                    # kg/mm3
M_PARTS = {"controller": 0.20, "supervisor (85 x 88 mm board)": 0.07, "contactor": 0.25, "precharge and fuse block": 0.08,
           "sockets, XT90 frame, M8 socket and vent": 0.14, "internal leads": 0.10,
           "pads, rivet nuts, standoffs, screws, gasket and sealant": 0.07}
# Floor joint (MTC-DDR-003): the floor plate carries the controller, contactor and fuse block and joins the
# finned tube through a film of thermally conductive silicone sealant on the wall and port end faces.
K_FILM, T_FILM = 1.0, 0.2e-3        # W/mK, m (film thickness after the screws are tightened)
M_KIT = {"reference hub motor": 2.40, "e-stop station": 0.25, "brake switches (pair)": 0.08,
         "key and throttle pod": 0.12, "speed sensor": 0.04, "harness": 0.45}
BUDGET = 300.0                      # USD, value-engineering target (budget_usd), not a limit

rows = []


def res(rid, value, target, status):
    rows.append((rid, value, target, status))


def ctrl_loss(v, i, k_ph=None):
    iph = (k_ph or K_PH) * i
    cond = 3 * iph ** 2 * R_LEG
    sw = 3 * 0.5 * v * 0.9 * iph * T_SW * F_SW
    return P_CTRL0 + cond + sw, cond, sw


def operating_point(p_shaft, v, fuse, eta_m=ETA_MOTOR):
    """Solve bus current for a shaft power at pack terminal voltage v. Returns dict of results."""
    p_aux = (P_COIL + P_SUP) / ETA_AUX
    r_path = R_CONTACTOR + R_INTERNAL + R_XT90 + R_FUSE[fuse]
    i = p_shaft / eta_m / v
    for _ in range(50):
        pc, cond, sw = ctrl_loss(v, i)
        p_in_ctrl = p_shaft / eta_m + pc
        i_new = (p_in_ctrl + p_aux) / v
        i = i_new
    p_path = i ** 2 * r_path
    i = (p_in_ctrl + p_aux + p_path) / v
    pc, cond, sw = ctrl_loss(v, i)
    return {"i": i, "p_in": p_in_ctrl + p_aux + p_path, "p_ctrl": pc, "cond": cond, "sw": sw,
            "p_aux": p_aux, "p_path": p_path, "eta_ctrl": (p_shaft / eta_m) / p_in_ctrl,
            "p_motor_in": p_shaft / eta_m}


def surface_temp(q, sun=0.0):
    """Module surface temperature for q W internal heat (plus sun W absorbed on the lid)."""
    L, W, H = P["body_l"] / 1e3, P["body_w"] / 1e3, (P["body_h"] + P["lid_t"]) / 1e3
    fin_h = (P["fin_z1"] - P["fin_z0"]) / 1e3
    a_top = L * W
    a_side = 2 * L * H + 2 * W * H
    a_fin = 2 * P["fin_n"] * (2 * P["fin_depth"] + P["fin_t"]) * (P["fin_z1"] - P["fin_z0"]) / 1e6
    lc_top = a_top / (2 * (L + W))
    a_rad = a_top + a_side                      # envelope; fins radiate mostly to each other; underside ignored
    lo, hi = T_AMB, T_AMB + 200
    for _ in range(80):
        ts = (lo + hi) / 2
        dt = ts - T_AMB
        h_v = 1.42 * (dt / H) ** 0.25
        h_f = 1.42 * (dt / fin_h) ** 0.25 * FIN_CHANNEL
        h_t = 1.32 * (dt / lc_top) ** 0.25
        tk, ta = ts + 273.15, T_AMB + 273.15
        h_r = EMISS * SIGMA * (tk ** 2 + ta ** 2) * (tk + ta)
        out = h_v * a_side * dt + h_f * a_fin * dt + h_t * a_top * dt + h_r * a_rad * dt
        if out > q + sun:
            hi = ts
        else:
            lo = ts
    return ts, {"a_top": a_top, "a_side": a_side, "a_fin": a_fin, "a_rad": a_rad, "h_v": h_v, "h_f": h_f,
                "h_t": h_t, "h_r": h_r, "UA": out / dt if dt else 0}


print("MotionCore sizing, MTC-CAL-001 v0.3\n")

# ---------------------------------------------------------------- 2. Operating points and currents (R1, R2)
print("2. Operating points")
cases = [("Reference, 250 W on SwapCell", 250, "swapcell", 20),
         ("CargoMule, 250 W on 12S LFP", 250, "cargomule", 20),
         ("Heavy, 350 W on 8S LFP", 350, "lfp8s", 40),
         ("Heavy, 500 W on 8S LFP (information)", 500, "lfp8s", 40)]
op = {}
for name, pw, pk, fuse in cases:
    _, vn, vmin, vmax, rp, ilim = PACKS[pk]
    a = operating_point(pw, vn, fuse)
    b = operating_point(pw, vmin, fuse)
    op[name] = (a, b, fuse, pk)
    print(f"  {name}: pack {a['p_in']:.0f} W, {a['i']:.1f} A at {vn} V; {b['i']:.1f} A at {vmin} V; "
          f"controller loss {a['p_ctrl']:.1f} W (conduction {a['cond']:.1f}, switching {a['sw']:.1f}), "
          f"controller efficiency {100 * a['eta_ctrl']:.1f} %, aux {a['p_aux']:.1f} W, path {a['p_path']:.2f} W")
ref_a = op["Reference, 250 W on SwapCell"][0]
heavy_a, heavy_b = op["Heavy, 350 W on 8S LFP"][0], op["Heavy, 350 W on 8S LFP"][1]

print("  Peak 750 W for 10 s at nominal voltage:")
peak = {}
for pk, fuse in (("swapcell", 20), ("cargomule", 20), ("lfp8s", 40)):
    label, vn, vmin, vmax, rp, ilim = PACKS[pk]
    a = operating_point(750, vn, fuse, ETA_MOTOR_PEAK)
    peak[pk] = a
    lim = f"; host pack limit {ilim:.0f} A" if ilim else ""
    cap = ""
    if ilim and a["i"] > ilim:
        p_cap = (ilim * vn - a["p_aux"] - (a["p_ctrl"])) * ETA_MOTOR_PEAK
        cap = f", so the host limit caps shaft power at about {p_cap:.0f} W"
        peak[pk + "_cap"] = p_cap
    print(f"    {label}: {a['i']:.1f} A{lim}{cap}")
print(f"  Flow at the reference point: pack {ref_a['p_in']:.0f} W; aux and path {ref_a['p_aux'] + ref_a['p_path']:.1f} W; "
      f"controller input {ref_a['p_motor_in'] + ref_a['p_ctrl']:.0f} W; controller loss {ref_a['p_ctrl']:.1f} W; "
      f"motor input {ref_a['p_motor_in']:.0f} W; motor and gear loss {ref_a['p_motor_in'] - 250:.1f} W; shaft 250 W")
sag_ref = ref_a["i"] * PACKS["swapcell"][4]
print(f"  Voltage sag at the reference point: {sag_ref:.2f} V (pack resistance only)")

print(f"  R1 range {V_RANGE[0]:.0f} to {V_RANGE[1]:.0f} V: CellGuard 16S LiFePO4 full at {CELLGUARD_16S_MAX} V, "
      f"{V_RANGE[1] - CELLGUARD_16S_MAX:.1f} V below the upper bound")
res("R1", f"20 to 60 V covered by a 75 V controller and an 18 to 75 V aux buck; SwapCell 39.0 to 54.6 V, "
          f"CargoMule 30.0 to 43.8 V, 8S LFP 20.0 to 29.2 V and CellGuard 16S LFP up to {CELLGUARD_16S_MAX} V inside the range",
    "20 to 60 V DC; 75 V transient", "Met (design review)")

# ---------------------------------------------------------------- 3. Fuses, contactor, leads
print("\n3. Fuses, contactor and leads")
fuse_rows = []
for pk, fuse, cont_case in (("swapcell", 20, "Reference, 250 W on SwapCell"),
                            ("cargomule", 20, "CargoMule, 250 W on 12S LFP"),
                            ("lfp8s", 40, "Heavy, 350 W on 8S LFP")):
    label, vn, vmin, vmax, rp, ilim = PACKS[pk]
    i_cont = op[cont_case][1]["i"]                       # at minimum voltage
    i_pk = min(peak[pk]["i"], ilim) if ilim else peak[pk]["i"]
    need = max(1.25 * i_cont, i_pk / 1.1)
    ok = fuse >= need
    i_sc = vmax / (rp + R_CONTACTOR + R_INTERNAL + R_XT90 + R_FUSE[fuse])
    fuse_rows.append((label, i_cont, i_pk, need, fuse, ok, i_sc))
    print(f"  {label}: continuous {i_cont:.1f} A at {vmin} V, 10 s peak {i_pk:.1f} A, fuse needs >= {need:.1f} A,"
          f" fitted {fuse} A ({'ok' if ok else 'too small'}); prospective short circuit about {i_sc:.0f} A")
for mm2 in (2.5, 4.0):
    r = RHO_CU * 2 * LEAD_LEN / mm2
    i = heavy_b["i"]
    print(f"  Pack leads {mm2} mm2, 2 x {LEAD_LEN} m: {1000 * r:.1f} mOhm, heavy case {i:.1f} A: drop {i * r:.2f} V,"
          f" loss {i * i * r:.1f} W ({100 * i * i * r / 350:.1f} % of shaft power)")
r25 = RHO_CU * 2 * LEAD_LEN / 2.5
print(f"  Reference case on 2.5 mm2: drop {ref_a['i'] * r25:.2f} V, loss {ref_a['i'] ** 2 * r25:.1f} W")

# ---------------------------------------------------------------- 4. Thermal (R2, R9)
print("\n4. Thermal")
therm = {}
for name in op:
    a, b, fuse, pk = op[name]
    worst = b                                    # minimum voltage gives the highest current
    q = worst["p_ctrl"] + (worst["p_aux"] - 0) + worst["p_path"]
    ts, g = surface_temp(q)
    p_fet = (worst["cond"] + worst["sw"]) / N_FET
    tj = ts + p_fet * RTH_FET
    therm[name] = (q, ts, tj)
    print(f"  {name}: heat {q:.1f} W at minimum pack voltage (controller {worst['p_ctrl']:.1f}, aux "
          f"{worst['p_aux']:.1f}, path {worst['p_path']:.2f}); case {ts:.1f} C; MOSFET junction about {tj:.0f} C")
print(f"  Areas: lid {g['a_top']:.4f} m2, walls {g['a_side']:.4f} m2, fins {g['a_fin']:.4f} m2; "
      f"h at the heavy point: walls {g['h_v']:.1f}, fins {g['h_f']:.1f}, lid {g['h_t']:.1f}, radiation "
      f"{g['h_r']:.1f} W/m2K; UA {g['UA']:.2f} W/K")
hb = op["Heavy, 350 W on 8S LFP"][1]
for kph in (2.0,):
    pc2, c2, s2 = ctrl_loss(PACKS["lfp8s"][2], hb["i"], kph)
    q2 = pc2 + hb["p_aux"] + hb["p_path"]
    ts2, _ = surface_temp(q2)
    print(f"  Sensitivity: heavy case with phase current {kph} x bus current (motor well below base speed): "
          f"controller {pc2:.1f} W, heat {q2:.1f} W, case {ts2:.1f} C")
for rl in (2 * R_LEG,):
    k = rl / R_LEG
    q3 = hb["p_ctrl"] + hb["cond"] * (k - 1) + hb["p_aux"] + hb["p_path"]
    ts3, _ = surface_temp(q3)
    print(f"  Sensitivity: heavy case with twice the phase resistance (budget clone MOSFETs): heat {q3:.1f} W, "
          f"case {ts3:.1f} C")
sun = ALPHA_SUN * G_SUN * g["a_top"]
q_ref = therm["Reference, 250 W on SwapCell"][0]
ts_sun, _ = surface_temp(q_ref, sun)
q_h = therm["Heavy, 350 W on 8S LFP"][0]
ts_sun_h, _ = surface_temp(q_h, sun)
print(f"  Sun on the lid (information): {sun:.1f} W absorbed; reference case {ts_sun:.1f} C, heavy case {ts_sun_h:.1f} C")
q_econ = q_h - (P_COIL - 1.0) / ETA_AUX
ts_econ, _ = surface_temp(q_econ)
print(f"  With a coil economizer (hold at 1 W): heavy case heat {q_econ:.1f} W, case {ts_econ:.1f} C")
L_, W_, T_ = P["body_l"], P["body_w"], P["wall"]
a_joint = (2 * (L_ + W_) * T_ + 4 * math.pi * (P["port_r"] ** 2 - (P["port_hole"] / 2) ** 2)) / 1e6
g_joint = K_FILM * a_joint / T_FILM
p_sup_heat = P_SUP / ETA_AUX
joint = {}
for name in ("Reference, 250 W on SwapCell", "Heavy, 350 W on 8S LFP"):
    q, ts, tj = therm[name]
    dt_j = (q - p_sup_heat) / g_joint
    joint[name] = (dt_j, ts + dt_j)
    print(f"  Floor joint ({name}): {q - p_sup_heat:.1f} W through {1e6 * a_joint:.0f} mm2 of sealant film, "
          f"conductance {g_joint:.1f} W/K: floor plate {dt_j:.1f} K above the walls, {ts + dt_j:.1f} C")
aux_share = ref_a["p_aux"] / therm["Reference, 250 W on SwapCell"][0]
print(f"  Aux supply share of the reference-case heat: {100 * aux_share:.0f} %")

ts_ref = therm["Reference, 250 W on SwapCell"][1]
ts_hv = therm["Heavy, 350 W on 8S LFP"][1]
ts_500 = therm["Heavy, 500 W on 8S LFP (information)"][1]
res("R2", f"250 W: {ref_a['i']:.1f} A at 46.8 V; 350 W: {heavy_a['i']:.1f} A at 25.6 V; 750 W for 10 s: "
          f"{peak['swapcell']['i']:.1f} A (SwapCell), {peak['lfp8s']['i']:.1f} A (8S LFP); CargoMule's 15 A pack "
          f"limit caps its peak at about {peak['cargomule_cap']:.0f} W; heavy case thermal at risk (R9)",
    "250 W reference; 350 W heavy (8S LFP); 750 W for 10 s", "At risk")
res("R9", f"{ts_ref:.1f} C reference; {ts_hv:.1f} C heavy at 350 W (floor plate {joint['Heavy, 350 W on 8S LFP'][1]:.1f} C), "
          f"65 to 71 C in the sensitivity cases ({ts_500:.1f} C at 500 W); shade assumed",
    "60 C or less at 40 C ambient", "At risk")

# ---------------------------------------------------------------- 5. E-stop timing (R3)
print("\n5. Emergency stop timing")
i_nom = V_COIL / R_COIL
i_drop = I_DROP_FRAC * i_nom
tau = L_COIL / R_COIL
t_diode = tau * math.log((V_DIODE + i_nom * R_COIL) / (V_DIODE + i_drop * R_COIL))
t_zener = tau * math.log((V_ZENER + V_DIODE + i_nom * R_COIL) / (V_ZENER + V_DIODE + i_drop * R_COIL))
e_cap = 0.5 * C_BUS * (PACKS["swapcell"][3] ** 2 - 40.0 ** 2)
t_holdup = e_cap / ref_a["p_motor_in"]
t_model_z = T_BOUNCE + t_zener + T_MECH + T_ARC + t_holdup
t_model_d = T_BOUNCE + t_diode + T_MECH + T_ARC + t_holdup
t_worst = T_BOUNCE + T_RELEASE_SPEC + T_ARC + t_holdup
print(f"  Coil {R_COIL:.0f} ohm, {1000 * i_nom:.0f} mA, tau {1000 * tau:.1f} ms; decay to release: diode "
      f"{1000 * t_diode:.1f} ms, {V_ZENER:.0f} V Zener {1000 * t_zener:.1f} ms")
print(f"  Bus capacitor hold-up after opening: {e_cap:.2f} J, {1000 * t_holdup:.1f} ms at the reference point")
print(f"  Power removed: modeled {1000 * t_model_z:.0f} ms with Zener ({1000 * t_model_d:.0f} ms with a plain diode);"
      f" worst case with a {1000 * T_RELEASE_SPEC:.0f} ms release spec {1000 * t_worst:.0f} ms")
travel = {}
for label, v in (("25 km/h", V_PAS), ("1.5 m/s", V_WALK)):
    travel[label] = (v * t_worst, v * 0.1)
    print(f"  Travel at {label}: {100 * v * t_worst:.0f} cm in {1000 * t_worst:.0f} ms, {100 * v * 0.1:.0f} cm in 100 ms")
res("R3", f"{1000 * t_worst:.0f} ms worst case ({1000 * t_model_z:.0f} ms modeled); hardwired channel A, "
          f"no firmware in the path", "100 ms; works with both processors failed", "Met (paper)")
res("R4", "Coil loop needs key reset; supervisor closes its switch only at zero throttle, brakes released, "
          "no faults", "No automatic restart", "Met (design review)")

# ---------------------------------------------------------------- 6. Precharge (R8)
print("\n6. Precharge")
tau_p = R_PRE * C_BUS
t_close = N_TAU_CLOSE * tau_p
pre = []
for pk in PACKS:
    label, vn, vmin, vmax, rp, ilim = PACKS[pk]
    dv = vmax * math.exp(-N_TAU_CLOSE)
    r_loop = rp + R_CONTACTOR + R_INTERNAL + R_XT90 + R_FUSE[40 if pk == "lfp8s" else 20] + R_LOOP_EXTRA
    pre.append((label, vmax / R_PRE, dv, dv / r_loop))
    print(f"  {label}: peak {vmax / R_PRE:.2f} A, residual {dv:.3f} V at close, closure inrush {dv / r_loop:.1f} A")
e_pre = 0.5 * C_BUS * 54.6 ** 2
p_fault = 54.6 ** 2 / R_PRE
print(f"  At the R1 upper bound ({V_RANGE[1]:.0f} V): peak {V_RANGE[1] / R_PRE:.2f} A, residual "
      f"{V_RANGE[1] * math.exp(-N_TAU_CLOSE):.3f} V at close")
print(f"  tau {1000 * tau_p:.0f} ms; contactor closes at {t_close:.1f} s; resistor energy {e_pre:.2f} J per start;"
      f" into a shorted bus {p_fault:.0f} W, so a 1 s timeout limits it to {p_fault:.0f} J")
pmax = max(x[1] for x in pre); imax = max(x[3] for x in pre)
res("R8", f"Peak {pmax:.2f} A through the resistor; {imax:.1f} A at closure (worst pack); ready in {t_close:.1f} s",
    "Under 5 A; ready within 1 s", "Met")

# ---------------------------------------------------------------- 7. Speed sensing, brake and fault timing (R5 to R7)
print("\n7. Speed sensing and reaction times")
for w, c in WHEELS.items():
    for label, v in (("1.5 m/s", V_WALK), ("25 km/h", V_PAS)):
        f = v / c * N_MAG
        print(f"  {w} at {label}: {f:.1f} pulses/s, period {1000 / f:.0f} ms, {f * PERSIST:.1f} pulses in {PERSIST} s")
f_walk = V_WALK / WHEELS["20 in (CargoMule)"] * N_MAG
f_pas = V_PAS / WHEELS["20 in (CargoMule)"] * N_MAG
margin = OVERSPEED / MAG_JITTER
t_trip_walk = PERSIST + 1 / f_walk + t_worst
t_trip_pas = PERSIST + 1 / f_pas + t_worst
print(f"  Count method over {PERSIST} s at 1.5 m/s: +/-1 count is {100 / (f_walk * PERSIST):.0f} % (too coarse);"
      f" period method with a 1 MHz timer: resolution {100e-6 * f_pas:.4f} % at 25 km/h; magnet jitter {100 * MAG_JITTER:.0f} % vs "
      f"{100 * OVERSPEED:.0f} % threshold ({margin:.0f}x margin)")
print(f"  Overspeed trip, 20 in wheel: {t_trip_walk:.2f} s at 1.5 m/s, {t_trip_pas:.2f} s at 25 km/h")
t_brake = 10e-3 + 5e-3 + 10e-3 + 50e-3
t_hb = 100e-3 + 10e-3 + 10e-3 + 50e-3
t_bms = 10e-3 + 10e-3 + 10e-3 + 50e-3
print(f"  Brake switch to zero torque: {1000 * t_brake:.0f} ms (debounce 10, loop 5, CAN 10, current ramp 50)")
print(f"  Lost controller heartbeat: {1000 * t_hb:.0f} ms (timeout 100, loop 10, CAN 10, ramp 50; contactor also opens)")
print(f"  BMS fault (FAULTS sent on change): {1000 * t_bms:.0f} ms")
res("R5", f"{1000 * t_brake:.0f} ms from either switch to zero torque; brake coil powered from the loop",
    "200 ms", "Met (paper)")
res("R6", f"Period method, {100 * MAG_JITTER:.0f} % jitter vs {100 * OVERSPEED:.0f} % threshold; trip in "
          f"{t_trip_walk:.2f} s (1.5 m/s) and {t_trip_pas:.2f} s (25 km/h)", "10 % for 0.5 s opens the contactor",
    "Met (paper)")
res("R7", f"{1000 * max(t_hb, t_bms):.0f} ms worst (controller heartbeat); throttle range and BMS flag faster",
    "200 ms", "Met (paper)")

# ---------------------------------------------------------------- 8. CAN and bus voltage
print("\n8. CAN buses and bus voltage")
bits_ext, bits_int = 135, 160
load_int = (5 * 50 + 100) * bits_int / 500e3
load_ext = 0.018 + (10 + 10) * bits_ext / 250e3
print(f"  Internal bus (supervisor and controller, 500 kbit/s): {100 * load_int:.1f} %")
print(f"  External bus (SwapCell or CellGuard, 250 kbit/s): {100 * load_ext:.1f} % including the pack's 1.8 %")
v_regen = PACKS["swapcell"][3] + 10.0 * (PACKS["swapcell"][4] + 0.02)
dvdt = 10.0 / C_BUS / 1000
e_ind = 3 * 0.5 * 0.2e-3 * 20 ** 2
v_after = math.sqrt(V_OV ** 2 + 2 * e_ind / C_BUS)
print(f"  Regeneration at 10 A into a full SwapCell: {v_regen:.1f} V at the terminals")
print(f"  Regeneration with the contactor open: bus rises {dvdt:.0f} V/ms; with the controller's {V_OV:.0f} V fault the"
      f" phase inductance adds {e_ind:.2f} J, bus peaks near {v_after:.1f} V (limit {V_TRANSIENT:.0f} V)")
print(f"  Overvoltage fault {V_OV:.0f} V leaves {V_OV - CELLGUARD_16S_MAX:.1f} V above a full CellGuard 16S pack "
      f"and {V_OV - V_RANGE[1]:.0f} V above the R1 upper bound")
print(f"  Direct-drive motors: back-EMF stays under {V_TRANSIENT:.0f} V up to {V_TRANSIENT / V_RANGE[1]:.2f} x the "
      f"no-load speed at {V_RANGE[1]:.0f} V")

# ---------------------------------------------------------------- 9. Size and mass (R12)
print("\n9. Size and mass")
L, W, T = P["body_l"], P["body_w"], P["wall"]
h_tube = P["body_h"] - P["floor_t"]
walls = (L * W - (L - 2 * T) * (W - 2 * T)) * h_tube
ports = 4 * (math.pi * (P["port_r"] ** 2 - (P["port_hole"] / 2) ** 2) + P["port_r"] ** 2) * h_tube
fins = 2 * P["fin_n"] * P["fin_t"] * P["fin_depth"] * h_tube
holes_wall = 2 * (11 * 21 + math.pi * (10.25 ** 2 + 2 * 8.25 ** 2)) * T / 2      # connector holes, about
floor = L * W * P["floor_t"] - 4 * math.pi * 4.5 ** 2 * P["floor_t"]
lid = L * W * P["lid_t"]
m_tube = (walls + ports + fins - holes_wall) * RHO_AL
m_encl = m_tube + (floor + lid) * RHO_AL
m_mod = m_encl + sum(M_PARTS.values())
m_kit = m_mod + sum(M_KIT.values())
m_kit_nomotor = m_kit - M_KIT["reference hub motor"]
env = envelope()
print(f"  Module envelope {env[0]:.0f} x {env[1]:.0f} x {env[2]:.0f} mm")
print(f"  Enclosure metal {m_encl:.2f} kg (finned tube {m_tube:.2f}, of which fins {fins * RHO_AL:.2f}; floor plate "
      f"{floor * RHO_AL:.2f}; lid {lid * RHO_AL:.2f}); parts {sum(M_PARTS.values()):.2f} kg; module {m_mod:.2f} kg")
print(f"  Kit with motor {m_kit:.1f} kg; MotionCore kit without the reference motor {m_kit_nomotor:.1f} kg")
res("R12", f"{env[0]:.0f} x {env[1]:.0f} x {env[2]:.0f} mm; {m_mod:.2f} kg", f"250 x 170 x 70 mm; {M_LIMIT:.1f} kg",
    "Met" if m_mod <= M_LIMIT else "Not met")
print(f"  R12 mass limit {M_LIMIT:.1f} kg: margin {M_LIMIT - m_mod:.2f} kg")

# ---------------------------------------------------------------- 10. Cost (R14)
print("\n10. Cost")
with open(ROOT / "bom/bom.csv") as fh:
    bom = list(csv.DictReader(fh))
lines = []
for r in bom:
    n = int(r["item"].split()[0])
    lines.append((n, float(r["qty"]) * float(r["unit_cost_usd"])))
motor = sum(c for n, c in lines if n == 1)
kit = sum(c for n, c in lines if 2 <= n <= 14)
rig = sum(c for n, c in lines if n == 15)
d = BUDGET - kit
print(f"  Value-engineering target: USD {BUDGET:.0f}. Estimated cost of the constructable MotionCore kit (items 2 to 14): "
      f"USD {kit:.0f} (USD {abs(d):.0f} {'under' if d >= 0 else 'over'} the target)")
print(f"  Reference motor (item 1, costed to each host) USD {motor:.0f}; kit with motor USD {kit + motor:.0f}; "
      f"bench rig for the prototype (item 15, not part of the kit) USD {rig:.0f}")
res("R14", f"USD {kit:.0f} for items 2 to 14 (reference motor USD {motor:.0f} costed to the host; bench rig USD {rig:.0f}, prototype only)",
    f"Value-engineering target USD {BUDGET:.0f}", f"{'Under' if d >= 0 else 'Over'} the target by USD {abs(d):.0f} (indicative prices)")

# Requirements checked by review only
res("R10", "XT90 power socket is not sealed; a sealed power connector is to be evaluated before interface v0.1 is frozen "
           "(MTC-DDR-002); M12 and motor plug are IP65 or better when mated; vibration not analyzed",
    "IP65 mated; survive road and stair vibration", "At risk")
res("R11", "Interface v0.1 adopted: XT90 (provisional), 9-pin motor plug, M12 A-coded safety loop, M12 B-coded command, "
           "plus an M8 speed sensor socket (MTC-DDR-003, to confirm); fit time needs a timed fit", "One keyed connector set; fit in 2 h", "Not verifiable at TRL 3")
res("R13", "Supervisor firmware MIT on its own processor; VESC firmware unmodified GPL-3.0 on the controller; "
           "CAN link only; formal license review open", "Open hardware and firmware", "Met (design review)")

# ---------------------------------------------------------------- Results
order = {"Not met": 0, "At risk": 1, "Not verifiable at TRL 3": 2}
rows.sort(key=lambda r: (order.get(r[3], 3), int(r[0][1:])))
print("\nResults against requirements")
for r in rows:
    print(f"  {r[0]:4s} {r[3]:26s} {r[1]}")
with open(ROOT / "docs/04-calcs/results.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["id", "value", "target", "status"])
    w.writerows(rows)
print("\nwrote docs/04-calcs/results.csv")
