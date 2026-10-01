---
doc_id: MTC-BLD-001
title: MotionCore prototype build plan
project: MotionCore
doc_type: Build plan
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: First build plan, with pictures by component and step; design made constructable (MTC-DDR-003)
---

# MotionCore prototype build plan

**Plan, not yet built.** How to build the first proof-of-concept prototype, component by component. Building and testing to it is TRL 4 work. Decisions still to be made are kept in the design decisions register ([docs/06-design-decisions.md](06-design-decisions.md)), not here.

## 1. What you are building

![Figure 1. Every component, pulled apart and numbered in build order](05-build-plan/overview.png)

*Figure 1. Every component pulled apart and numbered in build order: the module (1 to 12), then the bench rig and devices (13 to 25).*

The prototype is one MotionCore module bolted to a plywood bench board through its own host mounting points, with the reference hub motor held by its axle in two slotted uprights so the wheel turns clear of the board, an e-stop station screwed beside it and a short handlebar carrying the two brake levers and the key and throttle pod. The module is a finned aluminum tube standing on a floor plate, closed by a gasketed lid, with the motor controller, the contactor, the precharge and fuse block and the safety supervisor board inside and five sockets through its walls. Figure 1 shows the 25 components in the order you make or fit them. Ten are made in a small workshop: the floor plate, the finned tube (cut and drilled), the supervisor carrier board, the lid and its gasket, the bench board, the motor uprights, their feet, the Hall pickup bracket, the bar posts and the handlebar stub; the harness is made up from bought leads. Everything else is bought and fitted. The work is cutting and drilling aluminum plate, bar, angle and tube, tapping, setting rivet nuts, cutting plywood, and wiring bought modules with crimped and soldered joints. The parts cost about USD 293 for the MotionCore kit, plus USD 70 for the reference motor and USD 35 for the bench rig, from the bill of materials.

> **Safety:** MotionCore switches a battery that can drive several hundred amperes into a short circuit and turns a motor. Build and wire the module with no battery in the room; keep the main fuse out until section 6 says otherwise; power it first from a current-limited bench supply; and never run the motor unless the wheel is clear of everything, a second person is at the e-stop and the e-stop has been checked that day. Cut aluminum edges are sharp: deburr everything. Wear eye protection for all cutting, drilling and soldering.

## 2. What changed to make it buildable

The concept showed what MotionCore does; some of its parts could not be made, fixed or connected as drawn. Each change below keeps what the module does, and all of them are recorded in decision record MTC-DDR-003, open for Amish's review.

*Table 1. Changes from the concept.*

| Component | The concept had | The buildable design has | Why |
| --- | --- | --- | --- |
| Enclosure body | An extruded box with a closed floor and vertical fins, which an extrusion cannot have | A 56 mm length of finned enclosure extrusion standing on a separate 3 mm floor plate, joined by conductive sealant and four screws into the corner ports (Figures 2 to 4) | One wall thickness and vertical fins, as the concept; the controller still sits on aluminum bolted to the fins |
| Lid | A lip inside the walls that clashed with the corner ports, and no fixing | A flat lid on a 1 mm gasket, four screws into the same ports (Figures 11, 12) | Ports take both floor and lid screws |
| Host mounting points | M6 inserts in cast bosses | Closed-end M6 rivet nuts in the floor plate, rubber pads under their flanges (Figure 5) | Same four M6 on 180 x 100 mm; the floor stays sealed |
| Supervisor board | Standoffs standing inside the controller | A wider board (85 x 88 mm) with its standoffs beside the controller (Figure 9) | No overlap; 10 mm of air over the controller |
| Connector panel | A plate outside a closed wall, connectors closer than their own flanges | Sockets straight through the end wall, spaced so every flange and nut has room (Figures 3, 6) | Buildable, and the power socket can be swapped by recutting one hole |
| Precharge and fuse block | In the path of the socket bodies | Beside the contactor | Room behind the end wall for sockets and wires |
| Speed sensor | No socket and no free pins | Its own small M8 socket between two fins (Figure 3) | Brings the sensor in without growing the module |
| Vent | Listed but not drawn | Adhesive membrane vent on the far end wall | Keeps the module inside 250 mm long |
| Speed ring and pickup | Floating beside the motor | Ring bolted to the motor's disc mount; pickup on a bracket on the motor upright (Figure 17) | Real fixings, 3.5 mm sensing gap |
| Reference kit layout | Loose on a bench, motor standing on its shell | A bench rig: board, motor uprights, bar posts and handlebar (Figures 13 to 21 and steps 8 to 16) | The wheel can turn clear of the board for first runs |
| Brake switches | Blocks with no mounting | Brake levers with built-in switches, clamped on the handlebar | Real parts that clamp where a host's controls go |
| Harness | Leads routed to the wrong devices | One lead per socket, with the key and brake levers on the safety loop | Matches the interface |

## 3. Making the components

Make and check each component before the assembly step that needs it. Sizes are in millimetres. The module's **connector end** carries the four main sockets; the **far end** is opposite it. Its **socket side** is the long side with the small speed socket; the **plain side** is the other. Workshop tolerance is 0.5 mm unless a step says otherwise; drawings do not carry tolerances before TRL 4.

### 3.1 Floor plate

![Figure 2. Making sketch of the floor plate](../cad/drawings/MTC-DWG-101.png)

*Figure 2. Floor plate making sketch (MTC-DWG-101).*

![Figure 2a. Floor plate hole positions](05-build-plan/floor-holes.png)

*Figure 2a. Every hole, measured from the far end and from the socket side.*

**What it is and what it is made from.** The bottom of the module and the plate everything inside is fixed to; it carries the four host mounting points and conducts the controller's heat into the finned walls. Aluminum plate 3 mm thick, 6061-T6, cut to 220 x 140 mm.

**How to make it.**

1. Cut the blank to 220 x 140 mm, square, and deburr. Mark the far end and the socket side on the top face.
2. Mark every hole from Figure 2a, measuring from the far end and from the socket side.
3. Rivet nut holes: four 9.0 mm holes at 20 and 200 from the far end, 20 and 120 from the socket side. Check the size against the rivet nut's datasheet before the last drill.
4. Corner screw holes: four 4.5 mm holes, 7.5 in from each end and each side. Countersink from the bottom face to 8.4 mm across so M4 countersunk heads sit flush.
5. Controller holes: four, drilled 2.5 mm and tapped M3 through, at 14 and 106 from the far end, 39 and 91 from the socket side. Check the pattern against your controller's mounting holes first and move these to suit.
6. Supervisor standoff holes: four, drilled 2.5 mm and tapped M3 through, at 30 and 90 from the far end, 26 and 102 from the socket side.
7. Contactor foot holes: two, drilled 3.3 mm and tapped M4 through, at 120 and 180 from the far end, 70 from the socket side.
8. Fuse block holes: two, drilled 3.3 mm and tapped M4 through, at 130 and 172 from the far end, 117 from the socket side.
9. Deburr every hole on both faces and clean off all chips and oil.

**How it fits the parts next to it.** The tube stands on its top face, flush with its edges all round, on a thin film of thermally conductive sealant, and four M4 countersunk screws come up through the corner holes into the tube's corner ports (Figure 4). The rivet nuts go in from below (Figure 5). The controller, standoffs, contactor and fuse block sit on its top face on screws into the tapped holes.

**Check before moving on.** Lay the tube on the plate: the four corner holes line up with the four ports, and every edge is flush within 0.5 mm.

### 3.2 Finned tube

![Figure 3. Making sketch of the finned tube](../cad/drawings/MTC-DWG-102.png)

*Figure 3. Finned tube making sketch (MTC-DWG-102).*

![Figure 3a. Socket hole positions](05-build-plan/wall-holes.png)

*Figure 3a. Holes in the connector end wall, seen from outside, and the speed socket hole in the socket side.*

**What it is and what it is made from.** The four walls and the fins of the module, and its heat sink. A bought finned enclosure extrusion, 220 x 140 mm outside the walls, 3 mm walls, eleven 3 x 14 mm fins on a 19 mm pitch along each long side and four screw ports in the inside corners, cut to 56 mm long so the fins stand upright.

**How to make it.**

1. Cut 56 mm off the extrusion with a fine-toothed saw, square to its length. Face both cut ends flat on a sheet of abrasive paper on a flat plate; they carry the floor and lid seals.
2. Tap the four corner ports M4, 12 mm deep from both ends.
3. Mark the connector end wall from Figure 3a. All four socket centres are 28.5 above the bottom edge, measured along the wall from the socket side's outer face: power socket at 28, motor at 56, safety loop at 83, command at 109.
4. Power socket: a 12 wide by 22 tall slot, centred at 28. Chain drill inside the outline, file to the line, then drill two 3.2 mm holes on its centre line, 14.5 above and below its centre, for the frame screws.
5. Motor socket: a 20.5 mm hole at 56. Safety loop and command: 16.5 mm holes at 83 and 109, each with four 3.2 mm holes on a 15 mm square round it. Use a step drill; check each size on the socket's datasheet before the last step.
6. Speed socket: an 8.5 mm hole in the socket side, between the first and second fins from the far end, 24.5 from the far end and 18 above the bottom edge.
7. Vent: a 5 mm hole in the far end wall on its centre line, 43 above the bottom edge.
8. Deburr every hole inside and out and clean the tube.

**How it fits the parts next to it.**

![Figure 4. Joint 1: floor plate to tube](05-build-plan/joint-01.png)

*Figure 4. The tube's wall and corner port stand on the floor plate; the screw pulls them together through the sealant film.*

The tube's bottom end sits flat on the floor plate, edges flush. Spread a thin, even film of thermally conductive silicone sealant on the floor plate where the walls and ports land, keeping it out of the port holes, fit the four screws and tighten them evenly; wipe off what squeezes out. The film seals the joint and carries the controller's heat into the fins; it should end up about 0.2 mm thick. The lid seals on the top end (Figure 12).

**Check before moving on.** The tube stands square on a flat plate without rocking; each socket and its screws fit their holes; no hole breaks into a fin or a port.

### 3.3 Rivet nuts and pads

![Figure 5. Joint 2: host mounting point](05-build-plan/joint-02.png)

*Figure 5. One of the four mounting points, cut through the bolt: board, rubber pad, rivet nut flange, floor plate and the closed rivet nut body inside.*

**What they are.** Four M6 closed-end steel rivet nuts for a 0.5 to 3 mm grip, and four rubber isolation pads 16 mm across and 3 mm thick with 6.5 mm holes. They are the host mounting interface: four M6 threads on a 180 x 100 mm rectangle.

**How to fit them.** Put each rivet nut in its hole from below, flange against the bottom face, and set it with an M6 rivet nut tool until it pulls tight on the plate and cannot turn. The closed end keeps water out of the module. The pads go between the flange and the host (here the bench board) when the module is mounted (step 8).

**Check before moving on.** Each rivet nut takes an M6 bolt by hand for its full thread and does not spin under a spanner.

### 3.4 Sockets and vent

![Figure 6. Joint 4: sockets from inside](05-build-plan/joint-04.png)

*Figure 6. The sockets in the connector end wall, seen from inside: frames and flanges outside, nuts inside.*

**What they are.** The power socket (XT90 anti-spark socket in a two-screw panel frame), the 9-pin waterproof motor socket (nut mounted), the safety loop socket (M12 8-pin A-coded) and the command socket (M12 5-pin B-coded, so the two M12 plugs cannot be swapped), both on 20 mm four-screw square flanges; the M8 4-pin speed socket; and a 20 mm adhesive membrane vent.

**How to fit them.** Each socket goes in from outside with its sealing ring between its flange and the wall. The power socket's frame and the M12 flanges are held by M3 screws with nuts inside; the motor socket by its own nut inside, tightened to the maker's torque. The speed socket goes in from outside with its nut inside. Stick the vent patch over the 5 mm hole on a clean, dry wall, pressing it down all round. The power socket is the XT90 for this prototype; it is not sealed, so keep the module dry.

**Check before moving on.** Every socket seats flat on its sealing ring; the M12 coding keys point the same way; nothing inside comes closer than 3 mm to a corner port.

### 3.5 Controller, contactor and precharge and fuse block

![Figure 7. Step 5 picture: contactor and fuse block](05-build-plan/step-05.png)

*Figure 7. The contactor and the precharge and fuse block on the floor plate beside the controller.*

**What they are.** The motor controller is a VESC-class controller with a 75 V power stage, CAN and about 1,000 µF of bus capacitance, with its overvoltage fault set to 66 V. The contactor is a sealed 100 A DC contactor with a 12 V coil and a mounting foot, able to break at least 50 A at 60 V DC and release within 50 ms with a 24 V Zener diode across its coil. The precharge and fuse block is a 100 ohm, 10 W aluminum-clad resistor and a sealed holder for a blade fuse rated 60 V DC or more with at least 1 kA breaking capacity: 20 A for 36 and 48 V packs, 40 A for 24 V packs.

**How to fit them.** The controller sits on a 1 mm thermal pad, trimmed 2 mm inside its base, on four M3 screws into the tapped floor holes. The contactor stands on its foot on two M4 screws. The precharge and fuse block sits on the plain side beside the contactor on two M4 screws. Put a drop of thread sealant on every screw that goes into the floor, and choose lengths that end flush with the floor's bottom face.

**Check before moving on.** Nothing rocks; the controller's base is flat on its pad; the contactor's terminals face the socket side with room for a spanner.

### 3.6 Supervisor carrier board

![Figure 8. Making sketch of the supervisor carrier board](../cad/drawings/MTC-DWG-103.png)

*Figure 8. Supervisor carrier board making sketch (MTC-DWG-103).*

**What it is and what it is made from.** The safety supervisor, built for the prototype from bought modules on a carrier board. FR4 perforated board 1.6 mm thick, 2.54 mm pitch, cut to 85 x 88 mm.

**How to make it.**

1. Cut the board to 85 x 88 mm. Drill four 3.2 mm holes 15 and 75 from the edge nearest the far end, 6 and 82 from the socket-side edge.
2. Lay out the modules of Table 2 inside a 73 x 68 mm area in the middle, so they clear the lid by 10 mm and the four standoff screws.
3. Fix each module with M2.5 or M3 screws and nylon spacers, or solder its header pins to the board.
4. Wire them as Figure 10 shows, with the signal pins of Table 3.

*Table 2. Modules that make up the prototype supervisor.*

| Module | What to buy |
| --- | --- |
| Microcontroller | STM32G0B1-class board with two CAN controllers and a USB socket for the fault log |
| CAN transceivers | Two 3.3 V CAN transceiver modules: one for the internal bus to the controller (500 kbit/s), one for the external bus to the pack or battery management system (250 kbit/s) |
| Auxiliary supply | Buck converter, 18 to 75 V in, 12 V out, 10 W, for the contactor coil and the logic |
| Coil switch | Logic-level N-channel MOSFET module, at least 2 A and 60 V, in series with the coil loop |
| Precharge switch | Logic-level MOSFET module, at least 1 A and 75 V, in series with the precharge resistor |
| Input conditioning | Opto-isolated or resistor-divider inputs for e-stop B, both brake switches and the speed pickup; a 0.8 to 4.2 V analog input for the throttle |

**How it fits the parts next to it.**

![Figure 9. Joint 3: supervisor board over the controller](05-build-plan/joint-03.png)

*Figure 9. The board stands on four 35 mm standoffs beside the controller, with 10 mm of air above the controller.*

The standoffs screw into the floor's tapped holes and the board onto the standoffs with four M3 screws.

**Check before moving on.** The board is flat; no solder tail underneath is longer than 2 mm; with nothing connected, each supply rail reads open to ground.

#### 3.6.1 Wiring inside the module and the connector pins

![Figure 10. Block-level wiring](05-build-plan/wiring.png)

*Figure 10. Block-level wiring with wire sizes. No circuit board is laid out at this stage; bought modules stand in for the supervisor board.*

Wire it like this, with stranded copper, crimped ring lugs on studs and ferrules on screw terminals:

1. Power socket positive to the main fuse holder, fuse holder to one contactor terminal, the other contactor terminal to the controller's battery positive: 4 mm² (12 AWG).
2. Power socket negative to the controller's battery negative: 4 mm².
3. Precharge resistor and the supervisor's precharge switch in series, across the contactor's two terminals: 1 mm² (18 AWG).
4. The supervisor's auxiliary supply from the fuse side of the contactor and from battery negative: 0.5 mm² (20 AWG).
5. Coil loop: the supervisor's 12 V out to safety loop pin 1; safety loop pin 2 back to the contactor coil; the coil's other end through the supervisor's coil switch to ground: 0.5 mm². Fit the 24 V Zener diode across the coil, cathode to the positive end.
6. Motor socket to the controller: three phases 4 mm²; Hall sensors, their 5 V and ground, and the motor temperature 0.25 mm² (24 AWG), pin for pin as the motor's maker lists them.
7. Internal CAN between the supervisor and the controller: twisted pair 0.25 mm², with a 120 ohm terminator at each end.
8. Safety loop pins 3, 4, 5 and 7, command pins 1 to 5 and speed pins 1, 3 and 4 to the supervisor: 0.25 mm², as Table 3.

*Table 3. Connector pins.*

| Socket | Pin | Line |
| --- | --- | --- |
| Safety loop (M12, 8-pin A) | 1 | Loop supply, 12 V out to e-stop channel A |
| | 2 | Loop return, after e-stop channel A and the key, to the contactor coil |
| | 3 | E-stop channel B (to ground when the e-stop is not pressed) |
| | 4 | Brake switch A (to ground when the lever is released) |
| | 5 | Brake switch B (to ground when the lever is released) |
| | 6 | Brake coil output, 12 V, for a host's spring-applied brake; live only while the loop is closed (not used on the bench) |
| | 7 | Ground |
| | 8 | Not connected |
| Command (M12, 5-pin B) | 1 | +5 V for the throttle |
| | 2 | Throttle signal, 0.8 to 4.2 V |
| | 3 | Ground |
| | 4 | CAN high, external bus |
| | 5 | CAN low, external bus |
| Speed (M8, 4-pin A) | 1 | +5 V |
| | 3 | Ground |
| | 4 | Speed pulses |
| | 2 | Not connected |

**Check before moving on.** Every wire continues end to end and is labelled; with the fuse out, the power socket's two pins read open to each other; the coil loop reads closed through the coil only when pins 1 and 2 are bridged.

### 3.7 Lid and lid gasket

![Figure 11. Making sketch of the lid and gasket](../cad/drawings/MTC-DWG-104.png)

*Figure 11. Lid and gasket making sketch (MTC-DWG-104).*

**What they are and what they are made from.** The lid closes the top of the tube and is part of the heat sink. Aluminum sheet 3 mm, 5052 or 6061, cut to 220 x 140 mm. The gasket seals it: closed-cell EPDM sheet 1 mm thick.

**How to make them.**

1. Lid: cut 220 x 140 mm; deburr; round the corners to about 1 mm. Drill four 4.5 mm holes, 7.5 in from each end and each side.
2. Gasket: cut a frame 220 x 140 mm outside and 3 mm wide, with a 12 mm round pad at each corner over the port; punch a 4.5 mm hole through each pad, using the lid as the template.

**How it fits the parts next to it.**

![Figure 12. Joint 5: lid corner](05-build-plan/joint-05.png)

*Figure 12. Lid, gasket and corner screw, cut through the port.*

The gasket lies on the top of the walls and ports; the lid lies on the gasket; four M4 x 10 stainless button-head screws with bonded sealing washers go into the ports. Tighten them evenly in a cross pattern until the gasket is squeezed to about two-thirds of its thickness.

**Check before moving on.** The lid sits flat with no gap you can see round the edge; the gasket is not pinched out at any point.

### 3.8 Bench board

![Figure 13. Making sketch of the bench board](../cad/drawings/MTC-DWG-105.png)

*Figure 13. Bench board making sketch (MTC-DWG-105).*

**What it is and what it is made from.** The base of the bench rig, standing in for a host vehicle. Exterior-grade plywood 18 mm thick, cut to 960 x 480 mm. The motor end is the left end; the front edge is the side the brake levers face.

**How to make it.**

1. Cut 960 x 480 mm; sand the edges and corners.
2. Module bolt holes: four 6.5 mm holes on a 180 x 100 mm rectangle, centred 520 from the left end and 240 from the front edge.
3. Motor upright feet: four 6.6 mm holes at 122 and 158 from the left end, 141.5 and 338.5 from the front edge.
4. Bar post feet: two 6.6 mm holes 80 from the front edge, at 652 and 938 from the left end.
5. Counterbore every bolt hole from below, 13 mm across and 3 mm deep, so the bolt heads keep the board flat on the bench.
6. Mark the e-stop station's place, centred 820 from the left end and 390 from the front edge.

**How it fits the parts next to it.** It lies flat on a sturdy bench, clamped at both ends. Everything else bolts or screws to it.

**Check before moving on.** Hold the module with its pads on the board: the four rivet nuts sit over the four 6.5 mm holes.

### 3.9 Motor uprights (make 2)

![Figure 14. Making sketch of the motor upright](../cad/drawings/MTC-DWG-106.png)

*Figure 14. Motor upright making sketch (MTC-DWG-106).*

**What it is and what it is made from.** The pair of uprights that hold the hub motor by its axle with the wheel clear of the board. Aluminum flat bar 60 x 6 mm, 6082 or 6061.

**How to make it.**

1. Cut two 150 mm lengths; square and deburr.
2. Axle slot: 10.2 wide on the centre line, 36 deep from the top end, with a flat bottom. Saw both sides and file square. The axle's 10 mm flats slide in from above and its centre sits 120 above the board.
3. Foot bolt holes: two 6.6 mm holes 20 up from the bottom end, 18 each side of the centre line.
4. On one upright only (the one on the front-edge side, which carries the speed pickup), drill two 4.4 mm holes 120 up, 12 and 20 from the centre line toward the module.

**How it fits the parts next to it.**

![Figure 15. Joint 6: axle in its upright](05-build-plan/joint-06.png)

*Figure 15. The axle end in the slot, before the washer and nut go on.*

The uprights stand on the board with their inside faces 135 apart, the motor's axle width; check yours and set the gap to suit. A foot bolts to the outside face of each. The axle's flats drop into both slots so the axle cannot turn, and a washer and the axle nut on the outside clamp each upright.

**Check before moving on.** With the motor in place the axle drops into both slots by hand, cannot turn, and the shell is about 19 mm above the board.

### 3.10 Upright feet (make 4: two 60 mm, two 40 mm)

![Figure 16. Making sketch of the upright foot](../cad/drawings/MTC-DWG-107.png)

*Figure 16. Upright foot making sketch (MTC-DWG-107).*

**What it is and what it is made from.** Short angles that fix the motor uprights and the bar posts to the board. Aluminum equal angle 40 x 40 x 4 mm.

**How to make it.**

1. Cut two 60 mm lengths (motor uprights) and two 40 mm lengths (bar posts); square and deburr.
2. 60 mm feet: upright leg, two 6.6 mm holes 20 up from the board side, 18 each side of centre; flat leg, two 6.6 mm holes 25 from the outside corner, 18 each side of centre.
3. 40 mm feet: upright leg, two 6.6 mm holes 12 up, 10 each side of centre; flat leg, one 6.6 mm hole 25 from the outside corner, on the centre.
4. Drill each foot's upright leg clamped to its upright or post so the holes match.

**How it fits the parts next to it.** The upright leg lies flat on the outside face of its upright or post, held by M6 bolts with washers and nyloc nuts; the flat leg lies on the board, pointing away from the upright, held by M6 bolts from below.

**Check before moving on.** The upright or post stands square to the board when the bolts are tight.

### 3.11 Speed sensor ring

![Figure 17. Joint 7: speed sensor](05-build-plan/joint-07.png)

*Figure 17. Cut level with the axle and seen from above: side cover, ring, 3.5 mm gap, pickup, bracket, upright.*

**What it is.** An eight-magnet ring 80 mm across with six 5.5 mm holes on a 44 mm circle, which bolts to the reference motor's six-bolt disc mount, and a sealed Hall pickup with a lead and an M8 plug.

**How to fit it.** Six M5 screws with medium threadlocker into the disc mount, on the side of the motor that faces the front-edge upright.

**Check before moving on.** The ring runs true within 0.5 mm when the wheel is turned by hand.

### 3.12 Hall pickup bracket

![Figure 18. Making sketch of the Hall pickup bracket](../cad/drawings/MTC-DWG-108.png)

*Figure 18. Hall pickup bracket making sketch (MTC-DWG-108).*

**What it is and what it is made from.** A short strip that holds the speed sensor's pickup facing the magnet ring. Aluminum flat bar 20 x 3 mm.

**How to make it.**

1. Cut 42 mm; deburr.
2. Drill two 4.4 mm holes on the centre line, 4 and 12 from one end.
3. Hold the pickup on the other end with its centre 26 from the drilled end; mark its lug holes through it and drill to suit (usually two M3).

**How it fits the parts next to it.** The bracket lies flat on the inside face of the front-edge upright, level with the axle, reaching toward the module, on two M4 bolts through the upright. The pickup's face then sits 3.5 from the magnet ring, over the ring's magnet circle 34 from the axle centre (Figure 17).

**Check before moving on.** Turn the wheel by hand: the ring passes the pickup without touching, with a gap of 3 to 4 all round.

### 3.13 Bar posts (make 2)

![Figure 19. Making sketch of the bar post](../cad/drawings/MTC-DWG-109.png)

*Figure 19. Bar post making sketch (MTC-DWG-109).*

**What it is and what it is made from.** Two posts that hold the handlebar stub 70 above the board. Aluminum flat bar 40 x 6 mm, 6082 or 6061.

**How to make it.**

1. Cut two 90 mm lengths; square and deburr.
2. Bar hole: 22.5 mm on the centre line, its centre 70 up from the bottom end. Drill a pilot, open out with a step drill or hole saw, and file to a sliding fit on the handlebar.
3. Grub screw: drill 4.2 mm down the centre line from the top end into the bar hole and tap M5.
4. Foot bolt holes: two 6.6 mm holes 12 up, 10 each side of centre.

**How it fits the parts next to it.** A 40 mm foot bolts to the outside face of each post. The posts stand 230 apart (centres) along the front edge with the bar through both, and an M5 grub screw in each locks the bar.

**Check before moving on.** The bar slides through both posts by hand and locks with the grub screws.

### 3.14 Handlebar stub

![Figure 20. Making sketch of the handlebar stub](../cad/drawings/MTC-DWG-110.png)

*Figure 20. Handlebar stub making sketch (MTC-DWG-110).*

**What it is and what it is made from.** A short handlebar for the brake levers and the key and throttle pod, standing in for a host's controls. Aluminum tube 22.2 mm (7/8 in) outside, 2 mm wall, cut to 270 mm.

**How to make it.** Cut square; deburr inside and out; chamfer both outside edges 0.5 mm so the clamps slide on without scoring.

**How it fits the parts next to it.**

![Figure 21. Joint 8: handlebar, post, lever and pod](05-build-plan/joint-08.png)

*Figure 21. The bar slides through the post and is locked from the top; the lever and pod clamp the bar.*

It passes through both posts, 70 above the board, its ends 10 out from each post. From the left: brake lever, pod, brake lever, each clamped with its own screw.

**Check before moving on.** The clamps tighten without the bar turning in the posts.

### 3.15 Harness

**What it is.** Four made-up leads with keyed waterproof plugs, built to Figure 10 and Table 3: the motor lead (supplied with the motor, plugged straight in); the safety loop lead from its M12 plug to the e-stop station, with a branch from the station to both brake levers and the key; the command lead from its M12 plug to the throttle in the pod (and the external CAN pair, left capped on the bench); and the speed lead from the pickup to its M8 plug. Use shielded pairs for the signals, spiral wrap, and adhesive cable clips to hold every lead to the board.

**How to make it.** Cut each lead to length on the board with 100 mm spare. Crimp the M12 and M8 field plugs to the pins of Table 3. In the e-stop station, wire channel A in series with the key so the loop runs pin 1, channel A, key, pin 2; wire channel B and the brake switches between their pins and ground (pin 7).

**Check before moving on.** With a meter at the plugs: pins 1 and 2 of the safety loop read closed with the e-stop up and the key on, open when the e-stop is pressed or the key is off; pins 3, 4 and 5 each read to pin 7 and open when their switch acts; the throttle reads about 0.8 V and 4.2 V at its ends when fed 5 V.

### 3.16 Bought components

Buy to specification, not brand. Line numbers are those of the bill of materials.

- **Reference hub motor (line 1).** 250 W geared brushless hub motor, 36 or 48 V winding, Hall sensors and temperature sensor, 9-pin waterproof plug, freewheel, 10 mm axle flats, axle width about 135 mm, six-bolt disc mount.
- **Motor controller (line 2), contactor (line 4), precharge and fuse block (line 5).** As section 3.5.
- **Finned enclosure extrusion (line 6).** As section 3.2; 6061 plate for the floor; thermally conductive silicone sealant (about 1 W/m·K).
- **Sockets and vent (line 8).** As section 3.4.
- **E-stop station (line 9).** 22 mm red mushroom-head pushbutton on a yellow enclosure, twist release, two normally closed contact blocks with positive opening.
- **Brake levers (line 10).** Two e-bike levers for 22.2 mm bars with built-in normally closed cut-off switches.
- **Key and throttle pod (line 11).** Two-position key switch and hall-effect thumb throttle (0.8 to 4.2 V) in one pod for a 22.2 mm bar.
- **Speed sensor (line 12).** As section 3.14.
- **Fixings (line 14).** Four M6 closed-end rivet nuts; four 16 x 3 mm rubber pads; four 35 mm M3 hex standoffs; four M4 x 8 countersunk screws (floor); four M4 x 10 button-head screws with bonded sealing washers (lid); M3 and M4 stainless screws and nuts; 1 mm thermal pad; medium thread sealant; cable ties and labels.
- **Bench rig fixings (line 15).** Four M6 x 30 bolts with washers (module); M6 x 16 bolts with washers and nyloc nuts (feet); two M4 x 12 bolts with nuts (Hall bracket); two M5 grub screws; wood screws for the e-stop station.

## 4. Putting it together

In each picture the parts already fitted are grey and the part being fitted is in colour, with an arrow showing the way it goes in.

### Step 1: rivet nuts into the floor plate

![Step 1](05-build-plan/step-01.png)

From below, flange underneath; set each with the rivet nut tool.

### Step 2: sockets and vent into the finned tube

![Step 2](05-build-plan/step-02.png)

Each socket from outside on its sealing ring, screws or nut inside; the vent patch on the far end wall.

### Step 3: finned tube onto the floor plate

![Step 3](05-build-plan/step-03.png)

A thin film of conductive sealant where the walls and ports land; tube on, edges flush; four M4 countersunk screws from below, tightened evenly; wipe off the excess. Let the sealant cure for the time its maker states before step 7.

### Step 4: controller onto the floor

![Step 4](05-build-plan/step-04.png)

Thermal pad under it; four M3 screws with thread sealant.

### Step 5: contactor and precharge and fuse block

![Step 5](05-build-plan/step-05.png)

Two M4 screws each with thread sealant. Then the power wiring of section 3.6.1, items 1 to 3. **Hold point:** the fuse stays out of its holder.

### Step 6: standoffs and supervisor board

![Step 6](05-build-plan/step-06.png)

Standoffs on M3 screws into the floor; the board on four M3 screws. Then the rest of the wiring of section 3.6.1. **Hold point:** the wiring checks of section 3.6 pass.

### Step 7: gasket and lid

![Step 7](05-build-plan/step-07.png)

Gasket on the wall tops, lid on the gasket; four button-head screws with sealing washers, tightened evenly in a cross pattern. Leave the lid off until the first power checks of section 5 are done if you want to probe inside; fit it before the motor runs.

### Step 8: module onto the bench board

![Step 8](05-build-plan/step-08.png)

Pads over the four holes, module on the pads; four M6 x 30 bolts with washers up through the board into the rivet nuts, snug, not crushing the pads.

### Step 9: motor uprights onto the board

![Step 9](05-build-plan/step-09.png)

Each upright bolted to a 60 mm foot, then each foot bolted to the board from below; inside faces 135 apart, square to the board.

### Step 10: magnet ring onto the motor

![Step 10](05-build-plan/step-10.png)

Six M5 screws into the motor's six-bolt disc mount, medium threadlocker.

### Step 11: Hall bracket and pickup onto the upright

![Step 11](05-build-plan/step-11.png)

Bracket on the inside face of the front-edge upright, two M4 bolts with the nuts inside; pickup on the bracket. Fit it now: it is hard to reach with the motor in place.

### Step 12: motor into the uprights

![Step 12](05-build-plan/step-12.png)

Lower the motor so the axle flats drop into both slots, ring toward the pickup; washers and axle nuts outside, to the motor maker's torque. Check the 3.5 gap.

### Step 13: bar posts and handlebar stub

![Step 13](05-build-plan/step-13.png)

Posts on their 40 mm feet, bolted to the board from below; slide the bar through both, centred; grub screws snug.

### Step 14: brake levers and pod onto the bar

![Step 14](05-build-plan/step-14.png)

From the left: lever, pod, lever; each clamp screw to its maker's torque.

### Step 15: e-stop station onto the board

![Step 15](05-build-plan/step-15.png)

Four wood screws through the base inside the station, head toward the operator's side of the board.

### Step 16: harness

![Step 16](05-build-plan/step-16.png)

Plug each lead into its socket and clip it to the board, every lead at least 50 mm from the motor shell. **Hold point:** safety stop S1 of section 6.

## 5. First checks

These are the checks a TRL 4 test report would record; this plan only lists them. Requirement numbers are those of MTC-REQ-001.

*Table 4. First checks.*

| Check | Requirement | How | Pass when |
| --- | --- | --- | --- |
| Size and mass | R12 | Measure and weigh the module off the board | Within 250 x 170 x 70 mm; 2.0 kg or less (1.91 kg estimated) |
| Sealing of the build | R10 | Look at every socket ring, the lid gasket and the floor joint under a lamp | Every ring and the gasket evenly squeezed; sealant line unbroken (spray testing comes later) |
| Supply range and supervisor start | R1 | Bench supply, current limit 1 A, raised from 0 to 25 V, fuse in, motor unplugged | The supervisor starts above about 18 V; nothing gets warm |
| Precharge | R8 | Scope across the precharge resistor at power-up from 25 V | Current under 5 A; the contactor closes only after about 0.6 s and only with the bus at 90 % or more |
| No automatic restart | R4 | Power up with the key on, then with the throttle open | The contactor stays open until the key is cycled with the throttle at zero |
| E-stop | R3 | Scope on the contactor's main contacts; press the e-stop with the motor turning slowly | Power removed within 100 ms; the motor stays off until reset |
| Brake interlock | R5 | Pull each lever with the motor turning slowly | Drive torque removed within 200 ms of either lever |
| Independent speed limit | R6 | Set a low test limit; turn the wheel faster than it by throttle | The contactor opens after the overspeed has lasted 0.5 s |
| Fault reaction | R7 | Unplug the command plug, then the internal CAN, with the motor turning slowly | Torque removed within 200 ms of each |
| Case temperature | R9 | Thermocouples on a fin, the lid and the floor plate edge during a 30 minute run under load | Plotted against the calculation; the heavy case is not run on the bench |
| Fit to a host | R11 | Time taking the module off the board and refitting it with hand tools | Logged as a first estimate of the 2 hour target |

## 6. Safety stops

Stop at each point. Carry on only when everything listed is true.

- **S1. Before the first power-up.** Lid fitted or the inside covered; the main fuse out; every wire checked end to end; no battery in the room. The bench supply is a certified unit set to 25 V with a 1 A limit, and its output reads correct on a meter.
- **S2. Before the fuse goes in.** With the bench supply off, the power socket's pins read no short; the controller's bus reads open to the case; the coil loop opens when the e-stop is pressed.
- **S3. Before the motor is plugged in.** The precharge, no automatic restart and e-stop checks of section 5 pass on the bench supply with the motor unplugged (the contactor heard and seen to open).
- **S4. Before the motor first turns.** The motor's axle nuts are tight and the axle cannot turn in its slots; the wheel is clear of the board and of every lead; nobody stands in line with the wheel; a second person has a hand on the e-stop; the speed limit is set low; loose clothing, hair and jewellery are tied back or removed.
- **S5. Before a battery is connected (after the bench supply checks).** The pack has its own battery management system and fuse; its voltage is inside 20 to 60 V; the main fuse matches it (20 A for 36 and 48 V, 40 A for 24 V) and is rated 60 V DC or more with 1 kA breaking capacity; the pack is plugged in through the anti-spark socket with the key off; and the pack sits on a non-combustible surface with an extinguisher for electrical fires within reach.
- **S6. Every session.** Press the e-stop once before the first run and see the contactor open. Never bridge the safety loop with a jumper. After the pack is unplugged, wait one minute and check the controller's bus reads under 5 V before opening the lid.

## 7. Tools, skills and workspace

**Tools.** Bench drill or a drill in a stand; drills 2.5 to 10 mm; step drill to 22 mm; countersink; taps M3, M4 and M5 with tap wrench; M6 rivet nut tool; hacksaw with a 32 teeth per inch blade (or a bandsaw); jigsaw for the plywood; flat, half-round and needle files; deburring tool; scriber, square, steel rule and calipers; flat plate and abrasive paper; sealant gun; crimper for 4 mm² ring lugs and for M12 and M8 field plugs; wire strippers; soldering iron; multimeter; bench power supply 0 to 30 V with an adjustable current limit; two-channel oscilloscope (for the timing checks); thermocouple meter; torque screwdriver and torque wrench covering about 1 to 40 N·m; kitchen or hanging scale to 5 kg; stopwatch.

**Skills.** No certified trade is needed. Basic metalwork (marking out, sawing, drilling, tapping, setting rivet nuts), crimping and through-hole soldering, safe use of a bench power supply, and care with lithium batteries and with a turning wheel. All circuits are extra-low voltage, 60 V DC at most; no mains wiring is part of this build. The battery's short-circuit current is the main hazard: treat its leads as live at all times.

**Workspace.** A sturdy bench at least 1.2 x 0.6 m that the board can be clamped to; a metalwork corner kept apart from the electronics so chips stay off the boards; good light; a clear zone of 1 m round the wheel during runs; a non-combustible surface for any battery.

**Personal protective equipment.** Safety glasses for cutting, drilling, soldering and every powered run; cut-resistant gloves for handling bar and plate; hearing protection when sawing; no gloves near a turning drill or a turning wheel.

## 8. Where the numbers come from

- Model and constructability checks: `cad/src/model.py` (`python cad/src/model.py --check`); STEP and STL exports in `cad/step/` and `cad/stl/`.
- Pictures: `cad/src/build_plan_media.py`, using `.kit/build_views.py`; written to `docs/05-build-plan/` and `cad/drawings/MTC-DWG-101` to `MTC-DWG-110`.
- General arrangement: `cad/drawings/MTC-DWG-001.pdf`, Rev P3.
- Calculations: `docs/04-calcs/01-sizing.md` (MTC-CAL-001 v0.3) and `docs/04-calcs/sizing.py`: thermal and floor joint (section 4), mass (section 9), cost (section 10).
- Bill of materials: `bom/bom.csv` and `bom/bom-notes.md`.
- Decisions: `docs/decisions/0003-design-for-construction.md` (MTC-DDR-003), with MTC-DDR-001 and MTC-DDR-002; open items in `docs/06-design-decisions.md` (MTC-DEC-001).
- Requirements: `docs/03-requirements.md` (MTC-REQ-001 v0.5).
