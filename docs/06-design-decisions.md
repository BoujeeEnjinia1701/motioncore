---
doc_id: MTC-DEC-001
title: MotionCore design decisions register
project: MotionCore
doc_type: Design decisions register
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: Register opened with the build plan; open items from REVIEW.md, MTC-DDR-001 to 003 and the build work; budget treated as a value-engineering target
  - version: "0.2"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Amish approved the recommendations for open decisions 1 to 9 (2026-10-02); moved to decisions made (MTC-DDR-003 accepted)"
  - version: "0.3"
    date: '2026-10-02'
    author: Amish Chadha
    change: 'Follow-ups carried out: economizer in BOM and model (kit USD 297); sealed connector evaluation and license boundary review written (MTC-DDR-004, MTC-DDR-005); item to confirm for the connector part'
---

# MotionCore design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

None. All open decisions were decided on 2026-10-02.

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | A finned enclosure extrusion near 220 x 140 mm with 3 mm walls, vertical-running fins about 3 x 14 mm on a 19 mm pitch and four inside-corner screw ports; if none is stocked, a short custom run or a machined body | Sets the tube, the floor plate's corner holes and the thermal figures | MTC-DDR-003, P1 |
| 2 | The controller's mounting-hole pattern, flat base for the thermal pad, bus capacitance (about 1,000 µF) and MOSFET resistance | Sets the floor plate's controller holes and the precharge and thermal figures | MTC-CAL-001 section 1 |
| 3 | The contactor's foot holes, release time (50 ms or less with the Zener) and DC breaking rating (50 A at 60 V) | Sets the floor holes and the e-stop timing | MTC-CAL-001 section 5 |
| 4 | The reference motor's axle width (about 135 mm), axle flats (10 mm) and six-bolt disc mount | Sets the upright spacing and slot, and the magnet ring | MTC-DDR-003, P10, P11 |
| 5 | Brake levers with normally closed (not normally open) cut-off switches | The interlock expects a closed contact when released | MTC-PRC-001 item 10 |
| 6 | The M12 sockets come with 20 mm four-screw square flanges and the XT90 with a two-screw panel frame | Sets the end wall holes | MTC-DDR-003, P5 |
| 7 | The prospective short-circuit current of a CellGuard 16S pack against the fuse's 1 kA breaking capacity | Fuse choice for CellGuard hosts | MTC-CAL-001 section 3 |
| 8 | Whether a SwapCell pack in legacy discharge accepts a heartbeat and moves to mode 2 without opening its output | The supervisor is powered from the pack | `docs/REVIEW.md`, cross-repo actions |
| 9 | The sealed power connector part: the evaluation (MTC-DDR-004) recommends an industrial IP67 single-pole pair; check one named part's datasheet against the rule (keyed, IP67 mated, 40 A or more at 60 V DC, no exposed live contact), then change the end wall holes, socket frame and BOM line 8 | Sets R10 and the end wall of the tube | MTC-DDR-004 |
| 10 | The coil economizer module: a 12 V, 1 A part with full voltage for 0.5 s, then about 1 W hold and an output capacitor of 100 uF or less | Sets the 1 W hold figure of R9 and the 74 ms of R3 | MTC-CAL-001 v0.5 |

## Value engineering

Value-engineering target: USD 300 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 297 for the MotionCore kit, items 2 to 14 (USD 3 under the target). The reference hub motor (USD 70) is costed to each host, and the bench rig (USD 35) belongs to the prototype only. Main cost drivers and savings worth trying:

- The largest lines are the controller (USD 85), the enclosure tube and floor plate (USD 30), the supervisor with its coil economizer (USD 34), the contactor (USD 25) and the connector set (USD 24).
- The contactor coil economizer (decided 2026-10-02) added USD 4 to the supervisor line.
- Making the design constructable added USD 28: the enclosure tube and floor plate (USD 8 more), the sockets with flanges and frames, the M8 speed socket and the membrane vent (USD 6), brake levers in place of bare switches (USD 6), the speed sensor's plug (USD 2), the harness branch (USD 2) and rivet nuts and fixings (USD 4).
- Savings worth trying: a stock finned extrusion close to the drawn size rather than a custom one; buying the motor, the brake levers and the pod as one e-bike kit; and, once the interface is settled, laying the supervisor out on one small circuit board in place of modules on a carrier board (TRL 4 work).

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items 1 to 11: budget scope (motor costed to hosts), 20 V lower bound, VESC-class controller, DC contactor, stop category 0, interface v0.1, SwapCell heartbeat, CellGuard link, 350 W heavy case, separate firmware, CargoMule as first host | Amish: "i accept all your recommendations, go with them across all repos." | MTC-DDR-001, MTC-DDR-002 |
| 2026-09-25 | R12 module mass limit relaxed from 1.5 to 2.0 kg | Amish, same instruction | MTC-DDR-002 item 15 |
| 2026-09-25 | TRL 3 engineering rules: two CAN buses, 0.6 s precharge with a 90 % bus check, DC-rated fuses with 1 kA breaking capacity, 4 mm² leads for 24 V hosts, 24 V Zener coil suppressor | Amish, same instruction | MTC-DDR-002 item 16 |
| 2026-09-25 | R1 upper bound raised from 58 to 60 V for CellGuard 16S packs (overvoltage fault 66 V, fuses 60 V DC as consequences) | Amish, same instruction | MTC-DDR-002 item 17 |
| 2026-09-25 | Evaluate a sealed power connector before interface v0.1 is frozen; XT90 provisional | Amish, same instruction | MTC-DDR-002 item 18 |
| 2026-10-01 | The budget is a value-engineering target, not a limit | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens. its ok to ensure wording reflects that the hypothesis budget was x - the real cost being accrued is y" | `.kit/STANDARDS.md` section 18 |
| 2026-10-02 | Design for construction accepted as made: the changes P1 to P14 (finned tube on a floor plate, rivet nuts, sockets through the wall, supervisor board layout, bench rig and the others) and their knock-on changes | Amish: "i approve your recommendations for all 555 open decisions." | MTC-DDR-003, Table 1 |
| 2026-10-02 | Interface v0.2: option (a). Issue interface v0.2 with an M8 4-pin speed socket and the pin-out of build plan Table 3, and tell CargoMule, the first host, of the fifth socket | Amish: "i approve your recommendations for all 555 open decisions." | MTC-DDR-003, A1 |
| 2026-10-02 | Bench rig: option (a). Build it with the first prototype, outside the kit total (USD 35) | Amish: "i approve your recommendations for all 555 open decisions." | MTC-DDR-003, A2 |
| 2026-10-02 | Contactor coil economizer: fit it, wired so the safety loop breaks the coil supply upstream of the economizer, so a stop still drops the contactor within the 50 ms the e-stop timing assumes | Amish: "i approve your recommendations for all 555 open decisions." | MTC-DDR-002 item 19; MTC-DDR-003, A3 |
| 2026-10-02 | Sealed power connector: do the paper evaluation now against one rule (keyed, IP67 when mated, at least 40 A continuous at 60 V DC, no exposed live contacts on the pack side); first candidate class, an industrial IP67 single-pole power connector such as Amphenol's SurLok Plus. The XT90 stays for the bench prototype only | Amish: "i approve your recommendations for all 555 open decisions." | MTC-DDR-002 item 18 |
| 2026-10-02 | Dual-motor hosts (PalletPilot): two controllers on one supervisor, with one safety loop and one contactor feeding both controllers | Amish: "i approve your recommendations for all 555 open decisions." | MTC-DDR-001 item 12 |
| 2026-10-02 | Brushed motors (StepClimber): the VESC-class controller's DC motor mode; a different power stage only if StepClimber's motor needs more current than the controller is rated for | Amish: "i approve your recommendations for all 555 open decisions." | MTC-DDR-001 item 13 |
| 2026-10-02 | Appearance model: the lid window, lights, two-flange hub, layout and harness are render-only; the renders are redone on the constructable design before the repo goes public | Amish: "i approve your recommendations for all 555 open decisions." | `docs/REVIEW.md`, session of 2026-09-26 |
| 2026-10-02 | License boundary: a short written review before any firmware is published; a lawyer only if a commercial partner will ship the module | Amish: "i approve your recommendations for all 555 open decisions." | MTC-REQ-001 R13 |
