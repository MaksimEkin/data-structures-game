from django.urls import path
from . import views

urlpatterns = [

    # API Calls
    path('api', views.api_overview, name='game-board-api_overview'),
    path('api/start_game/<int:difficulty>/<str:player_ids>/<str:data_structures>/<str:online>', views.start_game, name='game-board-start_game'),
    path('api/board/<int:game_id>', views.board, name='game-board-game_status'),
    path('api/rebalance/<str:graph>', views.rebalance, name='game-board-rebalance'),
    path('api/action/<str:card>', views.action, name='game-board-action')
]