import json
import re
from pathlib import Path
import dataclasses

import matplotlib.pyplot as plt

from models.model import Scenario, simulate

REPO = Path(__file__).resolve().parents[1]
RESULTS = REPO / "results"

def _is_numeric_series(x):
    if not isinstance(x, (list, tuple)):
        return False
    if len(x) < 5:
        return False
    # allow ints/floats
    for v in x[:5]:
        if not isinstance(v, (int, float)):
            return False
    return True

def _pick_time_axis(res):
    # Prefer explicit time arrays if present
    for k in ["t_days", "t", "time_days", "days"]:
        if k in res and _is_numeric_series(res[k]):
            return k, res[k]
    # Otherwise infer from any series length
    for k, v in res.items():
        if _is_numeric_series(v):
            return "index_days", list(range(len(v)))
    return None, None

def _pick_series(res, kind):
    # kind in {"o2","water"}
    # Strong preference: keys that contain kind and look like series/stock
    cand = []
    for k, v in res.items():
        if not _is_numeric_series(v):
            continue
        lk = k.lower()
        score = 0
        if kind == "o2":
            if "o2" in lk or "oxygen" in lk:
                score += 5
        else:
            if "water" in lk or "h2o" in lk:
                score += 5
        if "series" in lk:
            score += 3
        if "stock" in lk or "store" in lk:
            score += 2
        if "days" in lk:
            score += 1
        if score > 0:
            cand.append((score, k, v))
    if cand:
        cand.sort(reverse=True, key=lambda t: t[0])
        return cand[0][1], cand[0][2]

    # Fallback: choose any numeric series with semantic hints
    for k, v in res.items():
        if not _is_numeric_series(v):
            continue
        lk = k.lower()
        if kind == "o2" and ("o2" in lk or "oxygen" in lk):
            return k, v
        if kind == "water" and ("water" in lk or "h2o" in lk):
            return k, v

    return None, None

def _scenario_from_json(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    # allow either {"scenario": {...}} or direct kwargs
    if isinstance(data, dict) and "scenario" in data and isinstance(data["scenario"], dict):
        kwargs = dict(data["scenario"])
    elif isinstance(data, dict):
        kwargs = dict(data)
    else:
        raise ValueError("Scenario JSON is not a dict.")

    allowed = {f.name for f in dataclasses.fields(Scenario)}
    unknown = sorted([k for k in kwargs.keys() if k not in allowed])
    if unknown:
        print(f"[generate_figures] Dropping unknown Scenario keys in {path.name}: {unknown}")
    kwargs = {k: v for k, v in kwargs.items() if k in allowed}

    return Scenario(**kwargs)

def main():
    RESULTS.mkdir(parents=True, exist_ok=True)

    scenario_files = sorted(RESULTS.glob("S*_*.json"))
    if not scenario_files:
        raise SystemExit("No scenario JSON files found under results/ (expected S*_*.json).")

    made = 0
    for f in scenario_files:
        sc = _scenario_from_json(f)
        res = simulate(sc)

        if not isinstance(res, dict):
            print(f"[generate_figures] simulate() did not return dict for {f.name}; skipping.")
            continue

        tk, t = _pick_time_axis(res)
        if t is None:
            print(f"[generate_figures] No numeric time axis inferred for {f.name}; skipping.")
            continue

        o2k, o2 = _pick_series(res, "o2")
        wk,  w  = _pick_series(res, "water")

        stem = f.stem  # e.g., S1_baseline
        if o2 is not None:
            out = RESULTS / f"{stem}_o2.png"
            plt.figure()
            plt.plot(t, o2)
            plt.xlabel("Days")
            plt.ylabel("O2 stock (model units)")
            plt.title(f"{stem} - O2 ({o2k})")
            plt.tight_layout()
            plt.savefig(out, dpi=200)
            plt.close()
            made += 1
            print(f"[generate_figures] Wrote {out.name}")

        if w is not None:
            out = RESULTS / f"{stem}_water.png"
            plt.figure()
            plt.plot(t, w)
            plt.xlabel("Days")
            plt.ylabel("Water stock (model units)")
            plt.title(f"{stem} - Water ({wk})")
            plt.tight_layout()
            plt.savefig(out, dpi=200)
            plt.close()
            made += 1
            print(f"[generate_figures] Wrote {out.name}")

        if o2 is None and w is None:
            print(f"[generate_figures] No O2/Water series detected in simulate() output for {f.name} (keys: {list(res.keys())}).")

    print(f"[generate_figures] Total figures written: {made}")

if __name__ == "__main__":
    main()