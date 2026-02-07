# Mars Colony Viability (Strict Science-Only Baseline)

This repository starts from **zero assumptions** and enforces a hard rule:

> **No numeric parameter is used unless it is backed by a verifiable primary source.**

All verified constants are in `models/verified_constants.py` and documented in `VERIFIED_SOURCES.md`.

## Scope (v0.0.1)
This baseline model addresses a real, testable question without speculative inputs:

**Given a colony size N0, initial storage, local closure fractions for oxygen and water, and discrete resupply windows, when does the colony collapse due to O2 or water depletion?**

It also tracks **radiation dose bookkeeping** using published RAD rates (cruise vs surface). It does **not** convert dose to cancer probability (that requires clinical models and additional validated assumptions).

### What this repo explicitly does NOT do (yet)
- No food/calories model (requires verified agricultural yields and energy budgets).
- No fertility / multi-generational physiology in 0.38g (no verified human dataset).
- No ISRU reliability curves (requires long-duration demonstrated plant datasets).
- No Terraforming claims.

Those will be added only when backed by primary sources (NASA/ESA technical reports, peer-reviewed journals, or NTRS).

## Verified anchors used
- MOXIE total O2 produced and max hourly rate (NASA, 2023-09-06)
- RAD dose equivalent rates cruise vs surface (SwRI, 2013-12-09)
- ISS water recovery milestone 98% (NASA, 2023-06-20)
- NASA radiation framing: 3% REID at upper 95% CL (NASA TP, 2021)
- Metabolic consumables: O2 0.84 kg/crew-member-day and water 9.68 kg/CM-d baseline (NASA NTRS, 2023)

See `VERIFIED_SOURCES.md`.

## Install
```bash
python -m venv .venv
# Windows PowerShell:
. .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
