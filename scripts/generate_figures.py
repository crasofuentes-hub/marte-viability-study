from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Iterable, List, Tuple

import matplotlib
matplotlib.use("Agg", force=True)

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.ticker import NullLocator

RESULTS_DIR = Path("results")
MAX_PNG_PER_SCENARIO = 6   # profesional: no inundar el repo

def _is_num(x: Any) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(float(x))

def _looks_like_series(v: Any) -> bool:
    if not isinstance(v, list) or len(v) < 3:
        return False
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

def _safe_plot(out_png: Path, title: str, y: List[float]) -> None:
    out_png.parent.mkdir(parents=True, exist_ok=True)

    fig = Figure(figsize=(10, 4), dpi=140)
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)

    # Evita ticks/markers que en algunos entornos Py3.14+mpl disparan deepcopy recursivo
    ax.xaxis.set_major_locator(NullLocator())
    ax.yaxis.set_major_locator(NullLocator())
    ax.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)

    x = list(range(len(y)))
    ax.plot(x, y)

    fig.text(0.01, 0.98, title, ha="left", va="top")
    fig.text(0.01, 0.02, f"n={len(y)}  min={min(y):.6g}  max={max(y):.6g}", ha="left", va="bottom")

    fig.tight_layout(rect=[0, 0.06, 1, 0.92])
    canvas.draw()
    fig.savefig(out_png)

def generate() -> int:
    if not RESULTS_DIR.exists():
        raise SystemExit("Missing results/ directory. Run: python -m scripts.run_scenarios")

    json_files = sorted(RESULTS_DIR.glob("S*.json"))
    if not json_files:
        raise SystemExit("No scenario JSON files found (results/S*.json).")

    wrote = 0

    for jf in json_files:
        obj = json.loads(jf.read_text(encoding="utf-8"))

        candidates: List[Tuple[str, List[float]]] = []
        for k, v in _walk(obj):
            if _looks_like_series(v):
                candidates.append((k, [float(x) for x in v]))

        # Reporte determinista
        if not candidates:
            top_keys = sorted(list(obj.keys())) if isinstance(obj, dict) else []
            print(f"[generate_figures] {jf.name}: NO numeric series found. top-level keys={top_keys}")
            continue

        # Ordena por longitud desc, y luego por key asc (determinista)
        candidates.sort(key=lambda kv: (-len(kv[1]), kv[0]))

        base = jf.stem
        for i, (k, s) in enumerate(candidates[:MAX_PNG_PER_SCENARIO], start=1):
            out = RESULTS_DIR / f"{base}_series_{i:02d}.png"
            title = f"{base} :: series_{i:02d}  (source={k})"
            _safe_plot(out, title, s)
            print(f"[generate_figures] wrote: {out.as_posix()} (len={len(s)})")
            wrote += 1

    return wrote

if __name__ == "__main__":
    n = generate()
    if n == 0:
        raise SystemExit("No PNGs created. Your results JSON contain no numeric series arrays.")
    print(f"OK: created {n} PNGs")