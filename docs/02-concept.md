---
doc_id: MTC-PRC-001
title: MotionCore design precis
project: MotionCore
doc_type: Design precis
version: "0.7"
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
  change: Populate to TRL 2 (architecture, components, interface draft, first-order numbers, safety, open questions)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3. Design choices adopted for TRL 3 pending Amish's review (MTC-DDR-001); motor costed to hosts; numbers checked against MTC-CAL-001; two CAN buses, precharge closure at 0.6 s, fuse and contactor criteria; model, drawing MTC-DWG-001 and media refreshed
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002). Input 20 to 60 V, controller overvoltage fault 66 V, fuses rated 60 V DC or more, module mass limit 2.0 kg, XT90 provisional pending a sealed-connector evaluation; TRL 3 engineering proposals confirmed
- version: "0.5"
  date: '2026-10-01'
  author: Amish Chadha
  change: Constructable design (MTC-DDR-003, Draft, open for Amish's review). Finned tube on a floor plate, sockets through the end wall, M8 speed socket, bench rig for the prototype; size, mass and cost updated; budget as a value-engineering target
- version: "0.6"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Decisions of 2026-10-02: MTC-DDR-003 accepted; interface v0.2; economizer; sealed connector rule; dual-motor and brushed hosts; license review timing"
- version: "0.7"
  date: '2026-10-02'
  author: Amish Chadha
  change: 'Interface v0.2 issued (speed socket, pin-out, host arrangements); coil economizer in the design; R2 and R9 met on paper; figures per MTC-CAL-001 v0.5'
---

# MotionCore design precis

## Summary

MotionCore is a finned aluminum module, 240 x 168 x 69 mm, that sits between a host's battery pack and its motor. Inside are an open VESC-class motor controller, a small safety supervisor board, a DC contactor and a precharge and fuse block. Outside, one keyed connector set on its end wall links it to a named reference 250 W geared hub motor, a twin-channel emergency stop, two brake switches, a key and throttle pod and an independent speed sensor. The emergency stop opens the contactor through a hardwired loop, so it works even if both processors fail. The speed limit is held twice: once in the controller and once in the supervisor, which reads its own sensor.

The TRL 3 sizing note (MTC-CAL-001) gives, on paper: 6.9 A from a SwapCell pack in the reference case, about 47 °C on the case, motor power removed within 74 ms of an e-stop (worst case), and an estimated MotionCore kit cost of USD 297 against a value-engineering target of USD 300 (USD 3 under), with the USD 70 reference motor costed to each host. The module weighs about 1.92 kg, inside the 2.0 kg limit Amish set in place of 1.5 kg (R12 met, 0.08 kg margin), and the 350 W heavy case on a 24 V pack stays under the 60 °C case limit (about 55.6 °C) because a coil economizer holds the contactor at about 1 W (R9 met on paper, in shade). The design was made buildable in MTC-DDR-003 (Draft, open for Amish's review) without changing what it does; the prototype build plan is MTC-BLD-001. The design choices below were decided by Amish on 2026-09-25, going with the recommendations (MTC-DDR-001 and MTC-DDR-002).

![MotionCore concept](../media/hero.png)

*Figure 1. Reference kit laid out on a bench: module (center), reference hub motor (left), e-stop station, key and throttle pod and brake switches (right). Massing-plus model, not for fabrication.*

## How it works

1. **Power up.** The pack connects through an anti-spark plug and the main fuse. The supervisor, fed from the pack through its own 18 to 75 V buck, closes the precharge path, waits six time constants (0.6 s) and checks that the controller reports at least 90 % of the pack voltage; only then may the contactor close. On a SwapCell pack the supervisor first sends the SwapCell host heartbeat (host type 0, vehicle, mode 2).
2. **Enable.** The contactor coil is powered through the safety loop: e-stop channel A, the enable key and a supervisor-controlled switch, all in series. E-stop channel B goes to the supervisor as a separate input. The supervisor closes its switch only if the throttle reads zero, both brake switches are released, the controller reports no fault on CAN and the BMS reports no fault. This gives R4: no automatic restart.
3. **Drive.** The host's command (throttle, pedal-assist sensor or CAN set-point from a host computer) goes to the supervisor, which passes a limited command to the controller over an internal CAN bus. The controller runs the motor with its own current, temperature and speed limits. Its battery current limit is set to the lower of the host setting and the pack's allowed discharge current.
4. **Watch.** The supervisor times the pulses from a magnet ring on the wheel hub (item 12), independent of the controller's own speed estimate. It also watches the brake switches, command timeouts, temperatures and the BMS fault frames on the external CAN bus.
5. **Stop.** A brake switch or a minor fault sets the controller command to zero within 200 ms (R5, R7). Overspeed, a failed controller heartbeat or any safety-loop fault opens the contactor (stop category 0 in IEC 60204-1 terms). Pressing the e-stop opens the coil circuit directly, without software, and at the same time tells the supervisor to command zero current. A host with a spring-applied brake has that brake powered from the same loop, so it clamps when the loop opens.

![Exploded view](../media/exploded.png)

*Figure 2. Exploded view. Numbers match `bom/bom.csv`.*

## Main components

*Table 1. Main components. Item numbers match the BOM and Figure 2.*

| Item | Component | Role |
| --- | --- | --- |
| 1 | Reference hub motor, 250 W geared | Named reference motor in the interface; costed to each host, which may substitute another motor within R2 |
| 2 | Motor controller, VESC class, 75 V stage | Field-oriented control, current and temperature limits, speed limit, CAN; overvoltage fault set to 66 V |
| 3 | Safety supervisor board | Microcontroller with two CAN buses, 18 to 75 V buck for the coil and logic, independent speed input, throttle, brake and e-stop channel B inputs, contactor enable switch, precharge switch, fault log |
| 4 | Main DC contactor, 100 A | Removes all power to the controller on e-stop or fault; coil in the safety loop; breaks at least 50 A at 60 V DC; releases within 50 ms with a 24 V Zener suppressor |
| 5 | Precharge and main fuse block | 100 Ω precharge resistor and switch; main fuse rated 60 V DC or more: 20 A for 36 and 48 V hosts, 40 A for 24 V hosts |
| 6 | Enclosure: finned tube and floor plate | Heat sink for the controller: a cut length of finned extrusion on a 3 mm floor plate; four M6 rivet nuts on a 180 x 100 mm pattern (MTC-DDR-003) |
| 7 | Lid and lid gasket | Flat 3 mm lid on a 1 mm EPDM gasket, four screws into the corner ports |
| 8 | Connector set and vent | Power in, motor, safety loop and command sockets through the end wall; M8 speed sensor socket in the side wall; membrane vent |
| 9 | E-stop station, twin NC | Red mushroom head on yellow, two normally closed contact blocks, twist release |
| 10 | Brake levers with interlock switches (pair) | Normally closed switches in each brake lever (a host may use its own lever or pedal switches) |
| 11 | Key switch and throttle pod | Enable key (reset after a stop) and a hall-effect throttle |
| 12 | Independent speed sensor | Magnet ring and Hall pickup, read only by the supervisor |
| 13 | Wiring harness, keyed connectors | Pre-made leads from the sockets to each device; 4 mm² pack leads for 24 V hosts |
| 14 | Pads, rivet nuts, standoffs and fixings | Rubber pads on the host mounting points, rivet nuts, standoffs, thermal pad, screws |

![Cutaway](../media/cutaway.png)

*Figure 3. Cutaway through the module: supervisor board on standoffs above the controller (left), contactor (center) and precharge and fuse block (right).*

### Interface (MotionCore interface v0.2)

*Table 2. Connector set (item 8). Interface v0.2 was issued on 2026-10-02 (decided by Amish, MTC-DDR-003 A1): the four sockets of v0.1 (decided 2026-09-25, MTC-DDR-001 item 6) in the +X end wall, seen from the socket side, plus an M8 4-pin speed socket in the side wall. The power connector is a sealed single-pole pair, part to be chosen (MTC-DDR-004); the XT90 shown is for the bench prototype only.*

| Connector | Type | Lines |
| --- | --- | --- |
| Power in | XT90 anti-spark plug (bench prototype only; sealed single-pole pair to follow, MTC-DDR-004) | Pack positive and negative, 20 to 60 V |
| Motor | 9-pin waterproof e-bike motor plug | Three phases, Hall sensors, motor temperature |
| Safety loop | M12 8-pin A-coded | E-stop channels A and B, brake switches A and B, enable key, brake coil output |
| Command | M12 5-pin B-coded, so it cannot mate with the safety loop | Throttle or pedal-assist, CAN high and low (external bus, 250 kbit/s), 5 V, ground |
| Speed | M8 4-pin A-coded, in the side wall | 5 V, ground, speed pulses from the independent speed sensor |

*Table 2a. Pin-out of the three signal sockets (as build plan Table 3).*

| Socket | Pin | Line |
| --- | --- | --- |
| Safety loop (M12, 8-pin A) | 1 | Loop supply, 12 V out to e-stop channel A |
| | 2 | Loop return, after e-stop channel A and the key, to the contactor coil |
| | 3 | E-stop channel B (to ground when the e-stop is not pressed) |
| | 4 | Brake switch A (to ground when the lever is released) |
| | 5 | Brake switch B (to ground when the lever is released) |
| | 6 | Brake coil output, 12 V, for a host's spring-applied brake; live only while the loop is closed |
| | 7 | Ground |
| | 8 | Not connected |
| Command (M12, 5-pin B) | 1 | +5 V for the throttle |
| | 2 | Throttle signal, 0.8 to 4.2 V |
| | 3 | Ground |
| | 4 | CAN high, external bus |
| | 5 | CAN low, external bus |
| Speed (M8, 4-pin A) | 1 | +5 V |
| | 2 | Not connected |
| | 3 | Ground |
| | 4 | Speed pulses |

The module mounts on four M6 studs on a 180 x 100 mm pattern through rubber isolation pads (drawing MTC-DWG-001). The command connector carries the external CAN bus to a SwapCell pack or a CellGuard BMS; the controller sits on a separate internal bus. The SwapCell INTERLOCK coding resistor belongs in the host's pack receptacle, not in MotionCore. Interface v0.2 has five sockets, which is one more than v0.1: CargoMule, the first host, is told of the speed socket (see the review note).

*Host arrangements (decided 2026-10-02).* Dual-motor hosts such as PalletPilot fit two controllers on one supervisor, with one safety loop and one contactor feeding both controllers. Brushed-motor hosts such as StepClimber use the VESC-class controller's DC motor mode, and need a different power stage only if the motor needs more current than the controller is rated for.

## Numbers (MTC-CAL-001)

All numbers are paper estimates printed by `docs/04-calcs/sizing.py`; nothing is measured.

### Currents and fuse

At 250 W shaft power the pack supplies about 322 W: 6.9 A at 46.8 V (SwapCell) and 8.4 A at 38.4 V (CargoMule's 12S LiFePO4 pack). The heavy case, 350 W on 25.6 V, draws 17.7 A, and 22.9 A at 20 V. For 750 W over 10 s the pack delivers 21.9 A on SwapCell and 40.9 A on 8S LiFePO4. A 20 A fuse suits 36 and 48 V hosts and a 40 A fuse suits 24 V hosts, both rated for 60 V DC or more with at least 1 kA breaking capacity (prospective short-circuit currents are about 470 to 860 A for the three packs calculated; a CellGuard 16S pack is to be checked once its resistance is known). The 100 A contactor has a wide margin on continuous current; its selection criteria are breaking at least 50 A at 60 V DC and releasing within 50 ms.

![Power flow](../media/flow.png)

*Figure 4. Estimated power flow at 250 W shaft output on a SwapCell pack (MTC-CAL-001).*

### Emergency stop timing

The e-stop contacts open the coil circuit directly. With a 24 V Zener across the coil, the modeled time to remove motor power is about 37 ms; using the 50 ms release limit that the contactor must meet, the worst case is about 74 ms, inside the 100 ms target of R3. In 74 ms a host at 25 km/h (6.9 m/s) travels about 52 cm and a walk-behind machine at 1.5 m/s about 11 cm. After that the host stops on its own brakes. A plain diode suppressor would lengthen the release; the Zener is part of the design.

### Precharge

With about 1,000 µF of bus capacitance and a 100 Ω resistor, the time constant is 0.1 s. The contactor closes after 0.6 s, when the residual difference is under 0.14 V and the closure current is at most 1.3 A. The peak precharge current is 0.55 A and the resistor absorbs about 1.5 J per start. A 1 s timeout protects the resistor if the bus is shorted.

### Thermal

The enclosure sheds about 1.16 W per kelvin of rise in still air (clear anodized, shaded).

- **Reference case:** about 6.5 W of heat in steady state (controller 4.2 W, auxiliary supply and held coil 1.9 W, power path 0.4 W at minimum pack voltage): about 47 °C at 40 °C ambient. R9 met.
- **Heavy case at 350 W:** about 16.5 W, about 55.6 °C on the walls and 56.9 °C on the floor plate, which joins the finned tube through a sealant film (MTC-CAL-001 v0.5). Met with about 4 K of margin on the walls, which would go if the controller runs hotter than modeled (62 to 68 °C in the sensitivity cases); R9 is **met on paper**, in shade. At 500 W the case would reach about 65 °C, which is why the heavy case is derated.
- **Coil economizer.** The contactor coil takes 4 W and was about half of the reference-case heat. An economizer module on the supervisor carrier board (BOM line 3), decided on 2026-10-02, applies full voltage for 0.5 s and then holds the coil at about 1 W. It is wired so the safety loop breaks the coil supply upstream of it, so a stop still drops the contactor within the 50 ms the e-stop timing assumes; its output capacitor is limited to 100 uF and the 74 ms worst case includes it.

### Speed sensing

With eight magnets and a 20 in wheel (1.57 m circumference), the supervisor sees about 7.6 pulses per second at 1.5 m/s and about 35 at 25 km/h. It times each pulse period rather than counting pulses, because a count over 0.5 s is too coarse at walking pace. Magnet placement jitter of about 2 % leaves a fivefold margin to the 10 % overspeed threshold, and a sustained overspeed opens the contactor in about 0.6 to 0.7 s.

### CAN and bus voltage

The internal bus (supervisor and controller, 500 kbit/s) runs at about 11 % load and the external bus (pack or BMS, 250 kbit/s) at about 3 %. Regeneration is off unless a host enables it, in which case the supervisor requests SwapCell mode 4 with a host charge limit. The controller's overvoltage fault sits at 66 V, above a full CellGuard 16S pack (58.4 V); if the contactor opens during regeneration it keeps the bus near 67.8 V, inside its 75 V rating. Direct-drive motors must not be pushed beyond about 1.25 times their no-load speed at 60 V without a bus clamp.

### Size, mass and cost

- Module: 240 x 168 x 69 mm; about 1.92 kg, of which the enclosure metal is about 1.0 kg. R12 (2.0 kg, relaxed from 1.5 kg by MTC-DDR-002) is met with 0.08 kg of margin. Kit: about 5.3 kg with the reference motor, 2.9 kg without.
- Cost: value-engineering target USD 300. Estimated cost of the constructable MotionCore kit (BOM items 2 to 14): USD 297 (USD 3 under the target, including USD 4 for the coil economizer module); the reference motor adds USD 70 and is costed to each host, and the prototype's bench rig USD 35 (`bom/bom.csv`).

## Key design choices

All choices below were decided by Amish on 2026-09-25, going with the recommendations (MTC-DDR-001, MTC-DDR-002).

1. **VESC-class controller rather than a custom power stage.** It is open, widely sold, already handles DC, BLDC and FOC motors and has CAN. The drawback is that it has no separate safety channel, which the supervisor and contactor provide.
2. **Contactor as the power-removal element.** A DC contactor is cheap, visible and testable with a multimeter. Safe Torque Off on the gate drivers would be faster and wear-free but needs a custom controller.
3. **Separate supervisor with its own speed sensor.** This gives two independent channels for speed limiting, following the structure of ISO 13849-1 Category 3 without claiming a performance level.
4. **Stop category 0 by default.** Removing power is simplest to verify. Category 1 (brake electrically, then open the contactor) is a per-host option for heavier hosts.
5. **Wide input range (20 to 60 V).** One module serves 24, 36 and 48 V hosts, including CellGuard's 16S LiFePO4 packs at 58.4 V full; DustRunner's 12.8 V system stays out of scope.
6. **Motor as a named reference part, costed to hosts.** The interface names the reference motor, but the USD 300 value-engineering target covers the module and devices only.
7. **Supervisor as SwapCell host and CellGuard reader.** The supervisor sends the SwapCell heartbeat and removes torque on a BMS fault.
8. **Heavy case derated to 350 W on 24 V packs.**
9. **Separate firmware.** Unmodified GPL-3.0 VESC firmware on the controller and MIT supervisor firmware on its own processor, linked only by CAN.

10. **Module mass limit 2.0 kg.** The enclosure stays as drawn, because it is the heat sink and R9 depends on it.
11. **TRL 3 engineering rules from MTC-CAL-001.** Two CAN buses on the supervisor, precharge closure at 0.6 s with a 90 % bus check, fuses rated for the full DC range with 1 kA breaking capacity, 4 mm² pack leads for 24 V hosts and a 24 V Zener coil suppressor. The fuse rating became 60 V DC and the controller overvoltage fault 66 V (instead of 58 V and 60 V) when R1 was raised to 60 V.
12. **Sealed power connector evaluated (MTC-DDR-004).** The XT90 stays in the model and drawing as the bench prototype's part until a sealed connector is chosen.

Decisions are recorded in [decisions/](decisions/).

## Safety

> **Safety:** MotionCore drives moving machinery from a lithium pack. Guard all rotating parts, test the emergency stop before every run and limit speed during development. The pack can deliver several hundred amperes into a short circuit (about 470 to 860 A for the host packs considered): fuse it with a fuse rated for the full DC voltage, use the anti-spark connector, and never work on the module with the pack connected. Bus capacitors can hold charge after disconnection; wait and measure before touching the board. The enclosure can reach about 50 to 60 °C in hot conditions, more in direct sun. Opening a contactor under DC load can arc; use a contactor rated for DC breaking at the full pack voltage. Lithium cells can overheat, vent and burn: use packs with a BMS, fuse every pack and never leave a first build charging unattended.

- **Unverified safety function.** Until tested at TRL 4, which is on hold, the e-stop timing, overspeed trip and restart inhibit are paper claims. First runs should be on a bench with the wheel off the ground and a second person at the e-stop.
- **Coasting after a stop.** A category 0 stop removes drive power but does not brake. The host must have brakes that stop it unpowered, and walk-behind hosts need spring-applied brakes.
- **Back-EMF.** A direct-drive motor pushed faster than about 1.25 times its no-load speed (at 60 V) can raise the bus above 75 V through the controller's MOSFET body diodes, even with the contactor open. Geared hubs with a freewheel avoid this; direct-drive hosts need a speed limit or a bus clamp.
- **Configuration errors.** The speed limit depends on the wheel circumference and magnet count stored in the supervisor. A wrong value moves the limit; the fault chart must say so.
- **Misuse of the interface.** If the safety loop is bridged with a jumper, every protection is lost. The loop connector is keyed and the fault chart must say so plainly.
- **No certification.** MotionCore is a research prototype. It is not certified to ISO 13849, IEC 60204-1, EN 15194 or any vehicle rule, and it does not make a host compliant.

## Open questions

- Dual-motor hosts (PalletPilot): decided 2026-10-02, two controllers on one supervisor, with one safety loop and one contactor feeding both, so a stop removes torque from both wheels at once.
- Brushed motors (StepClimber): decided 2026-10-02, the controller's DC motor mode; a different stage only if StepClimber's motor needs more current than the controller is rated for.
- Which sealed power connector replaces the unsealed XT90 (R10): the paper evaluation is written (MTC-DDR-004); it recommends an industrial IP67 single-pole pair, two receptacles with different key coding, and chooses no part, because the rule (keyed, IP67 when mated, 40 A or more continuous at 60 V DC, no exposed live contacts on the pack side) has to be checked against a named part's datasheet at the parts purchase. The XT90 stays for the bench prototype only; R10 stays at risk.
- Contactor coil economizer: decided 2026-10-02 and now in the design: a module on the supervisor carrier board (BOM line 3, USD 4), wired after the safety loop's break in the coil supply; heavy case 55.6 °C on the walls instead of 58.4 °C (MTC-CAL-001 v0.5).
- Whether a pack in SwapCell legacy discharge accepts a heartbeat and moves to mode 2 without opening its output; raised with SwapCell.
- License boundary between the VESC firmware (GPL-3.0) and the MIT supervisor firmware: the short written review is done (MTC-DDR-005), with a firmware readme to be written before any firmware is published; a lawyer only if a commercial partner will ship the module (decided 2026-10-02).
