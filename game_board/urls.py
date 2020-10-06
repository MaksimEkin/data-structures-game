from django.urls import path
from . import views

urlpatterns = [
    path('api', views.api_overview, name='game-board-api_overview'),
    path('api/start_game/<int:difficulty>', views.start_game, name='game-board-start_game'),
    path('api/game_status/<int:game_id>', views.game_status, name='game-board-game_status')
]