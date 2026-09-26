# BOM notes

- Costs are indicative USD prices for single prototype quantities, estimated in September 2026. Supplier types are given; specific suppliers are not yet selected.
- Item numbers 1 to 14 match the callouts in `media/exploded.png`.
- **Budget scope (MTC-DDR-001 item 1, decided by Amish, 2026-09-25: go with recommendation):** the $300 `budget_usd` covers the MotionCore kit, items 2 to 14. The reference hub motor (item 1) is a named part of interface v0.1 but is costed to each host.

*Table 1. Totals (checked by `docs/04-calcs/sizing.py`, MTC-CAL-001 section 10).*

| Scope | Items | Total | Against $300 |
| --- | --- | --- | --- |
| MotionCore kit | 2 to 14 | $265 | Within budget, $35 margin |
| Reference motor, costed to the host | 1 | $70 | Not in the MotionCore total |
| Complete kit with reference motor | 1 to 14 | $335 | For host budgets |

- Changes at TRL 3: the supervisor board rose from $22 to $30 (second CAN transceiver and an 18 to 75 V auxiliary buck); pads and consumables from $6 to $8 (rubber isolation pads with M6 studs). Specifications now carry the selection criteria from MTC-CAL-001: fuse rated 60 V DC or more with 1 kA breaking capacity (58 V before R1 was raised to 60 V, MTC-DDR-002), contactor breaking 50 A at 60 V DC and releasing within 50 ms with a 24 V Zener, 4 mm² pack leads for 24 V hosts. The controller overvoltage fault is set to 66 V (was 60 V) and the XT90 is provisional pending a sealed-connector evaluation (MTC-DDR-002). None of these changes alters a price.
- The battery pack, BMS and host mechanics (wheels, brakes, frame, pack receptacle and its SwapCell INTERLOCK coding resistor) are not included.
