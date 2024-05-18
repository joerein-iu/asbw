from flask import Flask, request, render_template, redirect, url_for, jsonify
import pandas as pd
import math
from flaskapp.bbmath import get_team_score, full, calculate_win_probability

app = Flask(__name__)

def get_teams():
    file_path = 'flaskapp/stats.csv'
    df = pd.read_csv(file_path)
    teams = df['Tm'].unique().tolist()
    return teams

@app.route("/")
def render_index():
    return render_template("index.html")

@app.route("/matchup/")
def render_matchup():
    teams = get_teams()
    return render_template("matchup.html", teams=teams)

def calculate_implied_probability(odds):
    if odds < 0:
        return round(abs(odds) / (abs(odds) + 100), 3)
    else:
        return round(100 / (odds + 100), 3)

@app.route("/matchup/result", methods=["POST"])
def render_matchup_result():
    home_team = request.form["home"]
    away_team = request.form["away"]
    home_score = get_team_score(full, home_team, "home")
    away_score = get_team_score(full, away_team, "away")
    prob_home_win, prob_away_win = calculate_win_probability(home_score, away_score)

    # Get betting lines from the form
    home_line = int(request.form["home_line"])
    away_line = int(request.form["away_line"])
    implied_home_win = calculate_implied_probability(home_line)
    implied_away_win = calculate_implied_probability(away_line)
    
    return render_template("matchup_result.html", home_team=home_team, away_team=away_team, home_score=home_score, away_score=away_score, prob_home_win=prob_home_win, prob_away_win=prob_away_win, implied_home_win=implied_home_win, implied_away_win=implied_away_win)

if __name__ == "__main__":
    app.run(debug=True)
