from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
import jsonpickle

from playground.models import Season, Team, Match

seasons = [Season("2008/2009", [Team("A", 10), Team("B", 10)], [Match("27-03-2022", Team("A", 10), Team("B", 10), 54, 55)]), Season("2009/2010", [Team("A", 10), Team("B", 10)], [])]


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