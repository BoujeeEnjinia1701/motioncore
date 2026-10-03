---
doc_id: MTC-DDR-005
title: MotionCore license boundary review
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
  change: Short written review of the license boundary between the VESC firmware (GPL-3.0) and the supervisor firmware (MIT), as decided on 2026-10-02
---

# 0005: License boundary review

- **Date:** 2026-10-02
- **Status:** proposed (a short review for Amish; not legal advice)

## Context

On 2026-10-02 Amish decided that a short written review of the license boundary is done before any firmware is published, and that a lawyer is called in only if a commercial partner will ship the module (R13; MTC-DEC-001). No firmware is published and none exists beyond a labeled sketch.

The parts involved: the hardware (CERN-OHL-S-2.0); the supervisor firmware, MIT, running alone on its own STM32G0B1-class processor; and the motor controller's unmodified VESC firmware, GPL-3.0, running on a separate VESC-class controller. The two processors exchange messages over an internal CAN bus at 500 kbit/s.

## Review

1. **Separate programs.** The supervisor and the controller are separate programs on separate processors that share no code and no memory, and they talk only through CAN messages in the controller's documented command and status formats. Under the usual reading of the GPL (see the Free Software Foundation's FAQ on communication between programs), programs that exchange ordinary messages at arm's length are separate works, so the GPL-3.0 of the controller firmware does not reach the MIT supervisor firmware.
2. **What would break this.** Copying any VESC source, headers or generated tables into the supervisor firmware; linking a VESC library into it; or passing complex internal data structures that make the two intimately dependent. The supervisor code must be written against the public message formats only, and the repo should say so in its firmware readme.
3. **Shipping the controller firmware.** The controller stays unmodified GPL-3.0. Anyone who ships a module with that firmware loaded must give recipients the license text and an offer of the corresponding source (GPL-3.0 section 6); the repo only needs to point to the upstream project and version. If the module is sold as a consumer product, the "installation information" rule (section 6) means the controller must remain re-flashable by the owner, which a standard VESC-class controller is.
4. **Controller hardware.** The module buys a controller; it does not redistribute a hardware design. If a future version builds its own controller board from open VESC hardware files, those files carry their own license, which must be read then.
5. **Names.** "VESC" is a name of its maker; the repo says "VESC-class" and does not use the name as a product name.
6. **Hardware and documents.** The CERN-OHL-S-2.0 hardware and the documents sit beside the MIT firmware with no conflict, since each file carries its own license in `REUSE.toml`.

## Decision

Proposed: no change to the licenses in use. Before any firmware is published, add a firmware readme that states the boundary (separate processor, CAN messages only, no VESC code), the upstream VESC source and version in use, and the offer of corresponding source for the controller firmware. A lawyer is called in only if a commercial partner will ship the module.

## Consequences

- R13 stays met by design review; the review is now written.
- Nothing is published or built; the firmware readme is TRL 4 work.
