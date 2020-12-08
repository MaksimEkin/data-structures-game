"""
    Home Page application URLs.
"""
from django.urls import path
from home_page.api import api
from . import views

urlpatterns = [
    path('', views.home, name='home-page'),

    # Homepage API call to get the ranking
    path('api', api.api_overview, name='homepage-api_overview'),
    path('api/rankings/<str:top_n>', api.rankings, name='game-board-ranking-top-n'),
]
