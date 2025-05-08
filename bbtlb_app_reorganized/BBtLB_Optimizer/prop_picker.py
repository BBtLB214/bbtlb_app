# BBtLB_Optimizer/prop_picker.py

import pandas as pd
from monte_carlo_sim import run_monte_carlo

THRESHOLD_VALUE = 5.0


def pick_props(sim_df: pd.DataFrame):
    props = []
    for _, row in sim_df.iterrows():
        median = row['Sim_Median']
        floor = row['Sim_Floor']
        ceiling = row['Sim_Ceiling']
        boom_prob = row['Boom_Prob']
        bust_prob = row['Bust_Prob']

        # Buy Over: strong median + high upside + low bust risk
        if median > THRESHOLD_VALUE and boom_prob > 30 and bust_prob < 20:
            props.append({
                "Player": row['Player'],
                "Type": "Over",
                "Target": median,
                "Confidence": boom_prob,
                "Range": f"{floor}-{ceiling}"
            })

        # Buy Under: low median + low boom chance + high bust chance
        elif median < THRESHOLD_VALUE and boom_prob < 20 and bust_prob > 30:
            props.append({
                "Player": row['Player'],
                "Type": "Under",
                "Target": median,
                "Confidence": bust_prob,
                "Range": f"{floor}-{ceiling}"
            })
    return props


def run_prop_picker():
    sim_df = run_monte_carlo()
    props = pick_props(sim_df)
    return pd.DataFrame(props)


if __name__ == '__main__':
    df = run_prop_picker()
    print("Suggested Props:")
    print(df.head(10))
