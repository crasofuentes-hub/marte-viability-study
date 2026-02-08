import csv, re
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def pick_col(cols, patterns):
    for pat in patterns:
        rx = re.compile(pat, re.I)
        for c in cols:
            if rx.search(c):
                return c
    return None

def to_float(x):
    if x is None: return None
    s = str(x).strip()
    if not s: return None
    try:
        return float(s)
    except:
        return None

def main():
    results = Path("results")
    csv_path = results / "summary.csv"
    if not csv_path.exists():
        print("[fig] summary.csv not found -> skip figures")
        return

    rows = []
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        cols = r.fieldnames or []
        for row in r:
            rows.append(row)

    if not rows:
        print("[fig] summary.csv empty -> skip figures")
        return

    cols = list(rows[0].keys())

    sid_col = pick_col(cols, [r"scenario[_ ]?id", r"scenario", r"id"])
    day_col = pick_col(cols, [r"collapse[_ ]?day", r"days[_ ]?elapsed", r"survival", r"days"])
    dose_col = pick_col(cols, [r"dose", r"msv", r"radiation"])
    o2_col = pick_col(cols, [r"o2", r"oxygen"])
    w_col  = pick_col(cols, [r"water", r"h2o"])

    # Build x labels
    sids = []
    for i, row in enumerate(rows):
        s = row.get(sid_col) if sid_col else None
        sids.append(s if s else f"row{i+1}")

    created = 0

    def plot_metric(metric_col, title, ylab, outname):
        nonlocal created
        ys = [to_float(row.get(metric_col)) for row in rows]
        if all(v is None for v in ys):
            return
        xs = list(range(len(ys)))
        plt.figure()
        plt.plot(xs, [v if v is not None else float("nan") for v in ys])
        plt.xticks(xs, sids, rotation=90, fontsize=6)
        plt.title(title)
        plt.ylabel(ylab)
        plt.tight_layout()
        out = results / "figures" / outname
        plt.savefig(out, dpi=180, bbox_inches="tight")
        plt.close()
        print(f"[fig] wrote {out.as_posix()}")
        created += 1

    # Always try to create at least 1 falsifiable plot
    if day_col:
        plot_metric(day_col, "Collapse/Survival Day by Scenario", "day", "collapse_day_by_scenario.png")
    if dose_col:
        plot_metric(dose_col, "Radiation Dose by Scenario", "mSv", "dose_msv_by_scenario.png")

    # Optional: only if summary contains them (may be scalar, not series)
    if o2_col:
        plot_metric(o2_col, "O2 Metric by Scenario (summary)", "model units", "o2_metric_by_scenario.png")
    if w_col:
        plot_metric(w_col, "Water Metric by Scenario (summary)", "model units", "water_metric_by_scenario.png")

    if created == 0:
        print("[fig] No plottable numeric columns found in summary.csv")
    else:
        print(f"[fig] OK: created {created} figure(s)")

if __name__ == "__main__":
    main()