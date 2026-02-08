import json, math, os, re
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def find_series(obj, hints):
    found = {}
    stack = [("", obj)]
    while stack:
        path, node = stack.pop()
        if node is None:
            continue
        if isinstance(node, dict):
            for k, v in node.items():
                npath = f"{path}.{k}" if path else k
                stack.append((npath, v))
            continue
        if isinstance(node, list) and len(node) > 1 and all(isinstance(x, (int,float)) and not isinstance(x, bool) for x in node):
            for h in hints:
                if h not in found and re.search(h, path, re.I):
                    found[h] = (path, node)
            continue
        if isinstance(node, list):
            for i, x in enumerate(node[:2000]):
                if isinstance(x, (dict, list)):
                    stack.append((f"{path}[{i}]", x))
    return found

def main():
    repo = Path(".")
    results = repo / "results"
    figdir = results / "figures"
    figdir.mkdir(parents=True, exist_ok=True)

    files = sorted(list(results.glob("S*.json")))
    if not files:
        files = [p for p in results.glob("*.json") if "_scenario_inputs" not in str(p)]
        files = sorted(files)

    created = 0
    for p in files:
        obj = json.loads(p.read_text(encoding="utf-8"))
        sid = obj.get("scenario_id") or p.stem
        hints = [r"o2|oxygen", r"water|h2o"]
        found = find_series(obj, hints)
        # pick best matches
        o2 = found.get(hints[0])
        wa = found.get(hints[1])
        if not o2 and not wa:
            continue

        fig = plt.figure()
        if o2:
            path, series = o2
            plt.plot(range(len(series)), series, label=f"O2 ({path})")
        if wa:
            path, series = wa
            plt.plot(range(len(series)), series, label=f"Water ({path})")
        plt.xlabel("t (index)")
        plt.ylabel("quantity (model units)")
        plt.title(f"{sid}: depletion series")
        plt.legend()
        out = figdir / f"{sid}_depletion.png"
        fig.savefig(out, dpi=160, bbox_inches="tight")
        plt.close(fig)
        created += 1
        print(f"[figures] wrote {out.as_posix()}")

    if created == 0:
        print("[figures] No numeric O2/Water series found in JSON. Skipping figures truthfully.")
    else:
        print(f"[figures] OK: created {created} PNG(s).")

if __name__ == "__main__":
    main()