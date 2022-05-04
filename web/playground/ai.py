from functools import reduce
import pandas as pd
from playground.models import Season, Team, Match

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score
import numpy as np
from sklearn.model_selection import train_test_split as split
from sklearn.tree import DecisionTreeClassifier

pd.options.mode.chained_assignment = None  # default='warn'


def read_preseason_odds(seasons):
    PATH = "data\\preseason-odds\\"

    for i in range(8, 21):
        if i == 8:
            READPATH = PATH + str(2000 + i) + '-0' + str(i + 1) + '-odds.csv'
        else:
            READPATH = PATH + str(2000 + i) + '-' + str(i + 1) + '-odds.csv'
        odds = pd.read_csv(READPATH)
        teams = odds.Team
        values = odds.Odds
        season_teams = list()
        for j in range(len(teams)):
            if teams[j] == 'New Orleans Hornets':
                teams[j] = 'New Orleans Pelicans'
            if teams[j] == 'Charlotte Bobcats':
                teams[j] = 'Charlotte Hornets'
            if teams[j] == 'New Jersey Nets':
                teams[j] = 'Brooklyn Nets'
            season_teams.append(Team(teams[j], values[j]))
        season_teams.sort(key=lambda x: x.name)

        seasons.append(Season(str(2000 + i) + '/' + str(2000 + i + 1), season_teams))


def read_games_info(seasons):
    PATH = "data\\games\\"

    for i in range(8, 21):
        READPATH = PATH + str(2000 + i) + '-' + str(2000 + i + 1) + '.csv'
        games = pd.read_csv(READPATH)

        dates = games.Date
        home_teams = games['Home Team']
        away_teams = games['Away Team']
        home_scores = games['Home Score']
        away_scores = games['Away Score']
        home_odds = games['Home Odds']
        away_odds = games['Away Odds']
        winners = games['Who Won']
        playoffs = games['Playoffs']
        preseasons = games['Preseason']

        season_games = list()
        for j in range(len(dates)):
            home = None
            away = None
            for team in seasons[i - 8].teams:
                if team.name == home_teams[j]:
                    home = team
                if team.name == away_teams[j]:
                    away = team
            if not home or not away or preseasons[j] or playoffs[j]:
                continue
            if home_odds[j] == '-':
                home_odds[j] = 1.85
            if away_odds[j] == '-':
                away_odds[j] = 1.85
            season_games.append(Match(dates[j], home, away, str(home_scores[j]), str(away_scores[j]), str(home_odds[j]),
                                      str(away_odds[j]), str(winners[j]), str(playoffs[j]), str(preseasons[j])))

        seasons[i - 8].matches = season_games


def calc_form(seasons):
    for season in seasons:
        teams_last_games = [list() for team in season.teams]
        max_games = 3
        for match in reversed(season.matches):
            home_team = match.home_team
            away_team = match.away_team
            home_team_last_games = teams_last_games[season.teams.index(home_team)]
            away_team_last_games = teams_last_games[season.teams.index(away_team)]
            match.home_team_form = reduce(lambda a, b: a * b, home_team_last_games) if len(
                home_team_last_games) > 0 else 1.0
            match.away_team_form = reduce(lambda a, b: a * b, away_team_last_games) if len(
                away_team_last_games) > 0 else 1.0
            if len(home_team_last_games) == max_games:
                home_team_last_games.pop(0)
            home_team_last_games.append(int(match.home_team_points) / int(match.away_team_points))
            if len(away_team_last_games) == max_games:
                away_team_last_games.pop(0)
            away_team_last_games.append(int(match.away_team_points) / int(match.home_team_points))


def find_ccp_alpha(alphas, attributes, labels):
    accuracy_train, accuracy_validate = [], []
    print(len(alphas))
    for i, alpha in enumerate(alphas):
        print(i)
        classifier = DecisionTreeClassifier(criterion="entropy", ccp_alpha=alpha)
        attributes_train, attributes_validate, labels_train, labels_validate = split(attributes, labels,
                                                                                     test_size=0.3)

        classifier.fit(attributes_train, labels_train)
        labels_predict_train = classifier.predict(attributes_train)
        labels_predict_validate = classifier.predict(attributes_validate)

        accuracy_train.append(accuracy_score(labels_train, labels_predict_train))
        accuracy_validate.append(accuracy_score(labels_validate, labels_predict_validate))

    sns.set()
    plt.figure(figsize=(20, 10))
    sns.lineplot(y=accuracy_train, x=alphas, label="Train accuracy")
    sns.lineplot(y=accuracy_validate, x=alphas, label="Validate accuracy")
    plt.xticks(ticks=np.arange(0.00, 0.10, 0.01))
    plt.xlabel("ccp_alpha")
    plt.ylabel("Wartość precyzji")
    plt.title("Wykres zależności precyzji od ccp_alpha")
    plt.savefig("data\\prunning.png")


def train(seasons):
    at, lb = get_data(seasons[:8])

    attributes = pd.DataFrame(data=at)
    labels = pd.DataFrame(data=lb)

    classifier = DecisionTreeClassifier(criterion="entropy", ccp_alpha=0.025)
    classifier = classifier.fit(attributes, labels)
    return classifier


def report(seasons, classifier):
    at, lb = get_data(seasons[9:])

    attributes = pd.DataFrame(data=at)
    labels = pd.DataFrame(data=lb)
    # Report
    from sklearn.metrics import classification_report
    print(classification_report(labels, classifier.predict(attributes)))


def get_data(seasons):
    at = dict()
    odds_home = list()
    odds_away = list()
    preseason = list()
    form = list()
    is_favorite_home_team = list()
    who_won = list()
    lb = dict()
    for i, season in enumerate(seasons):
        for match in reversed(season.matches):
            odds_home.append(match.home_team_odds)
            odds_away.append(match.away_team_odds)
            preseason.append(int(match.home_team.value) / int(match.away_team.value))
            form.append(match.home_team_form - match.away_team_form)
            is_favorite_home_team.append(1 if match.home_team_odds < match.away_team_odds else 0)
            who_won.append(match.winner)

    at['odds_home'] = odds_home
    at['odds_away'] = odds_away
    at['preseason'] = preseason
    at['form'] = form
    at['is_favorite_home_team'] = is_favorite_home_team
    lb['winner'] = who_won
    return at, lb
