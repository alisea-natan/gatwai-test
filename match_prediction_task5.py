import os

import requests
from dotenv import load_dotenv
from datetime import date, timedelta
import pandas as pd
from sklearn.ensemble import RandomForestClassifier


def get_upcoming_matches(base_url, API_KEY):
    today = date.today()
    tomorrow = today + timedelta(days=1)
    tomorrow_formatted = tomorrow.strftime("%Y-%m-%d")

    url = f"{base_url}GamesByDate/{tomorrow_formatted}"
    headers = {
        "Ocp-Apim-Subscription-Key": API_KEY
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        matches = response.json()
        return matches
    else:
        print("Failed to fetch upcoming matches. Status Code:", response.status_code)
        return None


def find_round_id(base_url, API_KEY, season):
    url = f"{base_url}Competitions"
    headers = {
        "Ocp-Apim-Subscription-Key": API_KEY
    }
    round_ids = []
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        info = response.json()
        for area in info:
            for season_area in area["Seasons"]:
                if season_area['Season'] == season:
                    for round1 in season_area["Rounds"]:
                        round_ids.append(round1["RoundId"])

        return list(set(round_ids))
    else:
        return []


def calculate_team_statistics(round_ids, base_url, API_KEY):
    data = pd.DataFrame(
        columns=['TeamId', 'TotalMatches', 'TotalWins', 'TotalLosses', 'TotalPoints', 'TotalScoreFor',
                 'TotalScoreAgainst'])
    for item in round_ids:
        url = f"{base_url}Standings/{item}"
        headers = {
            "Ocp-Apim-Subscription-Key": API_KEY
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            matches = response.json()
            for match in matches:
                team_id = match["TeamId"]
                if team_id in data["TeamId"].values:
                    data.loc[data["TeamId"] == team_id, 'TotalMatches'] += match["Games"]
                    data.loc[data["TeamId"] == team_id, 'TotalWins'] += match["Wins"]
                    data.loc[data["TeamId"] == team_id, 'TotalLosses'] += match["Losses"]
                    data.loc[data["TeamId"] == team_id, 'TotalPoints'] += match["Points"]
                    data.loc[data["TeamId"] == team_id, 'TotalScoreFor'] += match["ScoreFor"]
                    data.loc[data["TeamId"] == team_id, 'TotalScoreAgainst'] += match["ScoreAgainst"]
                else:
                    new_row = pd.DataFrame({'TeamId': team_id,
                                            'TotalMatches': match["Games"],
                                            'TotalWins': match["Wins"],
                                            'TotalLosses': match["Losses"],
                                            'TotalPoints': match["Points"],
                                            'TotalScoreFor': match["ScoreFor"],
                                            'TotalScoreAgainst': match["ScoreAgainst"]}, index=[team_id])
                    data = pd.concat([data, new_row])
    return data


def calculate_schedule_statistic(round_ids, base_url, API_KEY, team_df):
    data = pd.DataFrame(
        columns=['TotalMatchesA', 'TotalWinsA', 'TotalLossesA', 'TotalPointsA', 'TotalScoreForA', 'TotalScoreAgainstA',
                 'TotalMatchesB', 'TotalWinsB', 'TotalLossesB', 'TotalPointsB', 'TotalScoreForB', 'TotalScoreAgainstB',
                 'Winner'])
    for round_id in round_ids:
        url = f"{base_url}Schedule/{round_id}"
        headers = {
            "Ocp-Apim-Subscription-Key": API_KEY
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            info = response.json()
            for item in info:
                if (item["GameId"] not in data.index.values) and item["TeamAScore"] is not None:
                    data.loc[item["GameId"], 'TotalMatchesA'] = team_df.loc[team_df["TeamId"] == item["TeamAId"], "TotalMatches"].values[0] if len(
                            team_df.loc[team_df["TeamId"] == item["TeamAId"]]) > 0 else 0
                    data.loc[item["GameId"], 'TotalWinsA'] = team_df.loc[team_df["TeamId"] == item["TeamAId"], "TotalWins"].values[0] if len(
                            team_df.loc[team_df["TeamId"] == item["TeamAId"]]) > 0 else 0
                    data.loc[item["GameId"], 'TotalLossesA'] = team_df.loc[team_df["TeamId"] == item["TeamAId"], "TotalLosses"].values[0] if len(
                            team_df.loc[team_df["TeamId"] == item["TeamAId"]]) > 0 else 0
                    data.loc[item["GameId"], 'TotalPointsA'] = team_df.loc[team_df["TeamId"] == item["TeamAId"], "TotalPoints"].values[0] if len(
                            team_df.loc[team_df["TeamId"] == item["TeamAId"]]) > 0 else 0
                    data.loc[item["GameId"], 'TotalScoreForA'] = team_df.loc[team_df["TeamId"] == item["TeamAId"], "TotalScoreFor"].values[
                            0] if len(
                            team_df.loc[team_df["TeamId"] == item["TeamAId"]]) > 0 else 0
                    data.loc[item["GameId"], 'TotalScoreAgainstA'] = team_df.loc[team_df["TeamId"] == item["TeamAId"], "TotalScoreAgainst"].values[
                            0] if len(team_df.loc[team_df["TeamId"] == item["TeamAId"]]) > 0 else 0

                    data.loc[item["GameId"], 'TotalMatchesB'] = team_df.loc[team_df["TeamId"] == item["TeamBId"], "TotalMatches"].values[0] if len(
                            team_df.loc[team_df["TeamId"] == item["TeamBId"]]) > 0 else 0
                    data.loc[item["GameId"], 'TotalWinsB'] = team_df.loc[team_df["TeamId"] == item["TeamBId"], "TotalWins"].values[0] if len(
                            team_df.loc[team_df["TeamId"] == item["TeamBId"]]) > 0 else 0
                    data.loc[item["GameId"], 'TotalLossesB'] = team_df.loc[team_df["TeamId"] == item["TeamBId"], "TotalLosses"].values[0] if len(
                            team_df.loc[team_df["TeamId"] == item["TeamBId"]]) > 0 else 0
                    data.loc[item["GameId"], 'TotalPointsB'] = team_df.loc[team_df["TeamId"] == item["TeamBId"], "TotalPoints"].values[0] if len(
                            team_df.loc[team_df["TeamId"] == item["TeamBId"]]) > 0 else 0
                    data.loc[item["GameId"], 'TotalScoreForB'] = team_df.loc[team_df["TeamId"] == item["TeamBId"], "TotalScoreFor"].values[
                            0] if len(
                            team_df.loc[team_df["TeamId"] == item["TeamBId"]]) > 0 else 0
                    data.loc[item["GameId"], 'TotalScoreAgainstB'] = team_df.loc[team_df["TeamId"] == item["TeamBId"], "TotalScoreAgainst"].values[
                            0] if len(team_df.loc[team_df["TeamId"] == item["TeamBId"]]) > 0 else 0
                    data.loc[item["GameId"], 'Winner'] = "A" if item["TeamAScore"] > item["TeamBScore"] else "B" if item["TeamAScore"] < item["TeamBScore"] else "Draw"
    data.index.name = "GameId"
    return data


def calculate_next_match_stats(item, team_df):
    data = pd.DataFrame(
        columns=['TotalMatchesA', 'TotalWinsA', 'TotalLossesA', 'TotalPointsA', 'TotalScoreForA', 'TotalScoreAgainstA',
                 'TotalMatchesB', 'TotalWinsB', 'TotalLossesB', 'TotalPointsB', 'TotalScoreForB', 'TotalScoreAgainstB'])
    data.loc[item["GameId"], 'TotalMatchesA'] = team_df.loc[team_df["TeamId"] == item["TeamAId"], "TotalMatches"].values[0] if len(
                            team_df.loc[team_df["TeamId"] == item["TeamAId"]]) > 0 else 0
    data.loc[item["GameId"], 'TotalWinsA'] = team_df.loc[team_df["TeamId"] == item["TeamAId"], "TotalWins"].values[
        0] if len(
        team_df.loc[team_df["TeamId"] == item["TeamAId"]]) > 0 else 0
    data.loc[item["GameId"], 'TotalLossesA'] = team_df.loc[team_df["TeamId"] == item["TeamAId"], "TotalLosses"].values[
        0] if len(
        team_df.loc[team_df["TeamId"] == item["TeamAId"]]) > 0 else 0
    data.loc[item["GameId"], 'TotalPointsA'] = team_df.loc[team_df["TeamId"] == item["TeamAId"], "TotalPoints"].values[
        0] if len(
        team_df.loc[team_df["TeamId"] == item["TeamAId"]]) > 0 else 0
    data.loc[item["GameId"], 'TotalScoreForA'] = \
    team_df.loc[team_df["TeamId"] == item["TeamAId"], "TotalScoreFor"].values[
        0] if len(
        team_df.loc[team_df["TeamId"] == item["TeamAId"]]) > 0 else 0
    data.loc[item["GameId"], 'TotalScoreAgainstA'] = \
    team_df.loc[team_df["TeamId"] == item["TeamAId"], "TotalScoreAgainst"].values[
        0] if len(team_df.loc[team_df["TeamId"] == item["TeamAId"]]) > 0 else 0

    data.loc[item["GameId"], 'TotalMatchesB'] = \
    team_df.loc[team_df["TeamId"] == item["TeamBId"], "TotalMatches"].values[0] if len(
        team_df.loc[team_df["TeamId"] == item["TeamBId"]]) > 0 else 0
    data.loc[item["GameId"], 'TotalWinsB'] = team_df.loc[team_df["TeamId"] == item["TeamBId"], "TotalWins"].values[
        0] if len(
        team_df.loc[team_df["TeamId"] == item["TeamBId"]]) > 0 else 0
    data.loc[item["GameId"], 'TotalLossesB'] = team_df.loc[team_df["TeamId"] == item["TeamBId"], "TotalLosses"].values[
        0] if len(
        team_df.loc[team_df["TeamId"] == item["TeamBId"]]) > 0 else 0
    data.loc[item["GameId"], 'TotalPointsB'] = team_df.loc[team_df["TeamId"] == item["TeamBId"], "TotalPoints"].values[
        0] if len(
        team_df.loc[team_df["TeamId"] == item["TeamBId"]]) > 0 else 0
    data.loc[item["GameId"], 'TotalScoreForB'] = \
    team_df.loc[team_df["TeamId"] == item["TeamBId"], "TotalScoreFor"].values[
        0] if len(
        team_df.loc[team_df["TeamId"] == item["TeamBId"]]) > 0 else 0
    data.loc[item["GameId"], 'TotalScoreAgainstB'] = \
    team_df.loc[team_df["TeamId"] == item["TeamBId"], "TotalScoreAgainst"].values[
        0] if len(team_df.loc[team_df["TeamId"] == item["TeamBId"]]) > 0 else 0
    data.index.name = "GameId"
    return data


def make_prediction(game_stat_dataset, next_match_stat):
    X = game_stat_dataset.drop("Winner", axis=1)
    y = game_stat_dataset["Winner"]
    X = X.drop("TotalPointsA", axis=1)
    X = X.drop("TotalPointsB", axis=1)
    X = X.drop("TotalMatchesA", axis=1)
    X = X.drop("TotalMatchesB", axis=1)

    next_match_stat = next_match_stat.drop("TotalPointsA", axis=1)
    next_match_stat = next_match_stat.drop("TotalPointsB", axis=1)
    next_match_stat = next_match_stat.drop("TotalMatchesA", axis=1)
    next_match_stat = next_match_stat.drop("TotalMatchesB", axis=1)
    classifier = RandomForestClassifier(max_depth=10)
    classifier.fit(X, y)
    predictions = classifier.predict(next_match_stat)
    return predictions[0]


def start():
    base_url = "https://api.sportsdata.io/v3/lol/scores/json/"
    load_dotenv()
    API_KEY = os.getenv("GOLF_API")
    matches = get_upcoming_matches(base_url, API_KEY)

    if matches:
        next_match = matches[0]  # Assuming the first match is the next one
        season = next_match["Season"]
        round_ids = find_round_id(base_url, API_KEY, season)
        team_statistics_dataset = calculate_team_statistics(round_ids, base_url, API_KEY)
        if not os.path.isfile(os.path.join("data", "teams5.csv")):
            team_statistics_dataset.to_csv(os.path.join("data", "teams5.csv"))
        game_stat_dataset = calculate_schedule_statistic(round_ids, base_url, API_KEY, team_statistics_dataset)
        if not os.path.isfile(os.path.join("data", "game5.csv")):
            game_stat_dataset.to_csv(os.path.join("data", "game5.csv"))
        next_match_stat = calculate_next_match_stats(next_match, team_statistics_dataset)
        if not os.path.isfile(os.path.join("data", "to_predict.csv")):
            next_match_stat.to_csv(os.path.join("data", "to_predict.csv"))

        pred = make_prediction(game_stat_dataset, next_match_stat)
        if pred == "A":
            print(f"Team {next_match['TeamAName']} will win against {next_match['TeamBName']} "
                  f"on {next_match['DateTime']}.")
        elif pred == "B":
            print(f"Team {next_match['TeamBName']} will win against {next_match['TeamAName']} "
                  f"on {next_match['DateTime']}.")
        else:
            print(f"Draw will be between {next_match['TeamAName']} and {next_match['TeamBName']} "
                  f"on {next_match['DateTime']}")
    else:
        print("Game over, no more competitions left.")


if __name__ == "__main__":
    start()
