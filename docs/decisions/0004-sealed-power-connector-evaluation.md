---
doc_id: MTC-DDR-004
title: MotionCore sealed power connector evaluation
project: MotionCore
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-02'
  author: Amish Chadha
  change: Paper evaluation of sealed power connectors against the rule decided on 2026-10-02 (MTC-DEC-001); no part chosen
---

# 0004: Sealed power connector evaluation

- **Date:** 2026-10-02
- **Status:** proposed (evaluation done; no part chosen)

## Context

The power socket in interface v0.2 is an XT90 anti-spark plug, which is not sealed (R10 asks for IP65 on the enclosure and mated connectors). On 2026-10-02 Amish approved a paper evaluation now, against one rule, with the XT90 kept for the bench prototype only (MTC-DEC-001; MTC-DDR-002 item 18). This record is that evaluation. It is a TRL 3 paper task: nothing was bought, built or tested, and the figures below are the classes of rating to look for, to be confirmed against a named part's datasheet.

The rule: the mated connector is keyed so it cannot be reversed, is IP67 when mated, carries at least 40 A continuous at 60 V DC (the larger fuse rating of MTC-CAL-001), and leaves no exposed live contact on the pack side.

## Options considered

| Option | Keyed | IP67 mated | 40 A at 60 V DC | No live contact exposed on the pack side | Verdict |
| --- | --- | --- | --- | --- | --- |
| XT90 anti-spark plug in a panel frame (now) | By its shape | No | Yes (90 A class) | Anti-spark pin protects the first contact only | Bench prototype only |
| Industrial IP67 single-pole power connector, one for positive and one for negative (for example Amphenol's SurLok Plus class) | Yes, by colour and key coding between the two poles | Yes, as listed for the class | Yes, the class lists 50 A or more per pole and 600 V or more | Yes, touch-safe sockets on the receptacle side | First candidate class |
| XT90 or similar inside a sealed plastic boot or bulkhead cover | By shape | Only as good as the boot seal, with a cable gland | Yes | No: contacts stay bare inside the boot | Rejected: no touch protection, seal depends on assembly |
| Round multi-pin power connector (M23 class, several pins in parallel) | Yes | Yes | Needs three or four pins in parallel per line | Yes | Fallback: larger, dearer, and the pins must share current evenly |
| M12 power connector (L-coded, 16 A) | Yes | Yes | No: 16 A | Yes | Rejected: current too low |

## Decision

Proposed for Amish's confirmation: carry the industrial IP67 single-pole connector class forward as the sealed power connector, two receptacles in the end wall (positive and negative, with different key coding so they cannot be swapped), and keep the XT90 for the bench prototype only. The M23 class is the fallback if no single-pole part meets the rule at a sensible price.

## Consequences

- No part is chosen at TRL 3: the rule has to be checked against a named part's datasheet (ratings, panel cut-out, torque, cable cross-section for the pack leads), which belongs to the parts purchase at TRL 4. The end wall hole, socket frame and BOM line 8 therefore stay as they are and are marked as the bench prototype's XT90.
- When a part is chosen, the end wall needs two round or square holes in place of the 12 x 22 mm XT90 slot, and BOM line 8 changes (the XT90 is replaced by two receptacles and two cable plugs, priced from the chosen part).
- R10 stays at risk until a part is chosen and its datasheet confirms the rule; vibration is still not analysed.
- Interface v0.2 lists the power connector as "sealed single-pole pair, part to be chosen; XT90 on the bench prototype".
