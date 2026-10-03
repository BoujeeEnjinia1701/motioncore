# BOM notes

- Costs are indicative USD prices for single prototype quantities, estimated in September 2026. Supplier types are given; specific suppliers are not yet selected.
- Item numbers 1 to 15 match the callouts in `media/exploded.png`. Item 15, the bench rig, belongs to the prototype only (MTC-DDR-003).
- **Budget scope (MTC-DDR-001 item 1, decided by Amish, 2026-09-25: go with recommendation):** the USD 300 `budget_usd` is a value-engineering target (a hypothetical control target, not a limit; Amish, 2026-10-01) for the MotionCore kit, items 2 to 14. The reference hub motor (item 1) is a named part of interface v0.1 but is costed to each host.

*Table 1. Totals (checked by `docs/04-calcs/sizing.py`, MTC-CAL-001 section 10).*

| Scope | Items | Total | Against the USD 300 value-engineering target |
| --- | --- | --- | --- |
| MotionCore kit | 2 to 14 | USD 297 | USD 3 under the target |
| Reference motor, costed to the host | 1 | USD 70 | Not in the MotionCore total |
| Bench rig, prototype only | 15 | USD 35 | Not in the MotionCore total |
| Complete kit with reference motor | 1 to 14 | USD 367 | For host cost estimates |

- Changes at TRL 3: the supervisor board rose from $22 to $30 (second CAN transceiver and an 18 to 75 V auxiliary buck); pads and consumables from $6 to $8 (rubber isolation pads with M6 studs). Specifications now carry the selection criteria from MTC-CAL-001: fuse rated 60 V DC or more with 1 kA breaking capacity (58 V before R1 was raised to 60 V, MTC-DDR-002), contactor breaking 50 A at 60 V DC and releasing within 50 ms with a 24 V Zener, 4 mm² pack leads for 24 V hosts. The controller overvoltage fault is set to 66 V (was 60 V) and the XT90 is provisional pending a sealed-connector evaluation (MTC-DDR-002). None of these changes alters a price.
- The battery pack, BMS and host mechanics (wheels, brakes, frame, pack receptacle and its SwapCell INTERLOCK coding resistor) are not included.
- Changes for construction (MTC-DDR-003, 2026-10-01): item 6 becomes a cut length of finned extrusion on a floor plate (USD 22 to 30); item 7 a flat lid on an EPDM gasket (unchanged price); item 8 sockets through the wall with flanges and frames, an M8 speed sensor socket and a membrane vent (USD 18 to 24); item 10 brake levers with built-in switches (USD 4 to 7 each); item 12 adds the speed sensor plug (USD 6 to 8); item 13 adds the safety loop branch (USD 18 to 20); item 14 adds rivet nuts and lid and floor fixings (USD 8 to 12); item 15 added. The kit rises from USD 265 to USD 293.
- Decided on 2026-10-02 (MTC-DEC-001) and carried into the BOM the same day: a contactor coil economizer is fitted (module in line 3, USD 4.00 extra, so line 3 is USD 34.00; the carrier board grows 20 mm to 85 x 108 mm to take it), wired so the safety loop breaks the coil supply upstream of it. Not in the BOM lines: the XT90 (line 8) is for the bench prototype only, pending the sealed power connector evaluation (keyed, IP67 mated, 40 A or more at 60 V DC; first candidate class an industrial IP67 single-pole connector such as Amphenol's SurLok Plus); the M8 speed socket is part of interface v0.2.
