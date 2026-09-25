---
doc_id: MTC-REQ-001
title: MotionCore requirements
project: MotionCore
doc_type: Requirements
version: "0.2"
status: Draft
date: '2026-09-25'
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
---

# MotionCore requirements

These are first-pass requirements for the concept. Targets are proposals for review, not yet agreed with the host projects, and will be checked by calculation at TRL 3. The status column compares each target with the first-order estimates in MTC-PRC-001; no requirement has been verified by test.

The **reference case** used throughout is a 250 W geared hub motor on a 48 V (46.8 V nominal) SwapCell pack at 40 °C ambient. The **heavy case** is 500 W continuous on a 25.6 V LiFePO4 pack at 40 °C ambient.

*Table 1. Requirements.*

| ID | Requirement | Target | Verification (TRL 3 or later) | Status at TRL 2 |
| --- | --- | --- | --- | --- |
| R1 | Supply range | Operate from 20 to 58 V DC (8S LiFePO4 to 13S lithium-ion, including SwapCell at 54.6 V full); withstand 75 V transients from regeneration | Controller and contactor datasheets; bus voltage calculation | Met by design (estimate) |
| R2 | Motor power | 250 W continuous in the reference case; 500 W continuous in the heavy case; 750 W for 10 s | Current and thermal calculation | 250 W met; 500 W at risk (see R9) |
| R3 | Hardwired emergency stop | Twin-channel normally closed e-stop wired in series with the contactor coil; motor power removed within 100 ms of actuation; works with the supervisor and controller both failed | Circuit review; contactor drop-out time from datasheet | Met on paper (about 60 ms estimated); unverified |
| R4 | No automatic restart | After an e-stop, power loss or fault, the drive stays off until the e-stop is released, the throttle is at zero and the operator cycles the enable key | Circuit and state-machine review | Met by design; unverified |
| R5 | Brake interlock | Two brake switch inputs; drive torque removed within 200 ms of either switch opening; a spring-applied brake output released only while the safety loop is closed | Circuit review; supervisor timing budget | Met on paper; unverified |
| R6 | Independent speed limit | Speed limit set in the controller and checked by the supervisor from a separate sensor; overspeed of more than 10 % for more than 0.5 s opens the contactor; defaults 25 km/h (pedal assist) and 1.5 m/s (walk-behind) | Firmware review; sensor resolution calculation | Met on paper; unverified |
| R7 | Fault reaction | Supervisor removes torque within 200 ms of: command timeout, throttle signal outside 0.5 to 4.5 V, loss of controller CAN heartbeat, over-temperature or BMS fault flag | Fault table review | Met on paper; unverified |
| R8 | Precharge | Inrush at contactor closure under 5 A; bus ready within 1 s | Precharge calculation | Met (about 0.55 A peak, 0.5 s, estimate) |
| R9 | Thermal | Enclosure surface 60 °C or less at 40 °C ambient in natural convection | Thermal calculation | Reference case met (about 55 °C, estimate); **heavy case not met** (about 67 °C, estimate) |
| R10 | Ingress and vibration | Enclosure and mated connectors IP65; survive road and stair vibration without loosening | Datasheets and design review | Not yet assessed |
| R11 | One interface | One documented connector set (power in, motor, sensors, safety loop, command) keyed against mis-mating; fitted to a new host in 2 h or less with hand tools | Interface document; timed fit at TRL 4 | Interface drafted in MTC-PRC-001; unverified |
| R12 | Size and mass | Module within 250 x 170 x 70 mm; module mass 1.5 kg or less | Model and mass estimate | Met (about 250 x 170 x 66 mm, about 1.3 kg, estimate) |
| R13 | Open and repairable | Hardware under CERN-OHL-S-2.0; supervisor firmware MIT; controller firmware open source; fault log readable over USB without closed software | License review | **At risk:** VESC firmware is GPL-3.0, so its relation to the MIT supervisor firmware needs review |
| R14 | Cost | Reference kit, including the 250 W motor, $300 or less in parts | Priced BOM (`bom/bom.csv`) | **Not met:** about $325 (indicative) |

## Assumptions

- Motor efficiency about 80 % and controller efficiency about 95 % at 250 W, typical of small geared hub motors and VESC-class controllers; to be checked against datasheets at TRL 3.
- Contactor drop-out time 20 to 50 ms with a Zener coil suppressor, typical of small DC contactors; to be confirmed from the chosen part.
- Enclosure heat transfer about 10 W/m²K (natural convection plus radiation) over about 0.13 m² including fins.
- The host provides mechanical brakes able to stop it with the motor unpowered. MotionCore removes drive power; it does not replace the host's brakes.
- The host carries out its own risk assessment. MotionCore targets are not a claimed ISO 13849 performance level.
