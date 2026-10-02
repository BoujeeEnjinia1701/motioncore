---
doc_id: MTC-REQ-001
title: MotionCore requirements
project: MotionCore
doc_type: Requirements
version: "0.6"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: First measurable requirements for TRL 2, with status against the concept estimates
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3. R2 heavy case relaxed to 350 W and R14 redefined to the MotionCore kit without the motor (MTC-DDR-001, adopted for TRL 3 pending Amish's review); status column from MTC-CAL-001
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002). R1 upper bound 58 to 60 V; R12 mass limit 1.5 to 2.0 kg; status from MTC-CAL-001 v0.2
- version: "0.5"
  date: '2026-10-01'
  author: Amish Chadha
  change: Constructable design (MTC-DDR-003); status from MTC-CAL-001 v0.3 (R9, R11, R12); R14 reported against the value-engineering target; no status changed
- version: "0.6"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Decisions of 2026-10-02 noted: interface v0.2 (R11), economizer (R9), sealed connector evaluation (R10), license review timing (R13); no status changed"
---

# MotionCore requirements

These requirements are checked by calculation in MTC-CAL-001 v0.3, against the constructable design of MTC-DDR-003. Four targets have changed since TRL 2, all decided by Amish on 2026-09-25 (MTC-DDR-001 and MTC-DDR-002): the heavy case in R2 is 350 W instead of 500 W; R14 covers the MotionCore kit without the reference motor; the upper bound of R1 is 60 V instead of 58 V, so that CellGuard's 16S LiFePO4 packs are covered; and the mass limit in R12 is 2.0 kg instead of 1.5 kg, because the enclosure is also the heat sink. No requirement has been verified by test.

The **reference case** used throughout is a 250 W geared hub motor on a 48 V (46.8 V nominal) SwapCell pack at 40 °C ambient. The **heavy case** is 350 W continuous on a 25.6 V (8S) LiFePO4 pack at 40 °C ambient.

On paper, ten requirements are met and none is not met. R2, R9 and R10 are **at risk**; R11 cannot be verified at TRL 3. R12 is met with a margin of 0.09 kg.

*Table 1. Requirements.*

| ID | Requirement | Target | Verification (TRL 3 or later) | Status at TRL 3 (MTC-CAL-001) |
| --- | --- | --- | --- | --- |
| R1 | Supply range | Operate from 20 to 60 V DC (8S LiFePO4 to 13S lithium-ion and 16S LiFePO4, including SwapCell at 54.6 V full and CellGuard 16S at 58.4 V full); withstand 75 V transients from regeneration | Controller and contactor datasheets; bus voltage calculation | Met (design review): 75 V controller, 18 to 75 V auxiliary buck, bus peaks near 67.8 V with a 66 V controller overvoltage fault |
| R2 | Motor power | 250 W continuous in the reference case; 350 W continuous in the heavy case; 750 W for 10 s | Current and thermal calculation | **At risk:** met electrically (6.9 A, 17.7 A; 750 W peak 21.9 A on SwapCell, 40.9 A on 8S LiFePO4); heavy case limited by R9 |
| R3 | Hardwired emergency stop | Twin-channel normally closed e-stop wired in series with the contactor coil; motor power removed within 100 ms of actuation; works with the supervisor and controller both failed | Circuit review; contactor drop-out time from datasheet | Met on paper: 67 ms worst case, 30 ms modeled; unverified |
| R4 | No automatic restart | After an e-stop, power loss or fault, the drive stays off until the e-stop is released, the throttle is at zero and the operator cycles the enable key | Circuit and state-machine review | Met (design review); unverified |
| R5 | Brake interlock | Two brake switch inputs; drive torque removed within 200 ms of either switch opening; a spring-applied brake output released only while the safety loop is closed | Circuit review; supervisor timing budget | Met on paper: about 75 ms; unverified |
| R6 | Independent speed limit | Speed limit set in the controller and checked by the supervisor from a separate sensor; overspeed of more than 10 % for more than 0.5 s opens the contactor; defaults 25 km/h (pedal assist) and 1.5 m/s (walk-behind) | Firmware review; sensor resolution calculation | Met on paper: period timing, fivefold margin over magnet jitter, trip in 0.60 to 0.70 s; unverified |
| R7 | Fault reaction | Supervisor removes torque within 200 ms of: command timeout, throttle signal outside 0.5 to 4.5 V, loss of controller CAN heartbeat, over-temperature or BMS fault flag | Fault table review | Met on paper: about 170 ms worst (controller heartbeat), about 80 ms for a BMS fault; unverified |
| R8 | Precharge | Inrush at contactor closure under 5 A; bus ready within 1 s | Precharge calculation | Met: 0.55 A peak, 1.3 A at closure, ready in 0.6 s |
| R9 | Thermal | Enclosure surface 60 °C or less at 40 °C ambient in natural convection | Thermal calculation | Reference case met (50.2 °C); **heavy case at risk** (58.4 °C on the walls, 60.0 °C on the floor plate; 65 to 71 °C in sensitivity cases). The contactor coil economizer decided on 2026-10-02 lowers the heavy case to about 55.6 °C on the walls and 57 °C on the floor plate once it is in the design |
| R10 | Ingress and vibration | Enclosure and mated connectors IP65; survive road and stair vibration without loosening | Datasheets and design review | **At risk:** the XT90 power socket is not sealed; a sealed power connector is to be evaluated before interface v0.1 is frozen (MTC-DDR-002). Decided 2026-10-02: the paper evaluation is done now against a rule (keyed, IP67 mated, 40 A or more continuous at 60 V DC, no exposed live contacts on the pack side; first candidate class an industrial IP67 single-pole connector such as Amphenol's SurLok Plus), and the XT90 stays for the bench prototype only; vibration not analyzed |
| R11 | One interface | One documented connector set (power in, motor, sensors, safety loop, command) keyed against mis-mating; fitted to a new host in 2 h or less with hand tools | Interface document; timed fit at TRL 4 | Not verifiable at TRL 3: interface v0.2 decided on 2026-10-02 (MTC-DDR-003 A1): the four sockets of v0.1 drawn in MTC-DWG-001 Rev P3 plus an M8 4-pin speed sensor socket, with the pin-out of build plan Table 3 |
| R12 | Size and mass | Module within 250 x 170 x 70 mm; module mass 2.0 kg or less (1.5 kg before MTC-DDR-002) | Model and mass estimate | Met: 240 x 168 x 69 mm; about 1.91 kg, 0.09 kg margin |
| R13 | Open and repairable | Hardware under CERN-OHL-S-2.0; supervisor firmware MIT; controller firmware open source; fault log readable over USB without closed software | License review | Met (design review): separate programs on separate processors, CAN link only; a short written license boundary review is done before any firmware is published (decided 2026-10-02) |
| R14 | Cost | MotionCore kit (module and devices, BOM items 2 to 14) against a value-engineering target of USD 300 in parts (a hypothetical control target, not a limit); the reference motor is costed to each host | Priced BOM (`bom/bom.csv`) | USD 293 on indicative prices, USD 7 under the target (reference motor USD 70 extra) |

## Assumptions

- Motor efficiency about 80 % at rated load; controller losses from a component model (MTC-CAL-001 Table 1), which gives about 98 to 99 % controller efficiency; to be checked against datasheets once parts are chosen.
- Contactor release time 50 ms or less with a 24 V Zener coil suppressor; this is a selection criterion for the part.
- Enclosure conductance about 1.17 W/K from simplified natural convection and radiation correlations, clear anodized, shaded (MTC-CAL-001 section 4).
- The host provides mechanical brakes able to stop it with the motor unpowered. MotionCore removes drive power; it does not replace the host's brakes.
- The host carries out its own risk assessment. MotionCore targets are not a claimed ISO 13849 performance level.
