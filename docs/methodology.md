# Methodology (Strict Baseline)

## Scientific rule (non-negotiable)
This repository enforces a hard rule:

**No numeric parameter is used unless it is backed by a verifiable primary source** (NASA/ESA technical reports, peer-reviewed journals, or NTRS).
All such anchors live in models/verified_constants.py and are documented in VERIFIED_SOURCES.md.

## Scope of v0.0.1 baseline model
This baseline answers a narrow, testable question:

> Given a colony size N0, initial stored mass of O₂ and water, local closure fractions for oxygen and water, and discrete resupply windows, **when does the colony collapse due to O₂ or water depletion?**

Radiation is tracked only as **dose bookkeeping** using published RAD rates (cruise vs surface). This model **does not** convert dose to health outcomes.

## State variables (units)
The model uses explicit mass bookkeeping:
- M_O2(t) [kg]  — stored oxygen mass at time step 	
- M_H2O(t) [kg] — stored water mass at time step 	
- D(t) [mSv]    — cumulative dose (bookkeeping only)

## Core deterministic balance equations
At each time step (e.g., per day), consumables are updated by conservation:

### Oxygen
\[
M_{O2}(t+\Delta t) = M_{O2}(t) - N(t)\,c_{O2}\,\Delta t + P_{O2}(t) + R_{O2}(t)
\]

### Water
\[
M_{H2O}(t+\Delta t) = M_{H2O}(t) - N(t)\,c_{H2O}\,\Delta t + P_{H2O}(t) + R_{H2O}(t)
\]

Where:
- N(t) is population size (baseline assumes constant unless explicitly changed by the scenario inputs)
- c_O2, c_H2O are per-capita metabolic consumption rates (must be verified in VERIFIED_SOURCES.md)
- P_* are local production terms (only permitted if backed by a primary source and explicitly enabled)
- R_* are resupply injections on discrete windows (user-specified with explicit masses and cadence)

## Collapse definition (objective, testable)
A simulation is declared **collapsed** at the first time step where any critical life-support store crosses below zero:

- M_O2(t) < 0  OR
- M_H2O(t) < 0

This is a conservative engineering failure condition (no hidden buffers).

## Uncertainty handling (strict)
This repo will add stochasticity **only** where probability distributions are supported by primary data.
Until then, parameters remain deterministic and transparent.

## What is explicitly out-of-scope (until verified)
- Food/calories/agriculture yields (needs verified yields + power + closure fractions)
- Fertility / multi-generational physiology in 0.38g (no verified human dataset)
- Long-duration ISRU reliability curves (needs demonstrated long-run plant datasets)
- Terraforming claims (not part of this repository)

See docs/NON_CLAIMS.md.