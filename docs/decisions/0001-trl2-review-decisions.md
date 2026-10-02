---
doc_id: MTC-DDR-001
title: MotionCore TRL 2 review decisions
project: MotionCore
doc_type: Design decision record
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record the TRL 2 review recommendations adopted for TRL 3 under Amish's 2026-09-25 instruction, open for his review, and the items that remain open
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002). Items 1 to 11 and 15 to 18 decided; 12 and 13 remain open
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Items 12 and 13 decided by Amish on 2026-10-02 (MTC-DEC-001)"
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted. On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Items 1 to 11 and 15 to 18 are decided by Amish, 2026-09-25: go with recommendation (see MTC-DDR-002 for 15 to 18 and what changed). Items 12 and 13 carried no recommendation on 2026-09-25; recommendations were written later and Amish approved them on 2026-10-02 ("i approve your recommendations for all 555 open decisions."; MTC-DEC-001); item 14 belongs to the SunSpoke project.

## Context

The TRL 2 review note (`docs/REVIEW.md`, session of 2026-09-25) listed eleven MotionCore design choices as "Proposed, awaiting Amish", each with a recommendation. On 2026-09-25 Amish asked for this batch of repos to be taken through the usual process to TRL 3 ("you know the drill, nothing gets past TRL 3"). He has not reviewed this batch item by item. Under that instruction, each item that carries a recommendation is adopted as recommended so that TRL 3 work can proceed, and stays open for his review. Items without a recommendation stay open. TRL 4 is on hold by Amish's instruction. Later on 2026-09-25 Amish accepted all the recommendations, so these items are now decided (MTC-DDR-002).

## Options considered

The options for each item are in `docs/REVIEW.md` (session of 2026-09-25, TRL 2) and MTC-PRC-001 v0.2. They are not repeated here.

## Decision

*Table 1. Items decided by Amish, 2026-09-25.*

| # | Item | Decision | Where it now lives |
| --- | --- | --- | --- |
| 1 | Budget | Decided by Amish, 2026-09-25: go with recommendation. Option (b): `budget_usd` stays at $300 and covers the MotionCore kit (module and devices, BOM items 2 to 14); the reference hub motor stays a named part in the interface but is costed to each host. The pitch and problem wording change to match (see below). No new budget figure was recommended, so `project.yaml` keeps $300 | MTC-REQ-001 v0.3 R14, `bom/bom.csv`, `bom/bom-notes.md`, `project.yaml`, README |
| 2 | Input range | Decided by Amish, 2026-09-25: go with recommendation. 20 to 58 V DC; no 12 V variant, so DustRunner stays out of scope | MTC-REQ-001 v0.3 R1, MTC-PRC-001 v0.3 |
| 3 | Controller | Decided by Amish, 2026-09-25: go with recommendation. VESC-class controller with a 75 V stage | MTC-PRC-001 v0.3, `bom/bom.csv` item 2 |
| 4 | Power-removal element | Decided by Amish, 2026-09-25: go with recommendation. Sealed DC contactor in the hardwired safety loop | MTC-PRC-001 v0.3, MTC-CAL-001 section 5, `bom/bom.csv` item 4 |
| 5 | Stop category | Decided by Amish, 2026-09-25: go with recommendation. Category 0 by default; category 1 as a per-host option for heavier hosts | MTC-PRC-001 v0.3 |
| 6 | Interface v0.1 connectors | Decided by Amish, 2026-09-25: go with recommendation. XT90 anti-spark power socket, 9-pin motor plug, M12 8-pin A-coded safety loop, M12 5-pin B-coded command | MTC-PRC-001 v0.3 Table 2, `cad/src/model.py`, MTC-DWG-001 |
| 7 | SwapCell host role | Decided by Amish, 2026-09-25: go with recommendation. The supervisor sends the SwapCell HOST_HEARTBEAT (host type 0, mode 2, or mode 4 when the host enables regeneration). No change to the SwapCell interface. Whether SunSpoke drops its own host adapter is for the SunSpoke project to agree | MTC-PRC-001 v0.3, MTC-CAL-001 section 8 |
| 8 | CellGuard link | Decided by Amish, 2026-09-25: go with recommendation. The supervisor reads CellGuard (or SwapCell) BMS faults over CAN and removes torque | MTC-PRC-001 v0.3, MTC-REQ-001 v0.3 R7 |
| 9 | Heavy-case thermal fix | Decided by Amish, 2026-09-25: go with recommendation. Derate to 350 W continuous on 24 V class packs. R2's heavy case is relaxed from 500 W to 350 W | MTC-REQ-001 v0.3 R2, MTC-CAL-001 section 4 |
| 10 | Firmware licensing | Decided by Amish, 2026-09-25: go with recommendation. VESC firmware stays unmodified as a separate GPL-3.0 program on the controller; the supervisor firmware is MIT on its own processor; they talk only over CAN. A formal license review remains open | MTC-REQ-001 v0.3 R13, MTC-PRC-001 v0.3 |
| 11 | First host | Decided by Amish, 2026-09-25: go with recommendation. CargoMule is the proposed first adopter, subject to the CargoMule project's agreement | MTC-PRB-001 v0.3 |

**Pitch and problem wording (item 1).** The review noted that option (b) changes the pitch ("motor, controller and safety module"). The pitch in `project.yaml` and the README now reads: "A standard controller and safety module (open motor controller, e-stop, speed limit and brake interlock) with a named reference hub motor, which the lab's mobility and automation designs bolt on rather than re-engineer." The problem line is unchanged because it does not mention the motor.

### Items raised later

*Table 2. Items raised after the TRL 2 review, with their status on 2026-09-25.*

| # | Item | Status |
| --- | --- | --- |
| 12 | Dual-motor hosts (PalletPilot): two controllers on one supervisor, or two modules | Decided by Amish, 2026-10-02: two controllers on one supervisor, with one safety loop and one contactor feeding both (MTC-DEC-001) |
| 13 | Brushed motors (StepClimber): VESC DC mode or a different power stage | Decided by Amish, 2026-10-02: VESC DC motor mode; a different power stage only if StepClimber's motor needs more current than the controller is rated for (MTC-DEC-001) |
| 14 | SunSpoke's host adapter: SunSpoke also uses it as the SwapCell charge host (mode 3), which MotionCore does not provide, so the adapter cannot simply be dropped | For the SunSpoke project; not changed here |
| 15 | R12 mass shortfall (1.94 kg against 1.5 kg), found at TRL 3 | Decided by Amish, 2026-09-25: go with recommendation. Option (a): R12 relaxed to 2.0 kg (MTC-DDR-002) |
| 16 | TRL 3 engineering proposals: two CAN buses on the supervisor, contactor closure at 0.6 s with a 90 % bus check, 58 V DC fuses with 1 kA breaking capacity, 4 mm² pack leads for 24 V hosts, 24 V Zener coil suppressor, controller overvoltage fault at 60 V | Decided by Amish, 2026-09-25: go with recommendation. With R1 raised to 60 V (item 17), the fuse rating becomes 60 V DC and the overvoltage fault 66 V (MTC-DDR-002) |
| 17 | R1 upper bound: raise from 58 V to 60 V so that CellGuard's 16S LiFePO4 packs (58.4 V full) are covered | Decided by Amish, 2026-09-25: go with recommendation (MTC-DDR-002) |
| 18 | R10 sealing: boot over the XT90 or a sealed power connector in interface v0.1 | Decided by Amish, 2026-09-25: go with recommendation. Evaluate a sealed power connector before interface v0.1 is frozen; the XT90 is provisional (MTC-DDR-002) |

## Consequences

- The $300 budget now covers the MotionCore kit without the motor: $265 on indicative prices (MTC-CAL-001), so R14 is met. A complete kit with the reference motor is $335; hosts that cite MotionCore at "about $325" (for example GravitySort) should note that the motor is now their cost.
- R2 and R9 are checked at 350 W for the heavy case. The heavy case is at risk thermally (58.5 °C against 60 °C, with little margin).
- MotionCore acts as a SwapCell vehicle host. It depends on the same open SwapCell question that PowerBox raised: whether a pack in legacy discharge accepts a heartbeat and moves to mode 2 without opening its output. That is raised with SwapCell, not changed locally.
- Record any later change to these items as a new decision record.
