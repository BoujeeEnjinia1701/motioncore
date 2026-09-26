---
doc_id: MTC-CAL-001
title: MotionCore sizing calculations
project: MotionCore
doc_type: Calculation note
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First TRL 3 sizing note (currents, fuses and leads, thermal, e-stop timing, precharge, speed sensing, reaction times, CAN and bus voltage, size, mass, cost) against the TRL 3 decisions in MTC-DDR-001
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002). R1 upper bound 58 to 60 V (CellGuard 16S), controller overvoltage fault 60 to 66 V, fuse rating 60 V DC or more, R12 mass limit 1.5 to 2.0 kg
---

# MotionCore sizing calculations

On paper, MotionCore meets ten of its fourteen requirements and none is outright not met. R12 is met after Amish relaxed the mass limit from 1.5 kg to 2.0 kg (MTC-DDR-002): the module weighs about 1.94 kg, a margin of only 0.06 kg, because the finned enclosure that is also the heat sink weighs about 1.0 kg on its own. R1 now runs to 60 V so that CellGuard's 16S LiFePO4 packs (58.4 V full) are covered. R2 and R9 are **at risk** in the heavy case: at 350 W on an 8S LiFePO4 pack the case reaches about 58.5 °C against 60 °C, and reasonable changes to the controller assumptions push it to 65 to 71 °C. R10 is **at risk** because the XT90 power socket is not sealed, and R11 (fit time) cannot be verified at TRL 3. The reference case is comfortable: about 50 °C on the case, 6.9 A from a SwapCell pack, e-stop power removal within 67 ms worst case, and a MotionCore kit cost of $265 against the $300 budget, with the $70 reference motor costed to each host.

Every number here is printed by `docs/04-calcs/sizing.py` (run from the repo root: `python docs/04-calcs/sizing.py`), which also writes `docs/04-calcs/results.csv`. The script reads the enclosure dimensions from `cad/src/model.py` and the costs from `bom/bom.csv`. All values are first-principles estimates; nothing is measured.

## 1. Assumptions

*Table 1. Inputs. All are assumptions for a paper design; part-specific values are to be confirmed from datasheets once parts are chosen.*

| Input | Value | Basis |
| --- | --- | --- |
| Reference pack | SwapCell 13S lithium-ion, 46.8 V nominal, 39.0 to 54.6 V, 110 mΩ, 20 A continuous, 35 A for 10 s | SwapCell interface v0.3 (SWC-PRC-001 v0.3) |
| CargoMule pack | 12S LiFePO4, 38.4 V nominal, 30.0 to 43.8 V, about 60 mΩ, 15 A host limit | CargoMule precis (CGM-PRC-001); resistance assumed |
| Heavy-case pack | 8S LiFePO4, 25.6 V nominal, 20.0 to 29.2 V, about 30 mΩ | PalletPilot and StepClimber class; resistance assumed |
| Motor efficiency | 80 % at rated load, 75 % at 750 W for 10 s | Typical small geared hub |
| Phase to bus current ratio | 1.2 (winding matched to the host's speed) | Assumption; 2.0 checked as a sensitivity |
| Controller losses | 3.9 mΩ per phase (MOSFET 2.4 mΩ hot, shunt 0.5 mΩ, copper 1.0 mΩ); 100 ns switching edges at 30 kHz; 1.5 W fixed | Typical VESC-class 75 V stage |
| Power path in the module | Contactor 0.5 mΩ, internal leads 1.5 mΩ, XT90 pair 0.6 mΩ, fuse 3.5 mΩ (20 A) or 1.5 mΩ (40 A) | Typical parts |
| Auxiliary supply | Coil 4.0 W at 12 V, supervisor 0.6 W, buck efficiency 85 % | Typical sealed 100 A contactor without economizer |
| Enclosure | 220 x 140 x 60 mm body, 3 mm walls, 3 mm lid, 22 fins 4 x 14 x 48 mm; clear anodized, ε 0.80, solar absorptance 0.35 | `cad/src/model.py` |
| Convection | Vertical plates h = 1.42 (ΔT/L)^0.25, lid h = 1.32 (ΔT/L)^0.25, fin faces 0.8 of a free plate; underside ignored | Simplified laminar correlations for still air |
| CellGuard pack | 16S LiFePO4, 58.4 V full | R1 check only; pack resistance not known here |
| Contactor coil | 36 Ω, 0.30 H, releases at 10 % of rated current; 10 ms armature travel; 5 ms arc | Assumed; release time 50 ms or less is a selection criterion |
| Bus capacitance | 1,000 µF; precharge 100 Ω | To confirm from the chosen controller |
| Speed sensor | 8 magnets; 2 % period jitter from magnet placement | Concept (MTC-PRC-001) |
| Ambient | 40 °C, shaded | MTC-REQ-001 R9 |

## 2. Operating points (R1, R2)

The controller is more efficient than the blanket 95 % assumed at TRL 2, so the pack supplies about 322 W, not 333 W, in the reference case. At the reference point about 5.7 W goes to the auxiliary supply and power path, 3.9 W to the controller and 62.5 W to motor and gear losses (Figure 4 in MTC-PRC-001).

*Table 2. Operating points. Currents at nominal and minimum pack voltage.*

| Case | Pack power | Current, nominal V | Current, minimum V | Controller loss | Controller efficiency |
| --- | --- | --- | --- | --- | --- |
| Reference: 250 W, SwapCell | 322 W | 6.9 A at 46.8 V | 8.3 A at 39.0 V | 3.9 W | 98.8 % |
| CargoMule: 250 W, 12S LFP | 323 W | 8.4 A at 38.4 V | 10.8 A at 30.0 V | 4.3 W | 98.7 % |
| Heavy: 350 W, 8S LFP | 453 W | 17.7 A at 25.6 V | 22.9 A at 20.0 V | 9.0 W | 98.0 % |
| 500 W, 8S LFP (information) | 648 W | 25.3 A at 25.6 V | 32.9 A at 20.0 V | 15.5 W | 97.6 % |

For 750 W over 10 s at nominal voltage, the pack current is 21.9 A on SwapCell (inside its 35 A, 10 s limit) and 40.9 A on 8S LiFePO4. CargoMule's own 15 A pack limit caps its peak at about 414 W of shaft power: this is a host setting, which the supervisor respects, not a MotionCore limit. The supervisor sets the controller's battery current limit to the lower of the host setting and the pack's allowed discharge current in PACK_LIMITS.

All three host packs fall inside 20 to 60 V, and so does a full CellGuard 16S LiFePO4 pack at 58.4 V, 1.6 V below the new upper bound (MTC-DDR-002; it was 58 V). The controller is a 75 V class and the auxiliary buck accepts 18 to 75 V, so **R1 is met by design review**. R2 is met electrically; its heavy case depends on R9 and is **at risk**.

## 3. Fuses, contactor and leads

The fuse must carry 1.25 times the continuous current at minimum pack voltage and hold the 10 s peak at no more than 110 % of its rating, which a blade fuse carries without opening.

*Table 3. Fuse check.*

| Pack | Continuous at minimum V | 10 s peak | Fuse needed | Fitted | Prospective short circuit |
| --- | --- | --- | --- | --- | --- |
| SwapCell | 8.3 A | 21.9 A | 19.9 A | 20 A | about 470 A |
| CargoMule | 10.8 A | 15.0 A (host limit) | 13.6 A | 20 A | about 663 A |
| 8S LiFePO4 | 22.9 A | 40.9 A | 37.2 A | 40 A | about 856 A |

The 20 A and 40 A fuses proposed at TRL 2 hold, although the 20 A fuse has little margin for a SwapCell host that uses the full 750 W peak. The fuse must be rated for **60 V DC or more** (58 V before R1 was raised) with at least **1 kA** breaking capacity; common 32 V automotive fuses are not suitable. The prospective short-circuit current of a CellGuard 16S pack is not calculated here because its resistance is not known in this repo; it must be checked against the 1 kA breaking capacity before a CellGuard host is fitted. The contactor carries at most about 41 A for 10 s against its 100 A rating; the selection criterion that matters is breaking at least 50 A at 60 V DC.

Pack leads of 2.5 mm² over 1.5 m each way drop 0.14 V and lose 1.0 W in the reference case. In the heavy case at 20 V they drop 0.47 V and lose 10.8 W (3.1 % of shaft power); 4 mm² leads cut this to 0.30 V and 6.7 W, so 24 V hosts get 4 mm² pack leads (`bom/bom.csv` item 13).

## 4. Thermal (R9)

The enclosure has 0.0308 m² of lid, 0.0454 m² of walls and 0.0338 m² of fin faces. At the heavy point the heat-transfer coefficients are about 6.5 W/m²K on the walls, 5.6 on the fins, 6.7 on the lid and 6.4 for radiation, giving a conductance of about 1.17 W/K (the TRL 2 estimate was 1.3 W/K). Heat is taken at minimum pack voltage, where the current is highest.

*Table 4. Case and MOSFET temperatures at 40 °C ambient, shaded.*

| Case | Heat in the module | Case surface | MOSFET junction |
| --- | --- | --- | --- |
| Reference, 250 W on SwapCell | 10.0 W | 50.2 °C | about 52 °C |
| CargoMule, 250 W | 11.2 W | 51.2 °C | about 54 °C |
| Heavy, 350 W on 8S LFP | 20.1 W | 58.5 °C | about 67 °C |
| 500 W on 8S LFP (information) | 32.7 W | 67.9 °C | about 84 °C |

The derate to 350 W at 24 V (MTC-DDR-001 item 9) is needed: 500 W misses the 60 °C target by about 8 K. At 350 W the margin is only 1.5 K and depends on the controller assumptions:

- Phase current twice the bus current (a motor running well below its base speed, as a walk-behind host with a fast winding would): 37.2 W, **71.0 °C**.
- Twice the phase resistance (budget controller MOSFETs): 28.9 W, **65.1 °C**.
- Sun on the lid (information; R9 assumes shade): 10.8 W absorbed, 59.1 °C in the reference case and 66.5 °C in the heavy case.

The auxiliary supply is about 54 % of the reference-case heat, mostly the contactor coil. A coil economizer that holds the contactor at about 1 W would lower the heavy case to 16.5 W and 55.7 °C. **R9 is met in the reference case and at risk in the heavy case.**

## 5. Emergency stop timing (R3)

Channel A of the e-stop opens the contactor coil circuit directly. With a 24 V Zener across the coil, the coil current decays from 333 mA to its release point in 2.9 ms (τ = 8.3 ms); a plain diode takes 15.5 ms. Adding 10 ms for contact opening and bounce, 10 ms for armature travel, 5 ms of arc and 2.2 ms during which the bus capacitors (0.69 J) keep the motor running gives about **30 ms modeled** with the Zener and 43 ms with a plain diode.

The worst case uses the release time the contactor must meet as a selection criterion (50 ms or less with its suppressor): 10 + 50 + 5 + 2.2 ≈ **67 ms**, inside the 100 ms of R3. In 67 ms a host at 25 km/h travels about 47 cm and a walk-behind machine at 1.5 m/s about 10 cm (69 cm and 15 cm in the full 100 ms). No firmware is in this path, so R3 holds with both processors failed. **R3 is met on paper.** R4 (no automatic restart) is met by circuit review: the coil loop can close only after the key is cycled, and the supervisor closes its switch only at zero throttle with the brakes released and no fault.

## 6. Precharge (R8)

With 100 Ω and 1,000 µF the time constant is 100 ms. At the 60 V upper bound of R1 the peak precharge current is 0.60 A and the residual at closure 0.15 V. The supervisor closes the contactor after six time constants (0.6 s) and only if the controller reports a bus voltage of at least 90 % of the pack voltage, which catches a shorted bus or a missing capacitor bank. The residual difference at closure is 0.07 to 0.14 V, and the closure inrush is 1.0 A (SwapCell), 1.2 A (CargoMule) and 1.3 A (8S LiFePO4), under the 5 A target. Peak precharge current is 0.55 A at 54.6 V, and the resistor absorbs 1.49 J per start. Into a shorted bus it would dissipate 30 W; a 1 s timeout limits that to 30 J, which a 10 W aluminum-clad resistor survives. **R8 is met.** The TRL 2 figure of 0.5 s (five time constants) left up to 8 A at closure on a low-resistance LiFePO4 pack, so the closure point moves to 0.6 s.

## 7. Speed sensing and reaction times (R5 to R7)

*Table 5. Speed sensor pulse rates with eight magnets.*

| Wheel | At 1.5 m/s | At 25 km/h |
| --- | --- | --- |
| 20 in, 1.57 m (CargoMule) | 7.6 pulses/s (131 ms period) | 35.4 pulses/s (28 ms) |
| 700C or 28 in, 2.15 m (SunSpoke) | 5.6 pulses/s (179 ms) | 25.8 pulses/s (39 ms) |
| 200 mm hub, 0.63 m (walk-behind) | 19.0 pulses/s (52 ms) | 88.2 pulses/s (11 ms) |

Counting pulses over 0.5 s is too coarse at walking pace (one count is 26 % of the reading). The supervisor therefore times each period with a 1 MHz timer (resolution about 0.0035 % at 25 km/h); magnet placement jitter of about 2 % leaves a fivefold margin to the 10 % overspeed threshold. Overspeed held for 0.5 s opens the contactor in about 0.70 s at 1.5 m/s and 0.60 s at 25 km/h on a 20 in wheel, including one pulse period and the 67 ms contactor budget. **R6 is met on paper.** The wheel circumference and magnet count are configuration values; a wrong value moves the limit, so they belong on the fault chart.

Timing budgets: a brake switch sets the controller command to zero in about 75 ms (10 ms debounce, 5 ms loop, 10 ms CAN, 50 ms current ramp), inside 200 ms (**R5 met on paper**). A lost controller heartbeat takes about 170 ms (100 ms timeout plus loop, CAN and ramp), and the contactor is opened as well; a BMS fault, which SwapCell and CellGuard send on change, takes about 80 ms (**R7 met on paper**).

## 8. CAN buses and bus voltage

The supervisor uses two CAN buses: an internal bus to the controller at 500 kbit/s (the VESC default) and an external bus to the SwapCell pack or CellGuard BMS at the SwapCell rate of 250 kbit/s. The internal bus carries five controller status frames at 50 Hz and commands at 100 Hz, about 11.2 % load. The external bus carries the pack's frames (1.8 %, SWC-CAL-001) plus the supervisor's HOST_HEARTBEAT and a status frame at 10 Hz each, about 2.9 % in total. Keeping the buses apart means the pack never sees controller traffic and no VESC setting has to change.

As a SwapCell host, the supervisor sends HOST_HEARTBEAT as host type 0 (vehicle) and requests mode 2 (discharge). The controller's battery regeneration current is set to zero unless the host enables regeneration, in which case the supervisor requests mode 4 with a host charge limit, as SwapCell interface v0.3 item C allows.

Regeneration at 10 A into a full SwapCell pack raises its terminals to about 55.9 V, inside 60 V. Raising R1 to 60 V means the controller's overvoltage fault can no longer sit at 60 V, where a full CellGuard 16S pack (58.4 V) would leave only 1.6 V of headroom; it moves to 66 V, 7.6 V above that pack and 6 V above the R1 bound. If the contactor opens while the controller is regenerating, the bus rises at about 10 V/ms, and with the fault at 66 V the energy left in the phase inductance (0.12 J) lifts the bus to about 67.8 V (62.0 V with the earlier 60 V setting), still inside the 75 V rating but with less margin. A direct-drive motor pushed faster than its no-load speed is the remaining risk: its back-EMF stays under 75 V only up to 1.25 times the no-load speed at 60 V (1.29 times at 58 V), so direct-drive hosts need a speed limit below that or a bus clamp.

## 9. Size and mass (R12)

The module envelope from the model is 243 x 168 x 66 mm, inside 250 x 170 x 70 mm. The enclosure metal weighs about 1.01 kg (body shell 0.58 kg, fins 0.16 kg, lid 0.26 kg), and the parts inside and on the panel about 0.93 kg, so the module weighs about **1.94 kg against the 2.0 kg limit: R12 is met**, with 0.06 kg of margin. Amish relaxed the limit from 1.5 kg to 2.0 kg (MTC-DDR-002) rather than thin the enclosure, because the enclosure is the heat sink and R9 is already at risk. The TRL 2 estimate of 1.3 kg left out most of the enclosure metal. Thinner walls and lid (2 mm) and 3 mm fins would bring it to about 1.63 kg, at the cost of heat-sink metal. The kit weighs about 5.3 kg with the reference motor and 2.9 kg without it. Any part added to the module must be weighed against the small margin.

## 10. Cost (R14)

Under the redefined budget (MTC-DDR-001 item 1) the $300 covers the MotionCore kit, items 2 to 14 of `bom/bom.csv`: **$265, a margin of $35**. The reference hub motor (item 1, $70) is costed to each host, which brings a complete kit with motor to $335. The supervisor rose from $22 to $30 to carry a second CAN transceiver and the 18 to 75 V auxiliary buck, and the pads and consumables from $6 to $8. All prices are indicative. **R14 is met on indicative prices.**

## 11. Results against requirements

*Table 6. Requirement status (at risk first; none is not met).*

| ID | Value | Target | Status |
| --- | --- | --- | --- |
| R2 | 250 W: 6.9 A; 350 W: 17.7 A; 750 W for 10 s: 21.9 A (SwapCell), 40.9 A (8S LFP) | 250 W reference; 350 W heavy; 750 W for 10 s | At risk (heavy case thermal, R9) |
| R9 | 50.2 °C reference; 58.5 °C heavy (65 to 71 °C in sensitivity cases) | 60 °C at 40 °C ambient | At risk |
| R10 | XT90 not sealed; sealed power connector to be evaluated before interface v0.1 is frozen; M12 and motor plug sealed when mated; vibration not analyzed | IP65; survive vibration | At risk |
| R11 | Interface v0.1 adopted and drawn (MTC-DWG-001); fit time needs a timed fit | One keyed set; fit in 2 h | Not verifiable at TRL 3 |
| R1 | Three host packs and CellGuard 16S (58.4 V) inside 20 to 60 V; 75 V controller; 18 to 75 V auxiliary buck | 20 to 60 V; 75 V transients | Met (design review) |
| R3 | 67 ms worst case, 30 ms modeled; no firmware in the path | 100 ms | Met (paper) |
| R4 | Key reset; supervisor enable conditions | No automatic restart | Met (design review) |
| R5 | 75 ms | 200 ms | Met (paper) |
| R6 | Period method; 5x margin over jitter; trip 0.60 to 0.70 s | 10 % for 0.5 s | Met (paper) |
| R7 | 170 ms worst | 200 ms | Met (paper) |
| R8 | 0.55 A peak; 1.3 A at closure; ready in 0.6 s | Under 5 A; 1 s | Met |
| R13 | MIT supervisor on its own processor; unmodified GPL-3.0 VESC firmware; CAN link only | Open hardware and firmware | Met (design review); formal license review open |
| R12 | 243 x 168 x 66 mm; 1.94 kg | 250 x 170 x 70 mm; 2.0 kg | Met (0.06 kg margin) |
| R14 | $265 for items 2 to 14 | $300 | Met (indicative prices) |

## 12. Checks against earlier documents

The TRL 2 figures in MTC-PRC-001 v0.2, MTC-REQ-001 v0.2 and the README were checked against this script and corrected in v0.3: pack power 333 W to 322 W; reference current 7.1 A to 6.9 A; CargoMule current 9.3 A at 36 V to 8.4 A at 38.4 V (CargoMule uses a 12S LiFePO4 pack); controller loss 16 W to 3.9 W; reference case temperature 55 °C to 50 °C; 500 W case 67 °C to 68 °C (now information only); heavy case now 350 W and 58.5 °C; e-stop time about 60 ms to 67 ms worst case; precharge closure 0.5 s to 0.6 s; module envelope 250 x 170 x 66 mm to 243 x 168 x 66 mm; module mass 1.3 kg to 1.94 kg; kit mass 4.4 kg to 5.3 kg; cost $325 for the full kit to $265 for the MotionCore kit plus $70 for the reference motor ($335 with motor). The speed-sensor pulse rates (7.5 and 35 pulses per second) and the precharge peak (0.55 A, 1.5 J) stand. In v0.2 (MTC-DDR-002): R1 upper bound 58 V to 60 V; overvoltage fault 60 V to 66 V and bus peak 62.0 V to 67.8 V; fuse rating 58 V DC to 60 V DC or more; direct-drive back-EMF limit 1.29 to 1.25 times no-load speed; R12 limit 1.5 kg to 2.0 kg, status not met to met.

> **Safety:** These are paper estimates for a module that switches a lithium pack able to deliver several hundred amperes into a short and drives moving machinery. They do not replace a circuit review, datasheet checks or testing of the safety functions. Nothing may be built or energized from this note; building and testing are TRL 4 work and on hold by Amish's instruction.
