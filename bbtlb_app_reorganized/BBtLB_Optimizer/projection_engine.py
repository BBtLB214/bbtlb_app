import numpy as np
from scipy.stats import norm
from data_ingestion import load_all_sources, extract_espn_injuries

def apply_knick_factor(player_name, injury_status):
    if injury_status == "ACTIVE":
        return 1.0
    elif injury_status in ["PROBABLE", "QUESTIONABLE"]:
        return 0.90
    elif injury_status == "DOUBTFUL":
        return 0.75
    elif injury_status == "OUT":
        return 0.0
    return 1.0

def calculate_projection(base_stat, std_dev, injury_modifier):
    floor = norm.ppf(0.2, loc=base_stat, scale=std_dev) * injury_modifier
    median = base_stat * injury_modifier
    ceiling = norm.ppf(0.9, loc=base_stat, scale=std_dev) * injury_modifier
    return round(floor, 2), round(median, 2), round(ceiling, 2)

def blend_sources(stats_json, odds_json, injuries):
    player_projections = []

    for team in stats_json.get("home", {}).get("players", []) + stats_json.get("away", {}).get("players", []):
        p = team.get("statistics", {})
        player_name = team.get("full_name", team.get("jersey_number", "Unknown"))

        base_fpts = (
            p.get("points", 0) * 1 +
            p.get("rebounds", 0) * 1.2 +
            p.get("assists", 0) * 1.5 +
            p.get("steals", 0) * 3 +
            p.get("blocks", 0) * 3 +
            p.get("turnovers", 0) * -1
        )

        std_dev = np.std([p.get("points", 0), p.get("rebounds", 0), p.get("assists", 0)]) or 5.0
        injury_status = injuries.get(player_name, "ACTIVE")
        knick_factor = apply_knick_factor(player_name, injury_status)

        floor, median, ceiling = calculate_projection(base_fpts, std_dev, knick_factor)
        value = 0 if median == 0 else round(median / 5000, 2)

        player_projections.append({
            "Player": player_name,
            "Proj (Med/Floor/Ceil)": f"{median}/{floor}/{ceiling}",
            "Value": value,
            "Knick Factor": injury_status
        })

    return player_projections

def get_player_projections():
    data = load_all_sources()
    injuries = extract_espn_injuries(data["espn"])
    projections = blend_sources(
        stats_json=data["sportsradar_stats"],
        odds_json=data["odds"],
        injuries=injuries
    )
    return projections

if __name__ == "__main__":
    import pprint
    pp = pprint.PrettyPrinter(depth=2)
    results = get_player_projections()
    pp.pprint(results)
