---
doc_id: MTC-DDR-002
title: MotionCore recommendations accepted
project: MotionCore
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002); record every newly decided item, what changed in the repo and the items still open
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted

## Context

On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Before that, MTC-DDR-001 had adopted the eleven TRL 2 recommendations for TRL 3 work, open for his review, and the TRL 3 review note (`docs/REVIEW.md`) listed further items as proposed, awaiting Amish. This record lists every item that the instruction turns into a decision, what changed in this repo because of it, and the items that remain open because no recommendation was made. The portfolio stays at TRL 3; TRL 4 is on hold by Amish's instruction.

## Options considered

The options for each item are in `docs/REVIEW.md` (both sessions of 2026-09-25), MTC-DDR-001 and MTC-CAL-001. Where a recommendation named one of several options, that option is the decision.

## Decision

*Table 1. Items decided by Amish, 2026-09-25: go with recommendation.*

| # | Item (source) | Decision | What changed in the repo |
| --- | --- | --- | --- |
| 1 to 11 | TRL 2 review items: budget scope, 20 V lower bound, VESC-class controller, DC contactor, stop category 0, interface v0.1, SwapCell heartbeat, CellGuard link, 350 W heavy case, separate firmware, CargoMule as first host (MTC-DDR-001 Table 1) | Decided as recommended; they were already built into the TRL 3 design | Wording only: "adopted for TRL 3, open for review" replaced by "decided by Amish" in MTC-DDR-001 v0.2, MTC-PRB-001 v0.4, MTC-PRC-001 v0.4, MTC-REQ-001 v0.4 and `bom/bom-notes.md`. `budget_usd` stays $300 (item 1 redefined what the budget covers; no new figure was recommended) |
| 15 | R12 mass shortfall (MTC-DDR-001 item 15) | Option (a): relax R12 from 1.5 kg to 2.0 kg, because the enclosure is the heat sink and R9 is already at risk | MTC-REQ-001 v0.4 R12 target 2.0 kg; R12 status from **not met** to **met** (1.94 kg, 0.06 kg margin); MTC-CAL-001 v0.2 and `sizing.py`; drawing note on MTC-DWG-001 Rev P2; key figure on concept sheet MTC-DWG-010 Rev P3; README |
| 16 | TRL 3 engineering proposals from MTC-CAL-001 (MTC-DDR-001 item 16) | Confirmed: two CAN buses on the supervisor, precharge closure at 0.6 s with a 90 % bus check, DC-rated fuses with 1 kA breaking capacity, 4 mm² pack leads for 24 V hosts, 24 V Zener coil suppressor, controller overvoltage fault | Already in `bom/bom.csv` and MTC-PRC-001; now listed as decided design rules (MTC-PRC-001 v0.4 item 11). Because of item 17, the fuse rating moves from 58 V DC to 60 V DC or more and the overvoltage fault from 60 V to 66 V |
| 17 | R1 upper bound for CellGuard 16S LiFePO4 packs, 58.4 V full (cross-repo note, MTC-DDR-001 item 17) | Raise R1's upper bound from 58 V to 60 V | MTC-REQ-001 v0.4 R1 20 to 60 V; MTC-CAL-001 v0.2: overvoltage fault 66 V, bus peak after a regenerating contactor opening 62.0 V to 67.8 V (inside 75 V), direct-drive back-EMF limit 1.29 to 1.25 times no-load speed, precharge peak 0.60 A at 60 V; `bom/bom.csv` items 2 and 5; MTC-PRB-001 v0.4; MTC-PRC-001 v0.4; drawing and concept sheet notes; README |
| 18 | R10 sealing (MTC-DDR-001 item 18) | Evaluate a sealed power connector before interface v0.1 is frozen | The XT90 is marked provisional in MTC-PRC-001 v0.4 Table 2, `bom/bom.csv` item 8, MTC-DWG-001 Rev P2 and MTC-CAL-001 v0.2. The geometry is unchanged until a connector is chosen. R10 stays at risk. The evaluation itself is a paper task for a later TRL 3 session |

**Consequence of combining items 16 and 17.** Item 16 confirmed a 60 V controller overvoltage fault, and item 17 raised the supply range to 60 V. Both cannot hold: a full CellGuard 16S pack (58.4 V) would sit 1.6 V below the fault. The overvoltage fault therefore moves to 66 V, which keeps the bus under 75 V after a contactor opening during regeneration (67.8 V), and the fuse rating follows R1 to 60 V DC. These two values are engineering consequences of Amish's decisions, recorded here so he can see them.

No design change alters geometry, mass or price: `cad/src/model.py` is unchanged and the STEP and STL files were re-exported only to confirm the model runs. The MotionCore kit stays at $265 against $300, and `trl` and `trl_target` stay at 3.

### Items still open

*Table 2. Items that remain proposed, awaiting Amish.*

| # | Item | Why it stays open |
| --- | --- | --- |
| 12 | Dual-motor hosts (PalletPilot): two controllers on one supervisor, or two modules | No recommendation was made |
| 13 | Brushed motors (StepClimber): VESC DC mode or a different power stage | No recommendation was made |
| 19 | Contactor coil economizer (heavy case about 55.7 °C instead of 58.5 °C) | A suggestion only in MTC-CAL-001, not a recommendation |

Item 14 (whether SunSpoke keeps its own SwapCell charge-host adapter) belongs to the SunSpoke project and is listed under cross-repo actions in `docs/REVIEW.md`.

### Decided but on hold (TRL 4)

Testing of the safety functions, a bench build, the timed fit for R11 and any vibration test remain TRL 4 work and are on hold by Amish's instruction. No item above required TRL 4 work to be recorded.

## Consequences

- Requirement status on paper: ten of fourteen met, none not met, three at risk (R2, R9, R10), one not verifiable at TRL 3 (R11).
- The prospective short-circuit current of a CellGuard 16S pack is not known in this repo; it must be checked against the 1 kA fuse breaking capacity before a CellGuard host is fitted.
- CellGuard, SunSpoke and GravitySort need follow-up in their own repos (cross-repo actions in `docs/REVIEW.md`). No other repo was edited.
- Record any later change to these items as a new decision record.
