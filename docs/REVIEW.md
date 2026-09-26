# Review note: MotionCore

## Session 2026-09-25: recommendations accepted

On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Every item with a recommendation is now **decided by Amish, 2026-09-25: go with recommendation**. The decisions are recorded in `docs/decisions/0002-recommendations-accepted.md` (MTC-DDR-002 v0.1), and MTC-DDR-001 moved to v0.2 with its statuses updated.

### Decisions applied and what changed

| Item | Decision | Before | After |
| --- | --- | --- | --- |
| MTC-DDR-001 items 1 to 11 | Decided as recommended (budget scope, input range, controller, contactor, stop category, interface v0.1, SwapCell heartbeat, CellGuard link, 350 W heavy case, separate firmware, CargoMule first) | "Adopted for TRL 3, open for Amish's review" | "Decided by Amish, 2026-09-25"; no design change |
| Budget (item 1) | Option (b): budget covers the MotionCore kit; motor costed to hosts | `budget_usd` $300 | $300, unchanged (no new figure was recommended); kit $265, $35 margin |
| R12 mass (item 15) | Option (a): relax the limit | 1.5 kg, **not met** (1.94 kg) | 2.0 kg, met with 0.06 kg margin |
| R1 upper bound (item 17) | Raise to cover CellGuard 16S LiFePO4 (58.4 V full) | 20 to 58 V | 20 to 60 V |
| Controller overvoltage fault (item 16, as a consequence of item 17) | Keep headroom above a full 16S pack | 60 V; bus peak 62.0 V | 66 V; bus peak 67.8 V (75 V rating) |
| Fuse rating (item 16, as a consequence of item 17) | Follow R1 | 58 V DC or more, 1 kA | 60 V DC or more, 1 kA |
| Direct-drive back-EMF limit | Follows the 60 V bound | 1.29 times no-load speed | 1.25 times no-load speed |
| Other TRL 3 engineering proposals (item 16) | Confirmed: two CAN buses, 0.6 s precharge with 90 % check, 4 mm² leads for 24 V, 24 V Zener suppressor | Awaiting confirmation | Decided design rules (MTC-PRC-001 v0.4 item 11) |
| R10 sealing (item 18) | Evaluate a sealed power connector before freezing interface v0.1 | XT90 in interface v0.1 | XT90 marked provisional; evaluation is a later TRL 3 paper task; geometry unchanged |

Files changed: MTC-PRB-001 v0.4, MTC-PRC-001 v0.4, MTC-REQ-001 v0.4, MTC-CAL-001 v0.2 (`docs/04-calcs/01-sizing.md`, `sizing.py`, `results.csv`), MTC-DDR-001 v0.2, new MTC-DDR-002 v0.1, `bom/bom.csv` (items 2, 5 and 8 specifications; no price change), `bom/bom-notes.md`, `cad/src/sheets.py` and MTC-DWG-001 Rev P1 to P2 (notes only), `cad/src/concept_media.py` and concept sheet MTC-DWG-010 Rev P2 to P3 (key figures), `project.yaml` (evidence list), `README.md`. `cad/src/model.py` is unchanged; STEP, STL, drawings, media and all PDFs were regenerated, and the regenerated hero, blueprint, exploded view and drawing were checked by eye.

The README "What sparked the idea" section was rewritten around a documented precedent: the 2006 CPSC recall of about 23,500 Segway personal transporters that could apply reverse torque unexpectedly, fixed by a software upgrade ([CPSC](https://www.cpsc.gov/Recalls/2006/segway-inc-announces-recall-to-repair-segway-personal-transporters)). The earlier text that attributed the idea to a review of research areas was removed. `docs/01-problem.md` did not attribute the idea to a review.

### Requirement status now (MTC-CAL-001 v0.2)

Ten of fourteen met on paper; none not met; three at risk; one not verifiable at TRL 3.

| ID | Status | Value |
| --- | --- | --- |
| R2 | At risk | Met electrically; 350 W heavy case limited by R9 |
| R9 | At risk | 50.2 °C reference; 58.5 °C heavy (65 to 71 °C in sensitivity cases) |
| R10 | At risk | XT90 not sealed; sealed connector to be evaluated; vibration not analyzed |
| R11 | Not verifiable at TRL 3 | Interface v0.1 drawn; fit time needs a timed fit (TRL 4) |
| R12 | Met | 1.94 kg against 2.0 kg (was not met against 1.5 kg) |
| R1, R4, R13 | Met (design review) | 20 to 60 V with 75 V parts; key reset; separate firmware, formal license review open |
| R3, R5, R6, R7 | Met (paper) | 67 ms; 75 ms; 0.60 to 0.70 s; 170 ms |
| R8 | Met | 0.55 A peak (0.60 A at 60 V), 1.3 A at closure, 0.6 s |
| R14 | Met (indicative) | $265 against $300 |

### Still awaiting Amish

1. **Dual-motor hosts (PalletPilot):** two controllers on one supervisor, or two modules. No recommendation.
2. **Brushed motors (StepClimber):** VESC DC mode or a different power stage. No recommendation.
3. **Contactor coil economizer** (heavy case about 55.7 °C instead of 58.5 °C): a suggestion only, not a recommendation.

### Cross-repo actions (not changed here)

- **CellGuard:** MotionCore now accepts 16S LiFePO4 up to 58.4 V (R1 20 to 60 V). CellGuard should confirm its 16S pack resistance so that MotionCore can check the prospective short-circuit current against the 1 kA fuse breaking capacity.
- **SunSpoke:** SunSpoke's host adapter is also its SwapCell charge host (mode 3); whether it keeps that adapter is for the SunSpoke project (MTC-DDR-001 item 14).
- **SwapCell:** the open question shared with PowerBox stands: may a pack in legacy discharge accept a heartbeat and move to mode 2 without opening its output?
- **CargoMule:** confirm it agrees to be the first host (MTC-DDR-001 item 11).
- **GravitySort:** update its MotionCore cost from "about $325" to $265 for the kit plus $70 for the motor.

### Safety

- The overvoltage fault at 66 V leaves less margin to the 75 V MOSFET rating (bus peak 67.8 V instead of 62.0 V). Direct-drive hosts need a speed limit below 1.25 times no-load speed or a bus clamp.
- Fuses must be rated for 60 V DC or more with 1 kA breaking capacity; 32 V automotive fuses are not suitable.
- R12's 0.06 kg margin means any added part must be weighed; do not thin the enclosure, which is the heat sink.
- All other safety concerns from the TRL 3 session below still apply.

### TRL

`trl: 3` and `trl_target: 3` are unchanged. TRL 4 (bench build, safety-function tests, timed fit, vibration) remains on hold by Amish's instruction; nothing in this session started it.

### Recommended next step

A TRL 3 paper evaluation of sealed power connectors for interface v0.1 (R10), then freeze the interface.

## Session 2026-09-25: TRL 3

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (MTC-DDR-001 v0.1): the eleven TRL 2 recommendations adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review; open items listed.
- `docs/04-calcs/01-sizing.md` (MTC-CAL-001 v0.1) with `docs/04-calcs/sizing.py` and `results.csv`: operating points, fuses, contactor and leads, thermal with sensitivities, e-stop timing, precharge, speed sensing, reaction times, CAN loads, bus voltage, size, mass and cost. The script reads `cad/src/model.py` parameters and `bom/bom.csv` and prints every quoted number.
- `cad/src/model.py`: parametric build123d model of the module (enclosure with fins and M6 mounting inserts, lid, controller, supervisor, contactor, precharge and fuse block, connector panel with the four interface v0.1 connectors, isolation pads) and the reference kit devices. Exports `cad/step/` and `cad/stl/` `motioncore-module`, `motioncore-enclosure` and `motioncore-kit`.
- `cad/src/sheets.py` and `cad/drawings/MTC-DWG-001.svg`, `.pdf`, `.png`: general arrangement of the module, Rev P1, "CONCEPT, NOT FOR FABRICATION" (the concept sheet keeps MTC-DWG-010, now at P2).
- `bom/bom.csv`: all 14 lines priced with supplier types and the TRL 3 selection criteria; `bom/bom-notes.md` totals against the budget.
- `cad/src/concept_media.py` now builds from the model; all media in `media/` regenerated and checked by eye. The module is centered on the origin, so the kit's cutaway cuts through it; the connector panel and pads are excluded from the section.
- Docs updated to v0.3 with revision entries dated 2026-09-25: MTC-PRB-001, MTC-PRC-001, MTC-REQ-001. `project.yaml`: `trl: 3`, `trl_target: 3`, evidence listed, pitch reworded. `README.md`: TRL 3, new pitch, concept numbers from MTC-CAL-001, links to the drawing and sizing note.

### Requirements (MTC-CAL-001)

Nine of fourteen met on paper; one not met; three at risk; one not verifiable at TRL 3.

| ID | Status | Value |
| --- | --- | --- |
| R12 | **Not met** | Module about 1.94 kg against 1.5 kg (size 243 x 168 x 66 mm is met) |
| R2 | At risk | Met electrically; 350 W heavy case limited by R9 |
| R9 | At risk | 50.2 °C reference; 58.5 °C at 350 W on 8S LiFePO4, 65 to 71 °C in sensitivity cases; about 68 °C at 500 W |
| R10 | At risk | XT90 power socket is not sealed; vibration not analyzed |
| R11 | Not verifiable at TRL 3 | Interface v0.1 drawn; the 2 h fit needs a timed fit |
| R1, R4, R13 | Met (design review) | 20 to 58 V with 75 V parts; key reset; separate firmware, formal license review open |
| R3, R5, R6, R7 | Met (paper) | E-stop 67 ms worst case; brake 75 ms; overspeed trip 0.60 to 0.70 s; faults 170 ms worst |
| R8 | Met | 0.55 A peak, 1.3 A at closure, ready in 0.6 s |
| R14 | Met (indicative) | MotionCore kit $265 against $300; reference motor $70 costed to hosts ($335 with motor) |

TRL 2 numbers corrected: pack power 333 to 322 W, controller loss 16 to 3.9 W, e-stop about 60 to 67 ms worst case, precharge closure 0.5 to 0.6 s (0.5 s left up to 8 A at closure on a low-resistance pack), module 1.3 to 1.94 kg, kit 4.4 to 5.3 kg, CargoMule pack 36 V class to 12S LiFePO4 at 38.4 V.

### Decisions recorded (MTC-DDR-001)

Items 1 to 11 are decided by Amish, 2026-09-25: go with recommendation (MTC-DDR-002): budget option (b) with the motor costed to hosts and `budget_usd` unchanged at $300; 20 to 58 V input; VESC-class controller; DC contactor; stop category 0 by default; interface v0.1 connectors; supervisor sends the SwapCell heartbeat; CellGuard link over CAN; heavy case derated to 350 W on 24 V; separate firmware licensing; CargoMule as proposed first host. The pitch in `project.yaml` and the README was reworded to match item 1 (DDR-001 records the wording); the problem line is unchanged.

### Still awaiting Amish

Update, 2026-09-25: items 1, 3 and 4 below are now decided by Amish, 2026-09-25: go with recommendation (MTC-DDR-002); item 5 is settled by item 1 of MTC-DDR-001 ($300 unchanged); item 2 stays proposed, awaiting Amish.

1. **R12 mass (new at TRL 3).** Options: (a) relax R12 to 2.0 kg; (b) 2 mm walls and lid with 3 mm fins, about 1.63 kg, still over and with less heat-sink metal; (c) (b) plus a lighter contactor. Recommendation: (a), because the enclosure is the heat sink and R9 is already at risk.
2. **Dual-motor hosts (PalletPilot)** and **brushed motors (StepClimber)**. No recommendation was made; they stay proposed, awaiting Amish.
3. **R10 sealing.** Options: a sealing boot over the XT90, or a sealed power connector in interface v0.1. Recommendation: evaluate a sealed connector before freezing the interface; this changes an adopted interface item, so it needs Amish.
4. **Engineering proposals from MTC-CAL-001** (DDR-001 item 16): two CAN buses on the supervisor, precharge closure at 0.6 s with a 90 % bus check, 58 V DC fuses with 1 kA breaking capacity, 4 mm² pack leads for 24 V hosts, 24 V Zener coil suppressor, controller overvoltage fault at 60 V. A coil economizer (heavy case about 56 °C instead of 58.5 °C) is a suggestion only, not in the BOM.
5. **Budget.** No new figure was recommended; `budget_usd` stays $300 for the MotionCore kit. A complete kit with motor is $335 for host budgets.

### Cross-repo notes (not changed in other repos)

- **SwapCell:** MotionCore builds to interface v0.3 as a vehicle host (type 0, mode 2; mode 4 only when a host enables regeneration). It shares PowerBox's open question: may a pack in legacy discharge accept a heartbeat and move to mode 2 without opening its output? The supervisor is powered from the pack, so it depends on this. The INTERLOCK coding resistor is in the host's receptacle, not in MotionCore.
- **CellGuard:** consistent with CellGuard's recommendations to adopt the SwapCell message set and a STM32G0B1-class controller. Conflict: CellGuard supports 16S LiFePO4 at up to 58.4 V, just above MotionCore's 58 V limit in R1. Raising R1's upper bound to 60 V would cover it (the 75 V parts allow it); decided by Amish, 2026-09-25: go with recommendation (MTC-DDR-002).
- **SunSpoke:** its host adapter is also the SwapCell charge host (mode 3), so the MotionCore heartbeat does not let SunSpoke drop the adapter unless SunSpoke keeps a charge host elsewhere.
- **CargoMule:** its 15 A pack limit caps its peak at about 414 W of shaft power; that is a host setting.
- **GravitySort:** cites MotionCore at "about $325" including the motor; under item 1 that becomes $265 for the kit plus $70 for the motor.

### Safety concerns

- Every safety function (e-stop timing, restart inhibit, brake interlock, overspeed trip) is a paper claim until tested; first power-up only on a bench, wheel off the ground, second person at the e-stop. Testing is TRL 4 and on hold.
- Prospective short-circuit currents of about 470 to 860 A: the main fuse must be rated for 58 V DC or more with 1 kA breaking capacity; common 32 V automotive fuses are not suitable.
- The contactor must break DC under load at up to 58 V and release within 50 ms with a Zener suppressor; a plain diode lengthens the release.
- Regeneration with the contactor open drives the bus up at about 10 V/ms; the controller's 60 V overvoltage fault is part of the safety case. Direct-drive hosts need a speed limit below 1.29 times no-load speed or a bus clamp.
- The heavy case runs within 1.5 K of the 60 °C case limit in shade and above it in sun.
- A category 0 stop does not brake; hosts need unpowered brakes. Bridging the safety loop defeats every protection. A wrong wheel circumference moves the speed limit.
- MotionCore is not certified and does not make a host compliant with any machinery, vehicle or pedelec rule.

### Other notes

- No TRL 4 material exists in the repo; `build-log/README.md` is the scaffold stub and was not touched.
- Citations: the TRL 2 note lists no unchecked citations, so none were fetched.
- `render.py --check` and `render.py` pass; PDFs are in `docs/pdf/`.

### Recommended next step

Review MTC-DDR-001 and the items above, in particular R12 (mass) and the R1 upper bound for CellGuard's 16S packs. TRL 4 is on hold by Amish's instruction. For reference only, TRL 4 would need: a bench build of the module, a lab test report (TST, `environment: lab`) covering e-stop power-removal time, restart inhibit, brake interlock, overspeed trip, precharge inrush and case temperature at 250 W and 350 W, a timed fit on one host, and build-log entries. None of this has been started.

## Session 2026-09-25: /populate to a strong TRL 2

### What was done

- `docs/01-problem.md` (MTC-PRB-001 v0.2): problem with cited figures, users, host project table (SunSpoke, CargoMule, PalletPilot, StepClimber, DustRunner), operating environment, constraints, out of scope, prior work with links (VESC, ODrive, SimpleFOC, ISO 13850, IEC 60204-1, ISO 13849-1, Regulation (EU) No 168/2013), open questions and a new co-design checklist aimed at the host project leads.
- `docs/03-requirements.md` (MTC-REQ-001 v0.2): 14 measurable requirements (R1 to R14) with targets, verification method and a status column against the TRL 2 estimates; reference and heavy cases defined; assumptions listed.
- `docs/02-concept.md` (MTC-PRC-001 v0.2): how it works (power up, enable, drive, watch, stop), numbered components, draft connector interface v0.1, first-order numbers (currents and fuse, e-stop timing, precharge, thermal, speed sensing, size, mass and cost), proposed design choices, safety section, open questions.
- `cad/src/concept_media.py`: massing model of the reference kit on a bench (module with fins, controller, supervisor, contactor, precharge and fuse block, lid, connector panel, 250 W hub motor, e-stop station, brake switches, key and throttle pod, speed sensor, harness), each part with a BOM number; bench top and a phone as the scale context instead of the 1.75 m figure, because the kit is bench-sized.
- `media/`: `hero.png`, `concept-blueprint.png`, `.pdf` and `.svg`, `exploded.png` (callouts 1 to 13 match the BOM), `cutaway.png` (inside of the module), `flow.png` (power flow at 250 W, all values estimates), `model.glb` and `viewer.html`.
- `bom/bom.csv`: 14 lines with indicative prices, numbered to match the exploded view; `bom/bom-notes.md` updated.
- `README.md`: hero image and links line; Concept rationale, Burning platform, By industry, By country or region and What sparked the idea expanded with cited figures; Concept, Key components and Safety updated to match.
- `docs/pdf/`: branded PDFs of the three controlled documents.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Input range | 20 to 58 V DC (24, 36, 48 V hosts incl. SwapCell) | R1 met by design |
| Pack current, reference case (250 W shaft, 46.8 V) | about 333 W, about 7.1 A | Fuse 20 A |
| Pack current, heavy case (500 W, 25.6 V) | about 26 A | Fuse 40 A |
| E-stop power removal | about 60 ms (contactor drop-out 20 to 50 ms, assumed) | R3 met on paper (100 ms) |
| Travel during 100 ms | about 0.7 m at 25 km/h; about 0.15 m at 1.5 m/s | |
| Precharge | about 0.55 A peak, 0.5 s, 1.5 J per start | R8 met |
| Case temperature at 40 °C ambient | about 55 °C at 250 W; about 67 °C at 500 W | R9 met at 250 W; **not met at 500 W** |
| Module size and mass | about 250 x 170 x 66 mm, about 1.3 kg; kit about 4.4 kg | R12 met |
| Reference kit cost | about $325 (module and devices about $255, motor about $70) | **R14 not met, about 8 % over $300** |

Requirements not met or at risk:

- **R14 (cost) not met:** about $325 against $300.
- **R9 (thermal) not met in the heavy case:** about 67 °C case against 60 °C at 500 W on 24 V; R2 at 500 W is therefore at risk.
- **R13 (open licensing) at risk:** VESC firmware is GPL-3.0; the boundary with the MIT supervisor firmware needs review.
- **R10 (ingress and vibration)** not yet assessed.
- **R3 to R7** (e-stop, restart inhibit, brake interlock, speed limit, fault reaction) are met on paper only; none is verified.
- DustRunner (12.8 V) is outside the proposed input range, so MotionCore does not cover all five host projects.

### Proposed, awaiting Amish

Update, 2026-09-25: all eleven items below are decided by Amish, 2026-09-25: go with recommendation (MTC-DDR-001 v0.2, MTC-DDR-002).

1. **Budget.** Options: (a) raise `budget_usd` from $300 to $330; (b) cost the motor to each host, so the MotionCore kit (module and devices, about $255) meets $300, which changes the pitch wording ("motor, controller and safety module"); (c) cut cost (cheaper VESC variant, local enclosure) to reach $300. Recommendation: (b), keeping the motor as a named reference part in the interface. `project.yaml` is unchanged.
2. **Input range.** 20 to 58 V (recommended) versus adding a 12 V variant to cover DustRunner.
3. **Controller.** VESC class (recommended) versus ODrive or a custom stage with Safe Torque Off.
4. **Power-removal element.** DC contactor (recommended at TRL 2) versus gate-driver Safe Torque Off.
5. **Stop category.** Category 0 default (recommended) with category 1 as an option for heavier hosts, versus category 1 by default.
6. **Interface v0.1 connectors.** XT90 anti-spark, 9-pin motor plug, two keyed M12 connectors (recommended), versus all-automotive sealed connectors.
7. **SwapCell host role.** Let the supervisor send the SwapCell heartbeat (recommended; would let SunSpoke drop its separate host adapter, subject to that project's agreement) versus leaving it to each host. This needs no change to the SwapCell interface.
8. **CellGuard link.** Supervisor reads CellGuard BMS faults over CAN and removes torque (recommended).
9. **Heavy-case thermal fix.** Derate to 350 W continuous at 24 V (recommended at TRL 2), versus a fan, versus mounting to the host frame.
10. **Firmware licensing.** Keep VESC firmware unmodified as a separate program and the supervisor under MIT (recommended, pending review), versus licensing the supervisor firmware under GPL-3.0.
11. **First host.** SunSpoke or CargoMule (250 W geared hub, closest to the reference case) as the first adopter; recommendation: CargoMule, which also needs the brake interlock for its overrun coupler.

### Safety concerns

- The safety functions are unverified; first power-ups must be on a bench with the wheel off the ground and a second person at the e-stop.
- A category 0 stop does not brake; hosts must have brakes that work unpowered, and walk-behind hosts need spring-applied brakes.
- Direct-drive motors can pump the bus voltage through the MOSFET body diodes when pushed with the contactor open; a bus clamp is needed for those hosts.
- Contactor arcing when breaking DC under load at up to 58 V; part must be DC-rated at full pack voltage.
- Pack short-circuit current, residual charge in bus capacitors, and a hot enclosure (about 55 to 67 °C).
- Bridging the safety loop defeats every protection; keying and plain fault documentation are the only defense at this level.
- MotionCore is not certified and does not make a host compliant with any machinery, vehicle or pedelec rule.

### Problems and notes

- The kit is bench-sized, so the hero uses a bench top and a phone for scale rather than the 1.75 m figure.
- The cutaway shows the module interior only; external devices are excluded from the section.
- The legacy `cad/src/model.py` placeholder is untouched (TRL 3 work).
- Host README figures in Table 1 of MTC-PRB-001 are taken from the host repos as they stand; if a host changes voltage or motor, the table needs an update.

### Recommended next step

Review this note and the media, then decide items 1, 2 and 7. If approved, run `/advance-trl3` to check the e-stop timing, precharge, thermal and fuse estimates by calculation, choose the contactor and controller parts, freeze interface v0.1 and produce the parametric model and drawing sheet.

## Session 2026-09-26: sources strengthened

| README item | Old source | New source |
| --- | --- | --- |
| Kenya row (By country or region) | CleanTechnica, 2025, reporting KNBS 2024 registrations (trade press, standing alone) | [IEA Global EV Outlook 2026, trends in other EV modes](https://www.iea.org/reports/global-ev-outlook-2026/trends-in-other-ev-modes): electric two-wheeler sales more than tripled in 2025 to over 25,000, around 15 % of new registrations |

All other links in the four sourced README sections (IEA, CPSC micromobility report, HSE fatal injury statistics, Regulation (EU) No 168/2013, CPSC 2006 Segway recall) were fetched and confirmed on 2026-09-26. `docs/01-problem.md` did not cite the replaced source, so no controlled document changed.
