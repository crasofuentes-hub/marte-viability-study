from __future__ import annotations

import csv
import json
import os
import sys
from dataclasses import asdict, fields
from pathlib import Path

# --- Robust import: force repo root on sys.path (works for -m and direct run) ---
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from models.model import Scenario, simulate  # noqa: E402

def _ensure_results_dir() -> Path:
    out = REPO_ROOT / "results"
    out.mkdir(parents=True, exist_ok=True)
    return out

def _scenario_fields() -> set[str]:
    return {f.name for f in fields(Scenario)}

def _filter_kwargs(kwargs: dict) -> dict:
    allowed = _scenario_fields()
    unknown = sorted([k for k in kwargs.keys() if k not in allowed])
    if unknown:
        print("[run_scenarios] Dropping unknown Scenario kwargs:", unknown)
    return {k: v for k, v in kwargs.items() if k in allowed}

def _extract_result(result) -> dict:
    # simulate() en tu repo devuelve dict; aun así lo hacemos tolerante
    if isinstance(result, dict):
        collapsed = result.get("collapsed", result.get("Collapsed", None))
        collapse_day = result.get("collapse_day", result.get("day_of_collapse", None))
        o2_series = result.get("o2_series", result.get("o2_stock_days_series", None))
        water_series = result.get("water_series", result.get("water_stock_days_series", None))
        t_days = result.get("t_days", result.get("time_days", None))
        dose_msv = result.get("dose_msv", result.get("radiation_dose_msv", None))
    else:
        collapsed = getattr(result, "collapsed", getattr(result, "Collapsed", None))
        collapse_day = getattr(result, "collapse_day", getattr(result, "day_of_collapse", None))
        o2_series = getattr(result, "o2_series", None)
        water_series = getattr(result, "water_series", None)
        t_days = getattr(result, "t_days", None)
        dose_msv = getattr(result, "dose_msv", None)

    return {
        "collapsed": collapsed,
        "collapse_day": collapse_day,
        "t_days": t_days,
        "o2_series": o2_series,
        "water_series": water_series,
        "dose_msv": dose_msv,
    }

def _plot_series(path: Path, x, y, title: str, xlabel: str, ylabel: str) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt  # noqa: E402

    plt.figure()
    plt.plot(x, y)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True, alpha=0.25)
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()

def _write_summary_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        raise RuntimeError("No rows to write.")
    cols = ["scenario_id","N0","years","dt_days","o2_storage_days","water_storage_days",
            "o2_local_fraction","water_local_fraction","water_recovery_fraction",
            "launch_window_days","missed_window_probability",
            "import_restore_fraction_o2","import_restore_fraction_water","cruise_days",
            "collapsed","collapse_day","dose_msv"]
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in cols})

def _write_summary_md(path: Path, rows: list[dict]) -> None:
    cols = ["scenario_id","N0","o2_storage_days","water_storage_days","o2_local_fraction",
            "water_local_fraction","water_recovery_fraction","launch_window_days",
            "missed_window_probability","collapsed","collapse_day","dose_msv"]
    lines = []
    lines.append("| " + " | ".join(cols) + " |")
    lines.append("| " + " | ".join(["---"]*len(cols)) + " |")
    for r in rows:
        vals = []
        for c in cols:
            v = r.get(c, "")
            if isinstance(v, float):
                v = f"{v:.4g}"
            vals.append(str(v))
        lines.append("| " + " | ".join(vals) + " |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")

def main() -> int:
    out = _ensure_results_dir()

    # --- Escenarios 100% compatibles con Scenario(fields) ---
    # NOTA: aquí NO inventamos campos. Sólo usamos los que existen (filtrados).
    scenarios = [
        ("S1_baseline",
         dict(N0=12, years=10, dt_days=1,
              o2_storage_days=365, water_storage_days=365,
              o2_local_fraction=0.97, water_local_fraction=0.98,
              water_recovery_fraction=0.98,
              launch_window_days=780, missed_window_probability=0.2,
              import_restore_fraction_o2=1.0, import_restore_fraction_water=1.0,
              cruise_days=210)),
        ("S2_higher_closure_buffers",
         dict(N0=12, years=25, dt_days=1,
              o2_storage_days=730, water_storage_days=730,
              o2_local_fraction=0.995, water_local_fraction=0.995,
              water_recovery_fraction=0.98,
              launch_window_days=780, missed_window_probability=0.1,
              import_restore_fraction_o2=1.0, import_restore_fraction_water=1.0,
              cruise_days=210)),
        ("S3_scale_stress",
         dict(N0=50, years=10, dt_days=1,
              o2_storage_days=365, water_storage_days=365,
              o2_local_fraction=0.98, water_local_fraction=0.985,
              water_recovery_fraction=0.98,
              launch_window_days=780, missed_window_probability=0.2,
              import_restore_fraction_o2=1.0, import_restore_fraction_water=1.0,
              cruise_days=210)),
    ]

    rows = []
    for sid, kw in scenarios:
        kw = _filter_kwargs(kw)
        sc = Scenario(**kw)

        result = simulate(sc, seed=123)
        r = _extract_result(result)

        # Save JSON artifact
        art = {
            "scenario_id": sid,
            "scenario": asdict(sc),
            "result_summary": {
                "collapsed": r["collapsed"],
                "collapse_day": r["collapse_day"],
                "dose_msv": r["dose_msv"],
            },
        }
        (out / f"{sid}.json").write_text(json.dumps(art, indent=2), encoding="utf-8")

        # Plot if series exist
        if r["t_days"] is not None and r["o2_series"] is not None:
            _plot_series(out / f"{sid}_o2.png", r["t_days"], r["o2_series"],
                         f"{sid}: O2 stock (days of coverage)", "Day", "O2 stock (days)")
        if r["t_days"] is not None and r["water_series"] is not None:
            _plot_series(out / f"{sid}_water.png", r["t_days"], r["water_series"],
                         f"{sid}: Water stock (days of coverage)", "Day", "Water stock (days)")

        row = {"scenario_id": sid, **asdict(sc)}
        row["collapsed"] = r["collapsed"]
        row["collapse_day"] = r["collapse_day"]
        row["dose_msv"] = r["dose_msv"]
        rows.append(row)

    _write_summary_csv(out / "summary.csv", rows)
    _write_summary_md(out / "summary.md", rows)

    print("OK: wrote results/summary.csv and results/summary.md and per-scenario artifacts.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())