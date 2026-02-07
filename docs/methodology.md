# Methodology (Strict Baseline)

## Scientific rule (non-negotiable)
This repository enforces a hard rule:

**No numeric parameter is used unless it is backed by a verifiable primary source** (NASA/ESA technical reports, peer-reviewed journals, or NTRS).
All verified anchors live in models/verified_constants.py and are documented in VERIFIED_SOURCES.md.

## Scope of the v0.0.1 baseline model
This baseline answers a narrow, testable engineering question:

> Given a colony size N0, initial stored mass of O₂ and water, local closure fractions for oxygen and water, and discrete resupply windows, **when does the colony collapse due to O₂ or water depletion?**

Radiation is tracked only as **dose bookkeeping** using published cruise vs surface dose-equivalent rates.  
This model **does not** convert dose to clinical outcomes.

## State variables (units)
- M_O2(t) [kg] — stored oxygen mass at time step 	
- M_H2O(t) [kg] — stored water mass at time step 	
- D(t) [mSv] — cumulative dose (bookkeeping only)

## Core balance equations (conservation form)
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
- N(t) is population size (baseline assumes constant unless changed by scenario inputs)
- c_O2, c_H2O are per-capita metabolic consumption rates (must be verified in VERIFIED_SOURCES.md)
- P_* are local production terms (only permitted if backed by primary sources and explicitly enabled)
- R_* are resupply injections on discrete windows (user-defined with explicit masses and cadence)

## Collapse definition (objective)
A simulation is declared **collapsed** at the first time step where any critical store becomes negative:
- M_O2(t) < 0 OR M_H2O(t) < 0

This is a conservative engineering failure condition (no hidden buffers).

## What is out-of-scope until verified
- Food/calories/agricultural yields (needs verified yields + power + closure)
- Fertility / multi-generational physiology at 0.38g (no verified human dataset)
- Long-duration ISRU reliability curves (needs demonstrated multi-year datasets)
- Terraforming claims

See docs/NON_CLAIMS.md.