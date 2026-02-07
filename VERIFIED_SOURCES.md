# Verified Sources Registry (Do Not Edit Values Without Updating Citations)

This project enforces a strict rule: **no parameter enters the model unless it is backed by a verifiable primary source**.
All numeric constants used by the simulator MUST be defined in `models/verified_constants.py` with:
- value
- units
- source title
- publisher
- publication date
- URL

Primary sources used (2026-02-07 verification date):

1) MOXIE mission completion: total O2 and max hourly rate (NASA, 2023-09-06)
   - Total O2 produced: 122 grams
   - Max rate: 12 grams/hour (>=98% purity)
   https://www.nasa.gov/missions/mars-2020-perseverance/perseverance-rover/nasas-oxygen-generating-experiment-moxie-completes-mars-mission/

2) RAD dose equivalent rates: cruise vs surface (SwRI press release, 2013-12-09; aligns with Science-era reporting)
   - Cruise: 1.8 mSv/day (GCR dose equivalent rate inside spacecraft)
   - Surface: 0.67 mSv/day (average GCR dose equivalent rate Aug 2012–Jun 2013)
   https://www.swri.org/newsroom/press-releases/swri-scientists-publish-first-radiation-measurements-the-surface-of-mars

3) ISS ECLSS water recovery milestone (NASA, 2023-06-20)
   - Water recovery goal achieved: 98%
   https://www.nasa.gov/missions/station/iss-research/nasa-achieves-water-recovery-milestone-on-international-space-station/

4) NASA radiation permissible exposure limit framing: 3% REID at upper 95% confidence level (NASA TP, 2021)
   https://ntrs.nasa.gov/api/citations/20210009708/downloads/NASA-TP-20210009708.pdf

5) Crew metabolic consumables baseline (NASA NTRS, 2023)
   - O2 requirement: 0.84 kg per crew-member-day (kg/CM-d)
   - Water requirement table (life support): total 9.68 kg/CM-d (historic planning baseline, with caveats)
   https://ntrs.nasa.gov/api/citations/20230013555/downloads/Take%20or%20Make%20in%20space.pdf
