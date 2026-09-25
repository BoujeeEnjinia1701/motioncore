# MotionCore

**Area:** Shared Components · **Status:** Concept · **Prototype budget:** about $300 USD · **Difficulty:** 4 of 5

A standard motor, controller and safety module (hub or mid-drive motor, open controller, e-stop, speed limit and brake interlock) that the lab's mobility and automation designs bolt on rather than re-engineer.

## Concept rationale

Standardizing the drive and safety chain lets the lab spend design effort on what is different about each vehicle, while every project inherits a reviewed safety function.

## Burning platform

Light electric vehicles and small automation are growing fastest where formal engineering support is thinnest, and unsafe DIY drive systems cause avoidable injuries.

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| _To be developed_ | |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| _To be developed_ | |

## What sparked the idea

It came out of a September 2026 review of Design Molecule's applied research areas against the open projects already in the lab. CargoMule, PalletPilot, StepClimber, SunSpoke and DustRunner each describe their own motor and safety logic.

## Problem

Each vehicle or machine concept re-specifies the same drive train and safety logic, and small teams rarely have time to get the emergency stop, speed limit and brake interlock right.

## Concept

A standard motor, controller and safety module (hub or mid-drive motor, open controller, e-stop, speed limit and brake interlock) that the lab's mobility and automation designs bolt on rather than re-engineer.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- 250 to 500 W brushless motor
- Open-source motor controller (VESC class)
- Hardwired emergency stop and contactor
- Brake interlock switches
- Throttle or command input board
- Heat sink enclosure
- Wiring harness with keyed connectors

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> Moving machinery and stored electrical energy: guard all rotating parts, test the emergency stop before every run and limit speed during development. Lithium cells can overheat, vent and burn. Use protected cells or LiFePO4, fuse every pack, charge only within the cell maker's limits and never leave a first build charging unattended.

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

A project of the [Design Molecule](https://designmolecule.com) lab. Shared components set.
