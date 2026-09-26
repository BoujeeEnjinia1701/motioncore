---
doc_id: MTC-PRB-001
title: MotionCore problem statement
project: MotionCore
doc_type: Problem statement
version: "0.3"
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
  change: Populate to TRL 2 (problem, users, host projects, context, constraints, prior work, open questions)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3. Budget scope (motor costed to hosts), SwapCell and CellGuard links, first host and input range adopted for TRL 3 pending Amish's review (MTC-DDR-001); CargoMule pack corrected to 12S LiFePO4
---

# MotionCore problem statement

Each vehicle or machine concept in the lab re-specifies the same drive train and safety logic, and small teams rarely have time to get the emergency stop, speed limit and brake interlock right. MotionCore is a shared controller and safety module, with a named reference hub motor and one documented interface, so that each host design inherits a reviewed safety chain instead of inventing its own.

## The problem

Five existing lab designs drive a motor from a lithium pack: CargoMule (a 36 V, 250 W hub motor in a bicycle trailer), PalletPilot (two 24 V hub motors on a pallet jack), StepClimber (a 24 V worm gearmotor on a stair-climbing hand truck), SunSpoke (a 48 V, 250 W hub motor on a roadster bicycle) and DustRunner (12.8 V gearmotors on a panel-cleaning robot). Each one specifies its own controller, fuse, emergency stop, brake cut-off and speed limit, in its own words, with its own gaps. Three problems follow:

1. **Repeated effort.** The same parts (a brushless controller, a contactor, a fuse, a mushroom-head stop button, brake switches) are selected, wired and documented five times, and a fix found in one design does not reach the others.
2. **Uneven safety logic.** The safety function is the part most often left vague. Typical gaps in small builds are an emergency stop that only asks the firmware to stop, a speed limit held in the same controller that could fail, no interlock between the brake and the drive, and a restart that happens by itself when power returns. Machinery standards such as [ISO 13850](https://www.iso.org/standard/59970.html) (emergency stop) and [ISO 13849-1](https://www.iso.org/standard/73481.html) (safety-related control parts) describe how to avoid these, but they are written for industrial teams and are costly to read.
3. **Rising exposure.** Light electric vehicles and small machines are spreading fast. The IEA reports almost 10 million electric two-wheelers sold worldwide in 2025, about 14 % of all two-wheeler sales ([IEA Global EV Outlook 2026](https://www.iea.org/reports/global-ev-outlook-2026/trends-in-other-ev-modes)). In the United States, the Consumer Product Safety Commission estimates about 698,500 emergency department visits linked to micromobility products from 2017 through 2024 and records 533 deaths, 310 of them involving e-bikes ([CPSC, 2017 to 2024 report](https://www.cpsc.gov/s3fs-public/Micromobility_Products-Related_Deaths_Injuries_and_Hazard_Patterns_2017-2024.pdf)). These figures cover all causes, most of them crashes, so they show the scale of exposure rather than a failure rate of drive electronics.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Lab project lead (host designer) | Drop in a drive and safety chain with known limits and a documented interface; spend design time on what is new about the host | Designing a vehicle or machine at TRL 2 to 4 |
| Builder of a host prototype | Wire, configure and test the drive in a garage with hand tools and a multimeter, and know when it is safe to power up | Home or makerspace workshop, first power-up on a bench |
| Operator of a host machine | Stop the machine at once from a clearly marked button; never have it start by itself | Walk-behind machines (pallet jack, stair climber), cargo trailers, bicycles |
| People near the machine | Not be struck by a machine that runs away, over-speeds or restarts | Warehouses, sidewalks, stairwells, farms |
| Maintainer or repairer | Diagnose a fault from a fault log and swap a part without special tools or closed software | Local repair shop or the lab |

### Host projects (first-order envelope)

Table 1 lists the drive needs stated in the host READMEs. MotionCore is sized to cover the first four; DustRunner's 12.8 V system falls outside the 20 to 58 V input range.

*Table 1. Drive needs of existing lab host designs.*

| Host | Pack | Motor | Stop and brake need |
| --- | --- | --- | --- |
| SunSpoke | 48 V SwapCell (about 46.8 V nominal, 54.6 V full) | 250 W geared front hub | Brake cut-off on both levers; pedelec speed cutoff |
| CargoMule | 12S LiFePO4 (38.4 V nominal), 384 Wh | 250 W geared hub, 20 in wheel | Drive cut when the drawbar goes into compression; overrun brakes |
| PalletPilot | 25.6 V LiFePO4, 20 Ah | Two 24 V hub motors with spring-applied brakes | Two hardwired e-stops, safety relay, walking-pace limit |
| StepClimber | 24 V LiFePO4, 10 Ah | 24 V worm gearmotor with spring-applied brake | Stop on tilt; brake holds on stairs |
| DustRunner | 12.8 V LiFePO4 | Two small drive gearmotors | Out of the 20 to 58 V range |

### Operating environment

- **Supply:** LiFePO4 or lithium-ion packs from 8S LiFePO4 (about 25.6 V nominal, 29.2 V full) to 13S lithium-ion (54.6 V full), including the portfolio's SwapCell pack.
- **Power:** 250 W continuous reference, up to 500 W continuous on 24 V hosts; short peaks to about 750 W.
- **Climate:** 0 to 40 °C ambient in the working range, rain and dust on outdoor hosts, vibration from rough roads and stairs.
- **Speeds:** walking pace (about 1.5 m/s, 5.4 km/h) for walk-behind machines; up to 25 km/h for pedal-assist hosts.

## Constraints

- Garage-buildable prototype, $300 or less for the MotionCore kit (module and devices); the reference motor is costed to each host (MTC-DDR-001 item 1).
- Off-the-shelf, openly documented parts: a VESC-class controller ([VESC project](https://vesc-project.com/)), a DC contactor, standard fuses and industrial pushbuttons.
- The emergency stop must work without any firmware: a hardwired loop that opens the main contactor.
- One connector set shared by all hosts; keyed so that the safety loop and the command lines cannot be swapped.
- Compatible with SwapCell interface v0.3 (the supervisor acts as the vehicle host) and the CellGuard BMS where a host uses them (adopted for TRL 3 pending Amish's review, MTC-DDR-001 items 7 and 8).
- Research prototype only. MotionCore does not make a host compliant with any machinery, vehicle or pedelec regulation; each host remains responsible for its own risk assessment.

## Out of scope

- Battery packs and their BMS (SwapCell and CellGuard cover these).
- Host-specific mechanics: wheels, frames, brakes, gearboxes and guards.
- Traction above about 1 kW or systems above 60 V DC.
- Certification to ISO 13849, IEC 61508 or vehicle type approval.
- Autonomy, navigation and obstacle sensing (hosts such as PalletPilot own those layers and feed a stop request into the MotionCore safety loop).

## Prior work

- **VESC.** An open brushless motor controller started by Benjamin Vedder, with open hardware designs and firmware for DC, BLDC and FOC control ([VESC project](https://vesc-project.com/); [firmware, GPL-3.0](https://github.com/vedderb/bldc)). It already has current, temperature and speed (ERPM) limits, CAN bus and a PC tool, and many low-cost variants are sold. It has no separate safety channel.
- **ODrive and SimpleFOC.** Open motor control for robotics ([ODrive](https://odriverobotics.com/); [SimpleFOC](https://simplefoc.com/)). Good for position control; like VESC, they leave the safety chain to the integrator.
- **Machinery safety practice.** [ISO 13850:2015](https://www.iso.org/standard/59970.html) sets the principles for emergency stop design; [IEC 60204-1](https://www.se.com/us/en/faqs/FA122781/) defines stop categories 0, 1 and 2; [ISO 13849-1:2023](https://www.iso.org/standard/73481.html) sets the architecture and performance levels for safety-related control parts. MotionCore borrows their structure (two channels, fail-safe contactor, no automatic restart) without claiming conformity.
- **Pedelec rules.** In the European Union, pedal cycles with assistance up to 250 W that cuts off at 25 km/h are excluded from type approval under [Regulation (EU) No 168/2013](https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX%3A32013R0168); EN 15194 sets the product standard. This sets the default speed cutoff for pedal-assist hosts.
- **Commercial safety relays and drives.** Industrial drives with Safe Torque Off inputs and dual-channel safety relays solve the problem well, at a cost and size that suit factories, not garage prototypes.

## Open questions

At TRL 3 the recommendations on first host, SwapCell heartbeat, stop category and input range were adopted for TRL 3 under Amish's 2026-09-25 instruction, open for his review (MTC-DDR-001): CargoMule is the proposed first adopter, subject to its project's agreement; the supervisor sends the SwapCell heartbeat; category 0 is the default with category 1 as a per-host option; and the range stays 20 to 58 V, so DustRunner stays out of scope. Still open:

- Do the host leads agree to swap their current drive sections for MotionCore, starting with CargoMule?
- Can StepClimber's brushed worm gearmotor run from the VESC DC motor mode, or does it need a different power stage? Proposed, awaiting Amish.
- Should a dual-motor host such as PalletPilot use two controllers on one supervisor, or two modules? Proposed, awaiting Amish.

## User research and co-design

MotionCore's first users are the lab's own host designers, so co-design starts inside the lab.

- [ ] Review Table 1 with each host project and confirm voltage, power, speed and stop needs
- [ ] Walk through the safety loop with a builder who has not seen it and record where it is unclear
- [ ] Ask at least one external maker or repair shop to review the interface and fault chart
- [ ] Revise requirements (MTC-REQ-001) from findings before freezing the interface
