import argparse
import pandas as pd
from BBtLB_App import prop_picker, ownership_leverage, dk_fd_builder, projection_engine

def run_prop_picker():
    print("[INFO] Running Prop Picker...")
    sim_df = prop_picker.run_monte_carlo()
    picks = prop_picker.pick_props(sim_df)
    for p in picks:
        print(p)

def run_ownership_leverage():
    print("[INFO] Running Ownership Leverage...")
    ownership_leverage.main()

def run_lineup_builder():
    print("[INFO] Running DK/FD Lineup Builder...")
    print("[WARN] Lineup builder integration pending.")

def run_projection_engine():
    print("[INFO] Running Projection Engine...")
    projections = projection_engine.generate_projections()
    print(pd.DataFrame(projections).head())

def main():
    parser = argparse.ArgumentParser(description="Run BBtLB modules")
    parser.add_argument("--module", choices=["prop", "ownership", "lineup", "projection"],
                        required=True, help="Module to run")
    args = parser.parse_args()

    if args.module == "prop":
        run_prop_picker()
    elif args.module == "ownership":
        run_ownership_leverage()
    elif args.module == "lineup":
        run_lineup_builder()
    elif args.module == "projection":
        run_projection_engine()

if __name__ == "__main__":
    main()
