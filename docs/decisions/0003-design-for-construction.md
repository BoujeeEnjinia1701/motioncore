---
doc_id: MTC-DDR-003
title: MotionCore design for construction
project: MotionCore
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
---

# 0003: Design for construction

- **Date:** 2026-10-01
- **Status:** Draft. Made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review. The items in Table 3 are proposed, awaiting Amish.

## Context

On 2026-09-30 Amish asked for every repo's build plan to show how each component is made and how it fits the next, with pictures, and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The concept model of MTC-PRC-001 v0.4 showed what MotionCore does but had parts that could not be made, fixed or connected as drawn. Checking it with build123d found an overlap of 3,300 mm³ between the supervisor standoffs and the controller, a connector panel standing outside a closed wall with no holes through it, connectors closer together than their own flanges, and several parts with no fixing at all. The reference kit was laid loose on a bench with the motor standing on its shell, so it could not be run with the wheel off the ground as the safety section requires.

The changes below keep what MotionCore does: the same controller, supervisor, contactor, precharge and fuse, the same hardwired e-stop loop and twin speed check, the same host mounting interface (four M6 on 180 x 100 mm), the same four interface connectors and the same finned aluminum heat sink. Nothing here changes the pitch or the safety case. Every change is in `cad/src/model.py`, which now runs 111 constructability checks (`python cad/src/model.py --check`): parts that must touch do touch, and parts that must not touch are apart by at least the stated clearance. All 111 pass.

## Options considered

For the enclosure, three routes keep a finned aluminum heat sink: (a) a cut length of finned enclosure extrusion with a separate floor plate, (b) heat-sink slices bolted to a plain die-cast box, (c) a body machined from solid. Option (b) doubles the wall where the fins attach and adds about 0.19 kg, which breaks R12's 2.0 kg limit. Option (c) costs several times the USD 22 line and is not a garage process. Option (a) keeps one wall thickness and the vertical fins, and is chosen. For the other changes the simplest sound fix was taken; the alternatives are noted in Table 1.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The body was an "extruded" box with an integral floor and vertical fins. An extrusion cannot have a closed floor and fins that run across its length. | The walls and fins are a 56 mm length cut from a finned enclosure extrusion (220 x 140 mm outside the walls, 3 mm walls, eleven 3 x 14 mm fins per long side on a 19 mm pitch, four screw ports in the inside corners), standing on a separate 3 mm 6061 floor plate. The joint is a film of thermally conductive silicone sealant on the wall and port end faces, pulled together by four M4 countersunk screws from below into the ports. | One wall thickness, fins still vertical for natural convection, and the controller still sits on aluminum that is bolted to the fins. Fins drop from 4 to 3 mm (typical for extrusions) and now run the full tube height, so the fin area rises from 0.0338 to 0.0382 m². |
| P2 | The lid had a 3 mm lip inside the walls, which clashes with the corner screw ports; the lid had no fixing. | Flat 3 mm lid on a 1 mm closed-cell EPDM gasket frame, four M4 button-head screws with bonded sealing washers into the same corner ports. | The ports take both the floor and lid screws; button heads keep the module under 70 mm tall. |
| P3 | Four M6 inserts were drawn in cast bosses, which a 3 mm plate floor cannot carry. | Four M6 closed-end rivet nuts set in the floor plate from below, flanges outside; the rubber isolation pads (16 x 3 mm) sit under the flanges. | The host interface is unchanged (four M6 on 180 x 100 mm) and the closed end keeps the floor sealed. |
| P4 | The supervisor's standoffs stood inside the controller's footprint: 3,300 mm³ of overlap. | Supervisor carrier board 85 x 88 mm (was 85 x 60), on four 35 mm M3 standoffs placed outside the controller, 4.2 mm clear of it; 10 mm of air between the controller and the board. | The board stays over the controller where the concept put it; a wider board is free because it is a made part. |
| P5 | The connector panel was a plate on the outside of a closed end wall, with no holes or socket bodies inside; the four connectors were 24 mm apart, less than their flanges and nuts. | The sockets go straight through the 3 mm end wall, so the separate panel plate is dropped. XT90 stood on end in a two-screw panel frame; motor socket nut-mounted; both M12 sockets on 20 mm four-screw square flanges. Centres 28, 56, 83 and 109 mm from the socket-side face, 28.5 mm above the tube's bottom edge. | Every flange and nut has at least 4 mm to its neighbour, the rear bodies clear everything inside by 3 mm or more, and the XT90 can be swapped for a sealed connector by recutting one hole. |
| P6 | The precharge and fuse block sat 8 mm from the panel, in the path of the socket bodies. | Moved beside the contactor on the plain side (+Y), 52 x 30 mm footprint. | Leaves 20 mm behind the end wall for socket bodies and wiring. |
| P7 | The controller, contactor and fuse block had no fixings. | M3 (controller, standoffs) and M4 (contactor foot, fuse block) screws into holes tapped through the floor plate, with thread sealant; contactor on a 3 mm mounting foot. | The plate is too thin for blind holes; sealant keeps the floor sealed. |
| P8 | The independent speed sensor had no connector: the 8-pin safety loop and 5-pin command sockets have no free pins for its 5 V, ground and signal. | An M8 4-pin A-coded socket in the socket-side wall, between the first two fins from the far end, 18 mm above the tube's bottom edge. It stays inside the fin depth, so the envelope does not grow. | R11 already lists "sensors" in the connector set; the socket is the simplest way to bring the sensor in. See A1. |
| P9 | The vent plug in the BOM was not modelled; an M12 vent on an end wall would push the length past R12's 250 mm. | Adhesive membrane vent, 20 mm, over a 5 mm hole in the far end wall, 43 mm above the bottom edge. | 1.5 mm proud; the envelope stays at 240 mm long. |
| P10 | The magnet ring floated 1.5 mm off the motor and the Hall pickup floated in the air. | Ring bolted to the motor's six-bolt disc mount (44 mm circle, M5); pickup on a 20 x 3 mm bracket on the inside face of the socket-side motor upright, 3.5 mm from the ring over the 34 mm magnet circle. | Uses the mounting the reference hub already has. |
| P11 | The reference kit lay loose on a bench with the motor standing on its shell, so the drive could not run with the wheel off the ground. | A bench rig (new BOM line 15, not part of the MotionCore kit): 18 mm plywood board 960 x 480 mm; two 60 x 6 mm uprights with 10.2 mm slots that take the axle flats (axle 120 mm up, shell 19 mm clear of the board) on 40 x 40 x 4 mm angle feet; two bar posts carrying a 22.2 mm handlebar stub; the e-stop station screwed to the board; the module bolted through its own interface. | Lets the first build be run as the safety section asks, and exercises the host mounting interface. |
| P12 | The brake switches were blocks with no mounting. | E-bike brake levers with built-in normally closed cut-off switches, clamped on the handlebar stub with the key and throttle pod between them (BOM line 10, USD 7 each). | Real parts that clamp where a host's controls go. |
| P13 | The harness routed the power socket's lead to the motor and the motor socket's lead to the brake switches. | One lead per socket: motor socket to the motor, safety loop to the e-stop station with a branch to both brake levers and the key, command to the pod, M8 to the speed pickup. | Matches the interface. |
| P14 | No pin assignment existed for the safety loop, command and speed sockets. | A pin-out that fits each socket (build plan Table 3): safety loop 1 loop supply, 2 loop return, 3 e-stop B, 4 brake A, 5 brake B, 6 brake coil output, 7 ground, 8 spare; command 1 +5 V, 2 throttle, 3 ground, 4 CAN high, 5 CAN low; speed 1 +5 V, 3 ground, 4 signal. | The harness can be made; see A1. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Size | Module 240 x 168 x 69 mm (was 243 x 168 x 66 mm): no panel plate, a 1 mm lid gasket, lid screw heads and a 1 mm rivet nut flange; tube height 56 mm so the total stays under 70 mm. Inside R12's 250 x 170 x 70 mm. | P1 to P5 |
| Mass | Module about 1.91 kg (was 1.94 kg): enclosure metal 1.00 kg, parts 0.91 kg; 0.09 kg under R12's 2.0 kg (MTC-CAL-001 v0.3 section 9). | Thinner fins and no panel plate offset the rivet nuts, gasket, screws and the wider supervisor board. |
| Thermal | Walls and fins: 50.2 °C reference, 58.4 °C heavy (58.5 °C before). The floor joint adds about 0.8 K (reference) and 1.6 K (heavy) between the floor plate and the walls, so the floor plate reaches about 51.0 °C and 60.0 °C, and the MOSFETs about 2 K more. R9 stays at risk. | P1 |
| Cost | Value-engineering target USD 300. Estimated cost of the constructable MotionCore kit (items 2 to 14) USD 293, USD 7 under the target (was USD 265): lines 6, 8, 10, 12, 13 and 14 repriced. Reference motor USD 70 to each host; bench rig USD 35, prototype only. | P1, P3, P5, P8, P9, P12, P13 |
| Drawings | MTC-DWG-001 Rev P3; making sketches MTC-DWG-101 to 110; concept sheet MTC-DWG-010 Rev P4. | Follows the model. |
| Documents | MTC-CAL-001 v0.3, MTC-REQ-001 v0.5, MTC-PRC-001 v0.5, `bom/bom.csv` and `bom/bom-notes.md`. No requirement changed status. | Follows the model. |

*Table 3. Proposed, awaiting Amish.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | Interface v0.1 was decided as four connectors (MTC-DDR-001 item 6). The speed sensor needs a fifth, and the pin-out was never set. | (a) M8 4-pin speed socket and the Table 1 P14 pin-out, as modelled, as interface v0.2; (b) a 12-pin M12 safety loop socket that also carries the speed sensor, keeping four connectors. | (a): cheaper sockets, the speed sensor lead stays short, and the 8-pin loop keeps a spare pin. |
| A2 | The bench rig (P11) adds a board, motor stand and handlebar stub to the prototype. | (a) build it with the first prototype, outside the kit total; (b) mount the first prototype straight on CargoMule. | (a): it lets the safety functions be checked with the wheel off the ground before any host is involved. |
| A3 | The floor joint adds 1.6 K in the heavy case, so the floor plate reaches the 60 °C limit of R9. | (a) accept, with R9 still at risk; (b) fit the contactor coil economizer already listed as open item 19 of MTC-DDR-002 (walls about 55.6 °C, floor about 57 °C); (c) bond the floor with thermally conductive epoxy (not removable). | (b), decided together with open item 19. |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan MTC-BLD-001 shows every component and step in pictures drawn from the model (`cad/src/build_plan_media.py`), and the open items are in the design decisions register MTC-DEC-001.
- Requirement status is unchanged: none not met; R2, R9 and R10 at risk; R11 not verifiable at TRL 3; the rest met on paper or by design review (MTC-CAL-001 v0.3).
- The photoreal renders (`media/render-*.png`), `media/card.png`, `media/social-preview.png` and the appearance model `cad/src/product_model.py` still show the concept: a connector panel plate, a lid with a lip, 4 mm fins and the kit loose on a bench. They need updating on Amish's Mac, where Blender is.
- The extrusion profile, the controller's mounting holes and the reference motor's axle width and disc mount are confirmed when parts are bought; the floor plate, tube and upright holes move to suit.
