from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
import jsonpickle
import pandas as pd
from playground.models import Season, Team, Match

jsonpickle.set_encoder_options('simplejson',
                               use_decimal=True, sort_keys=True)

seasons = list()

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
        if not home or not away:
            continue
        season_games.append(Match(dates[j], home, away, str(home_scores[j]), str(away_scores[j]), home_odds[j],
                                  away_odds[j], str(winners[j]), str(playoffs[j]), str(preseasons[j])))

    seasons[i - 8].matches = season_games


def hello(request):
    context = {
        'seasons': [season.period for season in seasons],
        'startSeason': seasons[0].period
    }
    return render(request, 'index.html', context)


class SeasonView(APIView):
    def get(self, request):
        period = request.GET.get('period', '')
        season = next(season for season in seasons if season.period == period)
        return Response(jsonpickle.encode(season, unpicklable=False))


class ResultView(APIView):
    def post(self, request):
        match = jsonpickle.decode(request.body.decode('utf-8'))
        winner = match['home_team'] if match['winner'] == '0' else match['away_team']
        return Response(jsonpickle.encode(winner, unpicklable=False))  # return winner
