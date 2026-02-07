# Mars Colony Viability (Strict Science-Only Baseline)

This repository starts from **zero assumptions** and enforces a hard rule:

> **No numeric parameter is used unless it is backed by a verifiable primary source** (NASA/ESA technical reports, peer-reviewed journals, or NASA NTRS).

All verified numeric anchors are stored in `models/verified_constants.py` and documented in `VERIFIED_SOURCES.md`.

## What this repo answers (v0.0.x baseline)
A narrow, falsifiable engineering question:

**Given colony size `N0`, initial stores of O2 and water, local closure fractions, and discrete resupply windows: _when does the colony collapse due to O2 or water depletion?_**

Radiation is tracked only as **dose bookkeeping** using published cruise vs surface dose-equivalent rates.
This repo does **not** convert dose to clinical outcomes.

## Negative-result posture (important)
This project is designed to surface constraints. If a scenario collapses, that is a scientifically useful result (it reveals required closure/resupply conditions).

## What this repo explicitly does NOT do (yet)
- Food/calories model (requires verified agricultural yields and energy budgets).
- Fertility / multi-generational physiology at 0.38g (no verified human dataset).
- Long-duration ISRU reliability curves (requires demonstrated multi-year plant datasets).
- Terraforming claims.

See `docs/NON_CLAIMS.md`.

## Quickstart
### Install
`ash
python -m venv .venv
# Windows PowerShell:
. .\\.venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
`"
Add-Content -Path C:\Users\servi\marte-viability-study\README.content.txt -Encoding ascii -Value "
Add-Content -Path C:\Users\servi\marte-viability-study\README.content.txt -Encoding ascii -Value 
`ash
python main.py --help
`"
Add-Content -Path C:\Users\servi\marte-viability-study\README.content.txt -Encoding ascii -Value "
Add-Content -Path C:\Users\servi\marte-viability-study\README.content.txt -Encoding ascii -Value 
Because parent directories may contain unrelated pytest configs, always run:
`ash
python -m pytest -c pytest.ini
`"
Add-Content -Path C:\Users\servi\marte-viability-study\README.content.txt -Encoding ascii -Value "
Add-Content -Path C:\Users\servi\marte-viability-study\README.content.txt -Encoding ascii -Value 
- `docs/methodology.md` ? equations, units, collapse criterion (no speculative numbers)
- `docs/NON_CLAIMS.md` ? explicit scope limits and non-claims
- `paper/manuscript.md` ? manuscript scaffold (Markdown -> LaTeX/PDF later)

## Citation
See `CITATION.cff`.

- If/when a Zenodo DOI exists, it will be added to `CITATION.cff` and pinned in a new release.

