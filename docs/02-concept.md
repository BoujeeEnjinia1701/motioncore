---
doc_id: MTC-PRC-001
title: MotionCore design precis
project: MotionCore
doc_type: Design precis
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
  change: Populate to TRL 2 (architecture, components, interface draft, first-order numbers, safety, open questions)
---

# MotionCore design precis

## Summary

MotionCore is a finned aluminum module, about 250 x 170 x 66 mm, that sits between a host's battery pack and its motor. Inside are an open VESC-class motor controller, a small safety supervisor board, a DC contactor and a precharge and fuse block. Outside, one keyed connector panel links it to a reference 250 W geared hub motor, a twin-channel emergency stop, two brake switches, a key and throttle pod and an independent speed sensor. The emergency stop opens the contactor through a hardwired loop, so it works even if both processors fail. The speed limit is held twice: once in the controller and once in the supervisor, which reads its own sensor. The reference kit costs about $325 in parts (indicative), about 8 % over the $300 budget.

![MotionCore concept](../media/hero.png)

*Figure 1. Reference kit laid out on a bench: module (center), 250 W hub motor (left), e-stop station, key and throttle pod and brake switches (right). Massing model, not for fabrication.*

## How it works

1. **Power up.** The pack connects through an anti-spark plug and the main fuse. The supervisor closes the precharge path, waits until the controller's bus capacitors are charged, and only then may the contactor close.
2. **Enable.** The contactor coil is powered through the safety loop: both e-stop channels, the enable key and a supervisor-controlled switch, all in series. The supervisor closes its switch only if the throttle reads zero, both brake switches are released, the controller reports no fault on CAN and, where fitted, the BMS reports no fault. This gives R4: no automatic restart.
3. **Drive.** The host's command (throttle, pedal-assist sensor or CAN set-point from a host computer) goes to the supervisor, which passes a limited command to the controller. The controller runs the motor with its own current, temperature and speed limits.
4. **Watch.** The supervisor counts pulses from a magnet ring on the motor (item 12), independent of the controller's own speed estimate. It also watches the brake switches, command timeouts and temperatures.
5. **Stop.** A brake switch or a minor fault sets the controller command to zero within 200 ms (R5, R7). Overspeed, a failed controller heartbeat or any safety-loop fault opens the contactor (stop category 0 in IEC 60204-1 terms). Pressing the e-stop opens the coil circuit directly, without software. A host with a spring-applied brake has that brake powered from the same loop, so it clamps when the loop opens.

![Exploded view](../media/exploded.png)

*Figure 2. Exploded view. Numbers match `bom/bom.csv`.*

## Main components

*Table 1. Main components. Item numbers match the BOM and Figure 2.*

| Item | Component | Role |
| --- | --- | --- |
| 1 | Reference hub motor, 250 W geared | Motor for the reference case; hosts may substitute another motor within R2 |
| 2 | Motor controller, VESC class, 75 V stage | Field-oriented control, current and temperature limits, speed limit, CAN |
| 3 | Safety supervisor board | Small microcontroller with CAN, independent speed input, throttle and brake inputs, drive for the contactor enable switch, fault log |
| 4 | Main DC contactor, 60 V class, 100 A | Removes all power to the controller on e-stop or fault; coil in the safety loop |
| 5 | Precharge and main fuse block | Precharge resistor and bypass, main fuse sized per host (20 to 40 A) |
| 6 | Enclosure body, finned aluminum | Heat sink for the controller; mounting |
| 7 | Enclosure lid | Gasketed cover |
| 8 | Connector panel, keyed | Power in, motor, sensors, safety loop and command connectors |
| 9 | E-stop station, twin NC | Red mushroom head on yellow, two normally closed contact blocks, twist release |
| 10 | Brake interlock switches (pair) | Normally closed switches on each brake lever or pedal |
| 11 | Key switch and throttle pod | Enable key (reset after a stop) and a hall-effect throttle |
| 12 | Independent speed sensor | Magnet ring and Hall pickup, read only by the supervisor |
| 13 | Wiring harness, keyed connectors | Pre-made leads from the panel to each device |

![Cutaway](../media/cutaway.png)

*Figure 3. Cutaway through the module: supervisor board on standoffs above the controller (left), contactor (center) and precharge and fuse block (right).*

### Interface draft (MotionCore interface v0.1, proposed)

*Table 2. Connector set on the panel (item 8). Proposed, awaiting Amish.*

| Connector | Type (proposed) | Lines |
| --- | --- | --- |
| Power in | XT90 anti-spark plug | Pack positive and negative, 20 to 58 V |
| Motor | 9-pin waterproof e-bike motor plug, or three 4 mm bullets plus a 6-pin sensor plug | Three phases, Hall sensors, motor temperature |
| Safety loop | M12 8-pin A-coded | E-stop channels A and B, brake switches A and B, enable key, brake coil output |
| Command | M12 5-pin, B-coded or a keyed alternative so it cannot mate with the safety loop | Throttle or pedal-assist, CAN high and low, 5 V, ground |

The command connector also carries CAN to a SwapCell pack or a CellGuard BMS, so the supervisor can read pack faults and, if Amish agrees, send the SwapCell host heartbeat.

## First-order numbers

All numbers are estimates for TRL 2 and will be checked at TRL 3.

### Currents and fuse

At 250 W shaft power with a motor efficiency of about 80 % and controller efficiency of about 95 %, the pack supplies about 333 W (Figure 4). That is about 7.1 A at 46.8 V (SwapCell) and about 9.3 A at 36 V (CargoMule). The heavy case, 500 W on 25.6 V, draws about 500 / 0.75 / 25.6 ≈ 26 A. A 20 A fuse suits 48 V and 36 V hosts; the heavy case needs 40 A. The 100 A contactor has a wide margin on continuous current; its rating for breaking DC under load at 58 V is the figure to check.

![Power flow](../media/flow.png)

*Figure 4. Estimated power flow at 250 W shaft output on a 48 V pack.*

### Emergency stop timing

The e-stop contacts open the coil circuit directly. With a Zener suppressor across the coil, a small DC contactor typically drops out in 20 to 50 ms (assumption, to be confirmed from the chosen part); allowing 10 ms for contact bounce gives about 60 ms, inside the 100 ms target of R3. In 100 ms a host at 25 km/h (6.9 m/s) travels about 0.7 m and a walk-behind machine at 1.5 m/s travels about 0.15 m before drive power is gone. After that the host stops on its own brakes.

### Precharge

Assuming about 1,000 µF of bus capacitance in the controller and a 100 Ω precharge resistor, the time constant is 0.1 s, so the bus reaches 99 % in about 0.5 s. The peak precharge current is 54.6 V / 100 Ω ≈ 0.55 A and the resistor absorbs ½CV² ≈ 1.5 J per start. Without precharge, closing onto the capacitors would draw a spark and an inrush of well over 100 A.

### Thermal

The enclosure has about 0.13 m² of surface including fins. With about 10 W/m²K from natural convection and radiation, it sheds about 1.3 W per kelvin of rise.

- **Reference case:** controller loss about 16 W plus about 4 W from the supervisor, contactor coil and fuse gives about 20 W, a rise of about 15 K, so about 55 °C at 40 °C ambient. R9 met.
- **Heavy case:** controller loss roughly doubles to about 32 W (higher current at lower voltage) for about 35 W in total, a rise of about 27 K, so about 67 °C at 40 °C ambient. **R9 not met.** Options: a contactor coil economizer, forced air, mounting to the host frame as a heat sink, or a lower continuous rating at 24 V.

### Speed sensing

With eight magnets on the ring and a 20 in (about 1.6 m circumference) wheel, the supervisor sees about 7.5 pulses per second at 1.5 m/s and about 35 at 25 km/h. A 10 % overspeed held for 0.5 s spans 4 to 17 pulses, enough to detect it without false trips from single missed pulses.

### Size, mass and cost

- Module: about 250 x 170 x 66 mm including fins and connectors, about 1.3 kg (estimate). Kit with motor and devices: about 4.4 kg.
- Cost: about $325 in parts for the full reference kit, of which the motor is about $70 and the module and devices about $255 (see `bom/bom.csv`). **R14 not met** by about $25.

## Key design choices

All choices below are proposed, awaiting Amish.

1. **VESC-class controller rather than a custom power stage.** It is open, widely sold, already handles DC, BLDC and FOC motors and has CAN. The drawback is that it has no separate safety channel, which the supervisor and contactor provide.
2. **Contactor as the power-removal element.** A DC contactor is cheap, visible and testable with a multimeter. Safe Torque Off on the gate drivers would be faster and wear-free but needs a custom controller.
3. **Separate supervisor with its own speed sensor.** This gives two independent channels for speed limiting, following the structure of ISO 13849-1 Category 3 without claiming a performance level.
4. **Stop category 0 by default.** Removing power is simplest to verify. A category 1 option (brake electrically, then open the contactor) is an open question for heavier hosts.
5. **Wide input range (20 to 58 V).** One module serves 24, 36 and 48 V hosts; DustRunner's 12.8 V system stays out of scope.
6. **Reference motor included in the kit.** Keeps the pitch (motor, controller and safety module) but pushes the kit over budget.

Record each decision, once Amish makes it, as a file in [decisions/](decisions/).

## Safety

> **Safety:** MotionCore drives moving machinery from a lithium pack. Guard all rotating parts, test the emergency stop before every run and limit speed during development. The pack can deliver hundreds of amperes into a short circuit: fuse it at the pack, use the anti-spark connector, and never work on the module with the pack connected. Bus capacitors can hold charge after disconnection; wait and measure before touching the board. The enclosure can reach about 55 to 67 °C in hot conditions. Opening a contactor under DC load can arc; use a contactor rated for DC breaking at the full pack voltage. Lithium cells can overheat, vent and burn: use packs with a BMS, fuse every pack and never leave a first build charging unattended.

- **Unverified safety function.** Until tested at TRL 4, the e-stop timing, overspeed trip and restart inhibit are paper claims. First runs should be on a bench with the wheel off the ground.
- **Coasting after a stop.** A category 0 stop removes drive power but does not brake. The host must have brakes that stop it unpowered, and walk-behind hosts need spring-applied brakes.
- **Back-EMF.** A direct-drive motor pushed faster than its no-load speed can raise the bus voltage through the controller's MOSFET body diodes, even with the contactor open. Geared hubs with a freewheel avoid this; direct-drive hosts need a bus clamp.
- **Misuse of the interface.** If the safety loop is bridged with a jumper, every protection is lost. The loop connector must be keyed and the fault chart must say so plainly.
- **No certification.** MotionCore is a research prototype. It is not certified to ISO 13849, IEC 60204-1, EN 15194 or any vehicle rule, and it does not make a host compliant.

## Open questions for TRL 3

- Contactor part choice: DC breaking rating at 58 V, drop-out time and coil power.
- Controller bus capacitance and regeneration behavior when the contactor opens during braking.
- License boundary between the VESC firmware (GPL-3.0) and the MIT supervisor firmware.
- Whether the supervisor should send the SwapCell host heartbeat, replacing SunSpoke's separate host adapter.
- Dual-motor hosts (PalletPilot): two controllers on one supervisor, or two modules.
- Brushed motors (StepClimber): VESC DC mode or a different stage.
- Thermal fix for the heavy case.
