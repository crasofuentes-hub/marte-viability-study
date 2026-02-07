"""
models/verified_constants.py

This module contains ONLY constants that are directly backed by verifiable primary sources.
No assumptions. No estimates. No secondary "blog numbers".

If you need a value that is not verified, add it to `models/unverified_placeholders.py` and the
simulation must refuse to run until it becomes verified.
"""

from dataclasses import dataclass

@dataclass(frozen=True)
class VerifiedConstant:
    name: str
    value: float
    units: str
    source_title: str
    publisher: str
    date: str
    url: str

# (1) MOXIE (NASA, 2023-09-06)
MOXIE_TOTAL_O2_G = VerifiedConstant(
    name="MOXIE_TOTAL_O2_G",
    value=122.0,
    units="g",
    source_title="NASA’s Oxygen-Generating Experiment MOXIE Completes Mars Mission",
    publisher="NASA",
    date="2023-09-06",
    url="https://www.nasa.gov/missions/mars-2020-perseverance/perseverance-rover/nasas-oxygen-generating-experiment-moxie-completes-mars-mission/",
)

MOXIE_MAX_RATE_G_PER_H = VerifiedConstant(
    name="MOXIE_MAX_RATE_G_PER_H",
    value=12.0,
    units="g/h",
    source_title="NASA’s Oxygen-Generating Experiment MOXIE Completes Mars Mission",
    publisher="NASA",
    date="2023-09-06",
    url="https://www.nasa.gov/missions/mars-2020-perseverance/perseverance-rover/nasas-oxygen-generating-experiment-moxie-completes-mars-mission/",
)

# (2) RAD dose equivalent rates (SwRI, 2013-12-09)
RAD_SURFACE_DOSE_EQUIV_MSV_PER_DAY = VerifiedConstant(
    name="RAD_SURFACE_DOSE_EQUIV_MSV_PER_DAY",
    value=0.67,
    units="mSv/day",
    source_title="SwRI scientists publish first radiation measurements from the surface of Mars",
    publisher="Southwest Research Institute (SwRI)",
    date="2013-12-09",
    url="https://www.swri.org/newsroom/press-releases/swri-scientists-publish-first-radiation-measurements-the-surface-of-mars",
)

RAD_CRUISE_DOSE_EQUIV_MSV_PER_DAY = VerifiedConstant(
    name="RAD_CRUISE_DOSE_EQUIV_MSV_PER_DAY",
    value=1.8,
    units="mSv/day",
    source_title="SwRI scientists publish first radiation measurements from the surface of Mars",
    publisher="Southwest Research Institute (SwRI)",
    date="2013-12-09",
    url="https://www.swri.org/newsroom/press-releases/swri-scientists-publish-first-radiation-measurements-the-surface-of-mars",
)

# (3) ISS ECLSS water recovery milestone (NASA, 2023-06-20)
ISS_WATER_RECOVERY_FRACTION = VerifiedConstant(
    name="ISS_WATER_RECOVERY_FRACTION",
    value=0.98,
    units="fraction",
    source_title="NASA Achieves Water Recovery Milestone on International Space Station",
    publisher="NASA",
    date="2023-06-20",
    url="https://www.nasa.gov/missions/station/iss-research/nasa-achieves-water-recovery-milestone-on-international-space-station/",
)

# (4) NASA PEL framing: 3% REID at upper 95% CL (NASA TP, 2021)
NASA_REID_LIMIT_UPPER_95CL = VerifiedConstant(
    name="NASA_REID_LIMIT_UPPER_95CL",
    value=0.03,
    units="fraction",
    source_title="Medical Countermeasure Requirements for Meeting Permissible Radiation Exposure Limits in Space",
    publisher="NASA (NTRS Technical Publication)",
    date="2021",
    url="https://ntrs.nasa.gov/api/citations/20210009708/downloads/NASA-TP-20210009708.pdf",
)

# (5) Crew consumables (NASA NTRS, 2023)
O2_KG_PER_CREW_MEMBER_DAY = VerifiedConstant(
    name="O2_KG_PER_CREW_MEMBER_DAY",
    value=0.84,
    units="kg/(crew-member*day)",
    source_title="Take Material to Space or Make It There?",
    publisher="NASA (NTRS)",
    date="2023",
    url="https://ntrs.nasa.gov/api/citations/20230013555/downloads/Take%20or%20Make%20in%20space.pdf",
)

WATER_KG_PER_CREW_MEMBER_DAY_BASELINE = VerifiedConstant(
    name="WATER_KG_PER_CREW_MEMBER_DAY_BASELINE",
    value=9.68,
    units="kg/(crew-member*day)",
    source_title="Take Material to Space or Make It There?",
    publisher="NASA (NTRS)",
    date="2023",
    url="https://ntrs.nasa.gov/api/citations/20230013555/downloads/Take%20or%20Make%20in%20space.pdf",
)
