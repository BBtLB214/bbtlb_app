# dk_fd_builder.py

import pandas as pd
from monte_carlo_sim import run_monte_carlo
from projection_engine import get_player_projections

SALARY_CAPS = {
    'DraftKings': 50000,
    'FanDuel': 60000,
}

ROSTER_RULES = {
    'NBA': {
        'positions': ['PG', 'SG', 'SF', 'PF', 'C', 'G', 'F', 'UTIL', 'UTIL'],
        'size': 9,
    },
    'NFL': {
        'positions': ['QB', 'RB', 'RB', 'WR', 'WR', 'WR', 'TE', 'FLEX', 'DST'],
        'size': 9,
    },
    'NHL': {
        'positions': ['C', 'C', 'W', 'W', 'D', 'D', 'G', 'UTIL'],
        'size': 8,
    },
    'MLB': {
        'positions': ['P', 'P', 'C', '1B', '2B', '3B', 'SS', 'OF', 'OF', 'OF'],
        'size': 10,
    }
}


def is_valid_lineup(lineup, sport):
    if len(lineup) != ROSTER_RULES[sport]['size']:
        return False
    return True


def value_score(player):
    return player['Sim_Median'] / player['Salary']


def generate_lineups(sim_df, cap, sport):
    sim_df['Value'] = sim_df.apply(lambda x: value_score(x), axis=1)
    sim_df = sim_df[sim_df['Sport'] == sport]
    sim_df = sim_df.sort_values(by=['Value', 'Sim_Ceiling'], ascending=False)

    lineup_size = ROSTER_RULES[sport]['size']
    lineups = []
    used = set()

    for _ in range(100):
        lineup = []
        total_salary = 0
        for _, row in sim_df.iterrows():
            if row['Player'] in used:
                continue
            if len(lineup) >= lineup_size:
                break
            if total_salary + row['Salary'] > cap:
                continue
            lineup.append(row)
            used.add(row['Player'])
            total_salary += row['Salary']
        if is_valid_lineup(lineup, sport):
            lineups.append(lineup)
    return lineups


def format_lineups(lineups):
    formatted = []
    for lineup in lineups:
        formatted.append([
            {
                "Player": p['Player'],
                "Sport": p['Sport'],
                "Position": p.get('Position', ''),
                "Team": p.get('Team', ''),
                "Salary": p['Salary'],
                "Proj": f"{p['Sim_Median']}/{p['Sim_Floor']}/{p['Sim_Ceiling']}",
                "Value": round(p['Value'], 3),
                "Boom%": p['Boom_Prob'],
                "Bust%": p['Bust_Prob']
            }
            for p in lineup
        ])
    return formatted


def run_optimizer():
    sim_df = run_monte_carlo()
    projections = get_player_projections()
    proj_map = {p['Player']: p for p in projections}

    sim_df['Salary'] = sim_df['Player'].apply(lambda name: proj_map.get(name, {}).get('Salary', 5000))
    sim_df['Sport'] = sim_df['Player'].apply(lambda name: proj_map.get(name, {}).get('Sport', 'NBA'))
    sim_df['Position'] = sim_df['Player'].apply(lambda name: proj_map.get(name, {}).get('Position', 'UTIL'))

    results = {}
    for sport in ROSTER_RULES:
        dk_lineups = generate_lineups(sim_df.copy(), SALARY_CAPS['DraftKings'], sport)
        results[sport] = format_lineups(dk_lineups[:3])

    return results


if __name__ == '__main__':
    results = run_optimizer()
    for sport, lineups in results.items():
        print(f"\nDraftKings {sport} Lineups:")
        for l in lineups:
            print(l)
