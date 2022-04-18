from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
import jsonpickle
import pandas as pd

from playground.models import Season, Team, Match

seasons = list()

#C:\\Sem4\\SI-django\\si\\web\\
PATH = "data\\preseason-odds\\"

for i in range(8, 21):
    if i == 8:
        READPATH = PATH + str(2000+i) + '-0' + str(i+1) + '-odds.csv'
    else:
        READPATH = PATH + str(2000+i) + '-' + str(i+1) + '-odds.csv'
    odds = pd.read_csv(READPATH)
    teams = odds.Team
    values = odds.Odds
    season_teams = list()
    for j in range(len(teams)):
        season_teams.append(Team(teams[j], values[j]))
    seasons.append(Season(str(2000+i) + '/' + str(2000 + i + 1), season_teams))

#print(seasons[1].period)
PATH = "data\\games\\"

for i in range(8, 21):
    READPATH = PATH + str(2000+i) + '-' + str(2000+i+1) + '.csv'
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
        season_games.append(Match(dates[j], home_teams[j], away_teams[j], home_scores[j], away_scores[j], home_odds[j],
                                  away_odds[j], winners[j], playoffs[j], preseasons[j]))

    #debugging purposes
    #season_games[1000].print_match()
    
    seasons[i-8].matches = season_games

#seasons = [Season("2008/2009", [Team("A", 10), Team("B", 10)], [Match("27-03-2022", Team("A", 10), Team("B", 10), 54, 55)]), Season("2009/2010", [Team("A", 10), Team("B", 10)], [])]


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