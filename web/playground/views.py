from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
import jsonpickle
from sklearn.tree import DecisionTreeClassifier

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

classifier = ai.train(seasons)
ai.report(seasons, classifier)

def hello(request):
    context = {
        'seasons': [seasons[i].period for i in range(len(seasons)) if i > 9],
        'startSeason': seasons[10].period
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
        at = dict()

        at['odds_home'] = [match['home_team_odds']]
        at['odds_away'] = [match['away_team_odds']]
        at['preseason'] = [match['preseason']]
        at['form'] = [float(match['home_team_form']) / float(match['away_team_form'])]

        attributes = pd.DataFrame(data=at)
        labels = classifier.predict(attributes)
        winner = match['home_team'] if int(labels[0]) == 1 else match['away_team']
        return Response(jsonpickle.encode(winner, unpicklable=False))  # return winner
