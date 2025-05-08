# BBtLB_Optimizer/ownership_leverage.py

import os
import requests
import pandas as pd
import numpy as np
from monte_carlo_sim import run_monte_carlo
from dotenv import load_dotenv

load_dotenv()

SPORTSDATAIO_API_KEY = os.getenv("SPORTSDATAIO_API_KEY")
SPORTSDATAIO_HEADERS = {
    'Ocp-Apim-Subscription-Key': SPORTSDATAIO_API_KEY
}

DK_SALARY_URL = "https://api.sportsdata.io/v4/nfl/dfs/slates"
OWNERSHIP_URL = "https://api.sportsdata.io/v4/nfl/dfs/ownership"


def fetch_ownership_projections():
    try:
        response = requests.get(OWNERSHIP_URL, headers=SPORTSDATAIO_HEADERS)
        response.raise_for_status()
        data = response.json()
        return {p['Name']: p['DraftKingsOwnershipPercentage'] for p in data if 'Name' in p}
    except requests.RequestException as e:
        print(f"[ERROR] Could not fetch ownership data: {e}")
        return {}


def fetch_salaries():
    try:
        response = requests.get(DK_SALARY_URL, headers=SPORTSDATAIO_HEADERS)
        response.raise_for_status()
        slates = response.json()
        salaries = {}
        for slate in slates:
            for game in slate.get("Games", []):
                for player in game.get("Players", []):
                    name = player.get("Name")
                    salary = player.get("DraftKingsSalary")
                    if name and salary:
                        salaries[name] = salary
        return salaries
    except requests.RequestException as e:
        print(f"[ERROR] Could not fetch salary data: {e}")
        return {}


def compute_leverage(sim_df: pd.DataFrame, ownership_map: dict, salary_map: dict):
    leverage_list = []
    for _, row in sim_df.iterrows():
        player = row['Player']
        median = row['Sim_Median']
        ownership = ownership_map.get(player, 10.0)
        salary = salary_map.get(player, 5000)

        leverage_score = round((median / salary) / (ownership / 100), 2)
        if leverage_score >= 1.5:
            leverage_list.append({
                "Player": player,
                "Team": row.get('Team', ''),
                "Proj": median,
                "Ownership%": round(ownership, 2),
                "Salary": salary,
                "Leverage": leverage_score
            })

    return pd.DataFrame(leverage_list).sort_values(by="Leverage", ascending=False)


def run_leverage_analysis():
    sim_df = run_monte_carlo()
    salary_map = fetch_salaries()
    sim_df['Salary'] = sim_df['Player'].map(lambda p: salary_map.get(p, 5000))
    ownership_map = fetch_ownership_projections()
    leverage_df = compute_leverage(sim_df, ownership_map, salary_map)
    return leverage_df


if __name__ == '__main__':
    df = run_leverage_analysis()
    print("Top Leverage Plays:")
    print(df.head(10))
