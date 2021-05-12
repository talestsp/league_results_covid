import pandas as pd

WINNING_PTS = 3
DRAWING_PTS = 1
LOOSING_PTS = 0

def single_match_points(match_row: pd.Series):
    '''
    Compute match points for a single match row.
    :param match_row: Row representing a sigle match between two teams.
    :return:
    '''
    if match_row["FTHG"] > match_row["FTAG"]:
        return {"home_pts": WINNING_PTS, "away_pts": LOOSING_PTS}
    elif match_row["FTHG"] == match_row["FTAG"]:
        return {"home_pts": DRAWING_PTS, "away_pts": DRAWING_PTS}
    else:
        return {"home_pts": LOOSING_PTS, "away_pts": WINNING_PTS}


def matches_points(matches: pd.DataFrame):
    '''
    Compute all match points.
    :param matches: Team(s) matches table.
    :return:
    '''
    team_matches_points = matches.apply(single_match_points, axis=1).to_frame()

    team_matches_points_rows = []
    indexes = []

    for i, team_match_points in team_matches_points.iterrows():
        indexes.append(i)
        team_matches_points_rows.append(team_match_points.item())

    team_matches_points_df = pd.DataFrame(team_matches_points_rows, index=indexes)
    matches_points_df = matches.join(team_matches_points_df)
    try:
        matches_points_df = matches.name
    except AttributeError:
        pass

    return matches_points_df

def season_pts(matches: pd.DataFrame):
    '''
    Computer season points for each team both away and home matches
    :param matches: Team(s) matches table.
    :return:
    '''
    season_home_pts = matches.groupby("HomeTeam")["home_pts"].sum().sort_values(ascending=False)
    season_away_pts = matches.groupby("AwayTeam")["away_pts"].sum().sort_values(ascending=False)
    return (season_home_pts + season_away_pts).sort_values(ascending=False)

def team_matches(matches: pd.DataFrame, team: str, role: str=None):
    '''
    Filter matches dataframe by informed team and role.
    :param matches: Team(s) matches table.
    :param team: Team name.
    :param role: Either "home" or "away".
    :return: A matches dataframe filtered by team name and role.
    '''
    if role is None:
        return matches[(matches["HomeTeam"] == team) | (matches["AwayTeam"] == team)]

    elif role.upper() == "HOME":
        return matches[matches["HomeTeam"] == team]

    elif role.upper() == "AWAY":
        return matches[matches["AwayTeam"] == team]

def season_table(season_df: pd.DataFrame, team_names: list = None):
    '''
    Given all the matches it returns the league classification table with some descriptive statistics.
    :param season_df: Raw data with all teams.
    :param team_names: Filter for the informed teams.
    :return: A pd.DataFrame with computed statistics for each team.
    '''
    if team_names is None:
        team_names = season_df["HomeTeam"].append(season_df["AwayTeam"]).drop_duplicates()

    pts_data = []
    for team in team_names:
        home_team_matches = team_matches(season_df, team, "home")
        away_team_matches = team_matches(season_df, team, "away")

        if len(home_team_matches.append(away_team_matches)) == 0:
            home_pts, away_pts, pts, home_pts_percent, away_pts_percent = 0, 0, 0, 0, 0
            home_goals, away_goals, goals, home_goals_percent, away_pts_percent = 0, 0, 0, 0, 0
        else:
            home_pts = home_team_matches["home_pts"].sum()
            away_pts = away_team_matches["away_pts"].sum()
            pts = home_pts + away_pts
            home_pts_percent = home_pts / pts
            away_pts_percent = away_pts / pts

            home_goals = home_team_matches["FTHG"].sum()
            away_goals = away_team_matches["FTAG"].sum()
            goals = home_goals + away_goals
            home_goals_percent = home_goals / goals
            away_goals_percent = away_goals / goals

            home_goals_mean = home_goals / len(home_team_matches)
            away_goals_mean = away_goals / len(away_team_matches)
            goals_mean = goals / (len(home_team_matches) + len(away_team_matches))

        pts_data.append({"season": season_df["Season"].drop_duplicates().item(),
                         "team": team,
                         "pts": pts,
                         "home_pts": home_pts,
                         "away_pts": away_pts,
                         "home_pts_percent": home_pts_percent,
                         "away_pts_percent": away_pts_percent,
                         "goals": goals,
                         "home_goals": home_goals,
                         "away_goals": away_goals,
                         "home_goals_percent": home_goals_percent,
                         "away_goals_percent": away_goals_percent,
                         "goals_mean": goals_mean,
                         "home_goals_mean": home_goals_mean,
                         "away_goals_mean": away_goals_mean,
                         "home_matches": len(home_team_matches),
                         "away_matches": len(away_team_matches)})

    pts_data_df = pd.DataFrame(pts_data).sort_values("pts", ascending=False).reset_index(drop=True)

    pts_data_df["pos"] = pts_data_df["pts"].rank(method="min", ascending=False).astype(int)

    return pts_data_df.sort_values("pos", ascending=True)
