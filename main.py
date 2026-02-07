import argparse
import os
import matplotlib.pyplot as plt

from models.model import Scenario, simulate

def parse_args():
    ap = argparse.ArgumentParser("Mars colony viability (strict verified constants only)")
    ap.add_argument("--N0", type=int, required=True)
    ap.add_argument("--years", type=int, default=50)
    ap.add_argument("--dt_days", type=float, default=1.0)

    ap.add_argument("--o2_storage_days", type=float, required=True)
    ap.add_argument("--water_storage_days", type=float, required=True)

    ap.add_argument("--o2_local_fraction", type=float, required=True)
    ap.add_argument("--water_local_fraction", type=float, required=True)
    ap.add_argument("--water_recovery_fraction", type=float, default=0.98)

    ap.add_argument("--launch_window_days", type=int, default=780)
    ap.add_argument("--missed_window_probability", type=float, default=0.15)

    ap.add_argument("--import_restore_fraction_o2", type=float, default=0.20)
    ap.add_argument("--import_restore_fraction_water", type=float, default=0.20)

    ap.add_argument("--cruise_days", type=int, default=253)  # mission design choice; user-specified
    ap.add_argument("--seed", type=int, default=123)
    ap.add_argument("--outdir", type=str, default="figures")
    return ap.parse_args()

def main():
    a = parse_args()
    sc = Scenario(
        N0=a.N0,
        years=a.years,
        dt_days=a.dt_days,
        o2_storage_days=a.o2_storage_days,
        water_storage_days=a.water_storage_days,
        o2_local_fraction=a.o2_local_fraction,
        water_local_fraction=a.water_local_fraction,
        water_recovery_fraction=a.water_recovery_fraction,
        launch_window_days=a.launch_window_days,
        missed_window_probability=a.missed_window_probability,
        import_restore_fraction_o2=a.import_restore_fraction_o2,
        import_restore_fraction_water=a.import_restore_fraction_water,
        cruise_days=a.cruise_days,
    )

    res = simulate(sc, seed=a.seed)

    os.makedirs(a.outdir, exist_ok=True)

    # Plot
    plt.figure()
    plt.plot(res["t_days"], res["o2_stock_days"], label="O2 stock (days)")
    plt.plot(res["t_days"], res["water_stock_days"], label="Water stock (days)")
    plt.xlabel("Time (days)")
    plt.ylabel("Stock (days of coverage)")
    plt.title("Mars Colony Critical Resources (Strict Verified Constants)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(a.outdir, "stocks.png"))
    plt.close()

    # Report
    print("=== STRICT MODEL REPORT ===")
    print(f"N0: {a.N0}")
    print(f"Collapsed: {res['collapsed']}")
    print(f"Collapse day: {res['collapse_day']}")
    print(f"Total dose (mSv) bookkeeping: {res['dose_msv_total']:.2f}")
    print(f"O2 demand (kg/day): {res['o2_demand_kg_per_day']:.2f}")
    print(f"Water demand (kg/day): {res['water_demand_kg_per_day']:.2f}")
    print("Figure saved: figures/stocks.png")

if __name__ == "__main__":
    main()
