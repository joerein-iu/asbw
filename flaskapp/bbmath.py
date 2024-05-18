import pandas as pd
import math
from scipy.stats import norm

full = pd.read_csv('flaskapp/stats.csv')

# att = runs per inning/ average runs per inning
# def = oppositie

avg_rpi = full['R/G'].mean()/9
avg_rapi = full['RA/G'].mean()/9

def get_team_rpi(df, team):
    team_row = df[df['Tm'] == team]

    team_rg = team_row["R/G"].values[0]
    return team_rg/9

def get_full_rpi(df):
    team_dict = {}

    for index, row in df.iterrows():
        team_name = row["Tm"]
        team_rpi = row['R/G']/9
        team_dict[team_name] = round(team_rpi,2)

    return team_dict

def get_full_rapi(df):
    team_dict = {}

    for index, row in df.iterrows():
        team_name = row["Tm"]
        team_rpi = row['RA/G']/9
        team_dict[team_name] = round(team_rpi,2)

    return team_dict

def get_team_rg(df, team_name):
    team_row = df[df['Tm'] == team_name]
    team_rg = team_row['R/G'].values[0]
    return team_rg

def get_team_score(df, team, adv):
    full_rpi = get_full_rpi(df)
    full_rapi = get_full_rapi(df)
    att = full_rpi[team] / avg_rpi
    defense = full_rapi[team] /avg_rapi

    if adv == "home":
        score = att * defense * get_team_rg(df, team) * math.sqrt(1.03)

    elif adv == "away":
        score = att * defense * get_team_rg(df, team) * (1/math.sqrt(1.03))

    return round(score,2)

def calculate_win_probability(home_score, away_score, std_dev=2):
    # Assuming a standard deviation of 2 runs for simplicity
    # Calculate the probability of home team winning
    diff = home_score - away_score
    prob_home_win = norm.cdf(diff / std_dev)
    prob_away_win = 1 - prob_home_win
    return round(prob_home_win, 2), round(prob_away_win, 2)

def calculate_implied_probability(odds):
    if odds < 0:
        return round(abs(odds) / (abs(odds) + 100), 3)
    else:
        return round(100 / (odds + 100), 3)







