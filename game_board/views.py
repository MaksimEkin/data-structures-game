from django.shortcuts import render

from django.http import HttpResponse
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .database import game_board_db as db

@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'Start Game'      : '/start_game/<int:difficulty>/<int:num_players>/<bool:online>',
        'Game Board'      : '/board/<int:id>',
        'Re-balance Tree' : '/rebalance/<str:graph>',
        'Action'          : '/action/<str:card>'
    }
    return Response(api_urls)


@api_view(['GET', 'POST'])
def start_game(request, difficulty, num_players, online):
    sample = {
        'to-do'      : 'Currently being implemented!',
        'difficulty' : str(difficulty),
        'num_players': str(num_players),
        'online'     : bool(online),
        'game_id'    : 8
    }
    return Response(sample)


@api_view(['GET'])
def board(request, game_id):

    try:
        game_state = db.read_game(int(game_id))
    except Exception as e:
        return Response({'Error': str(e)})

    if game_state == None:
        return Response({'Not Found!'})

    sample = {
        'to-do'       : 'Currently being implemented!',
        'game_id'     : game_state['game id'],
        'graph'       : game_state['game state'],
        'player_ids'  : ['id2', 'id3', 'id4', 'id5'],
        'player_names': ['naomi', 'kulsoom', 'nick', 'ryan'],
        'points'      : {'id2':2, 'id3':2, 'id4':3, 'id5':10},
        'turn'        : game_state['player id current turn'],
        'cards'       : {'id2': ['card1','card2','card3'], 'id3': ['card1','card2','card3'], 'id4':['card1','card2','card3'], 'id5':['card1','card2','card3']},
        'gold_node'   : False,
        'difficulty'  : 'Medium',
        'num_players' : 4,
        'online'      : True
    }
    return Response(sample)


@api_view(['GET', 'POST'])
def rebalance(request, graph):
    sample = {
        'to-Do'     : 'Currently being implemented!',
        'graph'     : str(graph),
        'correct': True
    }
    return Response(sample)


@api_view(['GET', 'POST'])
def action(request, card):
    sample = {
        'to-Do'      : 'Currently being implemented!',
        'graph'      : "4(2(3)(1))(6(5))",
        'played'     : str(card),
        'new_card'   : 'card1',
        'turn'       : 2,
        'points'     : -20,
        'balanced'   : True,
        'golden_node': False
    }
    return Response(sample)
