# Review note: MotionCore

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
