from django.urls import path
from . import views
from .views import SeasonView

urlpatterns = [
    path('', views.hello),
    path(r'season', SeasonView.as_view())
]