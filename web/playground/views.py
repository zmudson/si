from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
import jsonpickle
from playground.models import Season, Team, Match
import time
import pandas as pd
import playground.ai as ai

jsonpickle.set_encoder_options('simplejson',
                               use_decimal=True, sort_keys=True)

seasons = list()
ai.read_preseason_odds(seasons)
ai.read_games_info(seasons)

ai.calc_form(seasons)

start_time = time.time()
print("siema")
#ai.train(seasons)
print("nara")

print(seasons[0].matches[-1].home_team_form, seasons[0].matches[1357].home_team_form, seasons[0].matches[1357].home_team.name)
print(seasons[0].matches[1346].away_team_form, seasons[0].matches[1346].away_team.name)
print(seasons[0].matches[1326].home_team_form, seasons[0].matches[1326].home_team.name)
print(seasons[0].matches[1314].home_team_form, seasons[0].matches[1314].home_team.name)
print(time.time()-start_time)

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
        winner = match['home_team_form'] if match['winner'] == '0' else match['away_team_form']
        return Response(jsonpickle.encode(winner, unpicklable=False))  # return winner
