# CONSERVATION-LAW BOOKKEEPING (strict baseline)
# Conceptual updates (no hidden buffers):
#   M_O2(t+dt)  = M_O2(t)  - N*c_O2*dt  + production_O2(t)  + resupply_O2(t)
#   M_H2O(t+dt) = M_H2O(t) - N*c_H2O*dt + production_H2O(t) + resupply_H2O(t)
# Collapse occurs when any critical store becomes negative.

"""
models/model.py

Strict-by-construction simulator:
- Uses ONLY verified constants from NASA/NTRS and other primary sources.
- Refuses to run if any required parameter is missing or unverified.
- Models 2 critical resources (O2, Water) + radiation dose bookkeeping + launch windows.

This is a *foundational* model. It is intentionally limited to avoid speculative assumptions.
"""

from dataclasses import dataclass
import math
import numpy as np

from .verified_constants import (
    O2_KG_PER_CREW_MEMBER_DAY,
    WATER_KG_PER_CREW_MEMBER_DAY_BASELINE,
    ISS_WATER_RECOVERY_FRACTION,
    RAD_SURFACE_DOSE_EQUIV_MSV_PER_DAY,
    RAD_CRUISE_DOSE_EQUIV_MSV_PER_DAY,
)

@dataclass(frozen=True)
class Scenario:
    # Colony size (user-specified; not a "science constant")
    N0: int

    # Duration and step
    years: int
    dt_days: float

    # Storage (days of demand available at t=0); user must declare (engineering design choice)
    # The model treats these as *design parameters*, not physical constants.
    o2_storage_days: float
    water_storage_days: float

    # Local closure fractions (0..1): fraction of daily demand met by local systems (ISRU + recycling).
    # These are *system performance parameters* and must be provided by the user
    # based on tested hardware or a cited design reference.
    o2_local_fraction: float
    water_local_fraction: float

    # Water recovery fraction: we allow using ISS milestone as a *demonstrated upper bound*.
    # You can set <= 0.98 unless you provide a new verified source.
    water_recovery_fraction: float

    # Launch window logistics: discrete imports every ~26 months (780 days)
    launch_window_days: int
    missed_window_probability: float

    # Imports: fraction of current storage restored per successful window (design choice)
    import_restore_fraction_o2: float
    import_restore_fraction_water: float

    # Radiation bookkeeping (not clinical risk): assume cruise for given days once at start.
    cruise_days: int

def _validate_scenario(sc: Scenario):
    if sc.N0 < 1:
        raise ValueError("N0 must be >= 1")

    if sc.dt_days <= 0:
        raise ValueError("dt_days must be > 0")

    for name, v in [
        ("o2_local_fraction", sc.o2_local_fraction),
        ("water_local_fraction", sc.water_local_fraction),
        ("water_recovery_fraction", sc.water_recovery_fraction),
        ("missed_window_probability", sc.missed_window_probability),
        ("import_restore_fraction_o2", sc.import_restore_fraction_o2),
        ("import_restore_fraction_water", sc.import_restore_fraction_water),
    ]:
        if not (0.0 <= v <= 1.0):
            raise ValueError(f"{name} must be in [0,1]")

    # Enforce demonstrated upper bound unless user changes code with new verified source
    if sc.water_recovery_fraction > ISS_WATER_RECOVERY_FRACTION.value + 1e-12:
        raise ValueError(
            f"water_recovery_fraction exceeds ISS demonstrated milestone ({ISS_WATER_RECOVERY_FRACTION.value}). "
            "Provide a new verified source and update verified_constants.py."
        )

def simulate(sc: Scenario, seed: int = 123):
    """
    Returns:
      dict with time series of resource stocks (in 'days of coverage') and population state (constant here),
      plus collapse time if resources hit zero.
    """
    _validate_scenario(sc)

    rng = np.random.default_rng(seed)

    steps = int(sc.years * 365.0 / sc.dt_days)
    t_days = np.arange(steps) * sc.dt_days

    # Convert daily demand (kg/day) for colony size
    o2_demand_kg_per_day = sc.N0 * O2_KG_PER_CREW_MEMBER_DAY.value
    water_demand_kg_per_day = sc.N0 * WATER_KG_PER_CREW_MEMBER_DAY_BASELINE.value

    # Represent storage as "days of demand coverage"
    o2_stock_days = float(sc.o2_storage_days)
    water_stock_days = float(sc.water_storage_days)

    o2_series = np.zeros(steps)
    water_series = np.zeros(steps)

    collapsed = False
    collapse_day = None

    # Radiation dose bookkeeping
    dose_msv = 0.0

    for i in range(steps):
        day = t_days[i]

        # Cruise dose applied at the beginning for sc.cruise_days
        if day < sc.cruise_days:
            dose_msv += RAD_CRUISE_DOSE_EQUIV_MSV_PER_DAY.value * (sc.dt_days / 1.0)
        else:
            dose_msv += RAD_SURFACE_DOSE_EQUIV_MSV_PER_DAY.value * (sc.dt_days / 1.0)

        # Effective local water closure: local_fraction + recovery contribution.
        # We treat water_recovery_fraction as a multiplier on the "non-local" portion, conservative:
        # unmet portion = (1 - local_fraction); recovered portion reduces imports needed, not producing water from nothing.
        # Here we approximate: net draw from storage per day = (1 - local_fraction) * (1 - recovery_fraction).
        water_net_draw_fraction = (1.0 - sc.water_local_fraction) * (1.0 - sc.water_recovery_fraction)

        # Oxygen: no general "98% recovery" claim is used here (not verified in our allowed constants set).
        # Net draw fraction = (1 - o2_local_fraction)
        o2_net_draw_fraction = (1.0 - sc.o2_local_fraction)

        # Update stocks in "days"
        o2_stock_days -= o2_net_draw_fraction * (sc.dt_days / 1.0)
        water_stock_days -= water_net_draw_fraction * (sc.dt_days / 1.0)

        # Launch window imports
        if sc.launch_window_days > 0 and i > 0 and (int(day) % sc.launch_window_days == 0):
            if rng.random() >= sc.missed_window_probability:
                o2_stock_days *= (1.0 + sc.import_restore_fraction_o2)
                water_stock_days *= (1.0 + sc.import_restore_fraction_water)

        o2_series[i] = max(0.0, o2_stock_days)
        water_series[i] = max(0.0, water_stock_days)

        if (o2_stock_days <= 0.0) or (water_stock_days <= 0.0):
            collapsed = True
            collapse_day = float(day)
            # clamp remaining
            o2_series[i:] = max(0.0, o2_stock_days)
            water_series[i:] = max(0.0, water_stock_days)
            break

    return {
        "t_days": t_days,
        "o2_stock_days": o2_series,
        "water_stock_days": water_series,
        "collapsed": collapsed,
        "collapse_day": collapse_day,
        "dose_msv_total": dose_msv,
        "o2_demand_kg_per_day": o2_demand_kg_per_day,
        "water_demand_kg_per_day": water_demand_kg_per_day,
    }
