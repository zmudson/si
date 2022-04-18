from django.urls import path
from . import views
from .views import SeasonView, ResultView

urlpatterns = [
    path('', views.hello),
    path(r'season', SeasonView.as_view()),
    path(r'result', ResultView.as_view())
]