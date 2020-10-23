from django.urls import path
from game_board.api import api
from . import views

urlpatterns = [

    # Views
    path('', views.game_board, name='game-board'),

    # Game Play API Calls
    path('api', api.api_overview, name='game-board-api_overview'),
    path('api/start_game/<str:difficulty>/<str:player_ids>/<str:data_structures>', api.start_game, name='game-board-start_game'),
    path('api/board/<str:game_id>', api.board, name='game-board-game_status'),
    path('api/rebalance/<str:game_id>', api.rebalance, name='game-board-rebalance'),
    path('api/action/<str:card>/<str:game_id>', api.action, name='game-board-action'),
]