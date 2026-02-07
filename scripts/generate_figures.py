from __future__ import annotations

import json
import math
import os
from pathlib import Path
from typing import Any, Iterable, List, Optional, Tuple

# Headless backend (no GUI)
import matplotlib
matplotlib.use("Agg", force=True)

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.ticker import NullLocator

RESULTS_DIR = Path("results")

def _is_num(x: Any) -> bool:
    if isinstance(x, (int, float)) and not isinstance(x, bool):
        return math.isfinite(float(x))
    return False

def _looks_like_series(v: Any) -> bool:
    if not isinstance(v, list):
        return False
    if len(v) < 3:
        return False
    # must be mostly numeric
    nums = sum(1 for x in v if _is_num(x))
    return nums >= int(0.9 * len(v))

def _walk(obj: Any, prefix: str = "") -> Iterable[Tuple[str, Any]]:
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f"{prefix}.{k}" if prefix else str(k)
            yield (p, v)
            yield from _walk(v, p)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            p = f"{prefix}[{i}]"
            yield (p, v)
            yield from _walk(v, p)

def _pick_series(candidates: List[Tuple[str, List[float]]], prefer_terms: List[str]) -> Optional[Tuple[str, List[float]]]:
    # deterministic: stable sort by (priority, -len, key)
    scored = []
    for k, s in candidates:
        k_low = k.lower()
        pr = min([prefer_terms.index(t) for t in prefer_terms if t in k_low], default=10_000)
        scored.append((pr, -len(s), k, s))
    scored.sort(key=lambda x: (x[0], x[1], x[2]))
    if not scored:
        return None
    _, _, k, s = scored[0]
    return (k, s)

def _safe_plot_series(out_png: Path, title: str, y: List[float]) -> None:
    out_png.parent.mkdir(parents=True, exist_ok=True)

    fig = Figure(figsize=(10, 4), dpi=140)
    canvas = FigureCanvas(fig)

    ax = fig.add_subplot(111)

    # CRÍTICO: eliminar ticks/locators para esquivar el bug de deepcopy en Py3.14 + mpl (ticks crean MarkerStyle)
    ax.xaxis.set_major_locator(NullLocator())
    ax.yaxis.set_major_locator(NullLocator())
    ax.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)

    # Plot
    x = list(range(len(y)))
    ax.plot(x, y)

    # Etiquetas "manuales" (sin ticks)
    fig.text(0.01, 0.98, title, ha="left", va="top")
    fig.text(0.01, 0.02, f"n={len(y)}  min={min(y):.3g}  max={max(y):.3g}", ha="left", va="bottom")

    fig.tight_layout(rect=[0, 0.05, 1, 0.92])
    canvas.draw()
    fig.savefig(out_png)

def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def generate() -> int:
    if not RESULTS_DIR.exists():
        raise SystemExit("Missing results/ directory. Run: python -m scripts.run_scenarios")

    json_files = sorted(RESULTS_DIR.glob("S*.json"))
    if not json_files:
        raise SystemExit("No scenario JSON files found (results/S*.json).")

    wrote = 0

    for jf in json_files:
        obj = _load_json(jf)

        series_candidates: List[Tuple[str, List[float]]] = []
        for k, v in _walk(obj):
            if _looks_like_series(v):
                series_candidates.append((k, [float(x) for x in v]))

        # Si NO hay series numéricas, reporta claves reales para debugging (determinista)
        if not series_candidates:
            keys = []
            if isinstance(obj, dict):
                keys = sorted(list(obj.keys()))
            print(f"[generate_figures] {jf.name}: NO numeric series found. top-level keys={keys}")
            continue

        # Selección determinista por prioridad textual
        o2_pick = _pick_series(series_candidates, prefer_terms=["o2", "oxygen"])
        w_pick  = _pick_series(series_candidates, prefer_terms=["water", "h2o"])

        # Si no hay match semántico, NO adivinamos: reportamos candidatos y seguimos
        if o2_pick is None or w_pick is None:
            print(f"[generate_figures] {jf.name}: cannot select o2/water deterministically.")
            print("  candidates:")
            for k, s in sorted(series_candidates, key=lambda x: x[0])[:50]:
                print(f"   - {k} (len={len(s)})")
            continue

        base = jf.stem
        o2_key, o2_series = o2_pick
        w_key,  w_series  = w_pick

        out_o2 = RESULTS_DIR / f"{base}_o2.png"
        out_w  = RESULTS_DIR / f"{base}_water.png"

        _safe_plot_series(out_o2, f"{base} :: O2  (source={o2_key})", o2_series)
        _safe_plot_series(out_w,  f"{base} :: Water (source={w_key})",  w_series)

        print(f"[generate_figures] wrote: {out_o2.as_posix()}  {out_w.as_posix()}")
        wrote += 2

    return wrote

if __name__ == "__main__":
    n = generate()
    if n == 0:
        raise SystemExit("No PNGs created. Either no numeric series exist in results/S*.json or selection could not be deterministic.")
    print(f"OK: created {n} PNGs")