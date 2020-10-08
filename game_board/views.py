from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .database import game_board_db as db
from . import utils
from . import config

from datetime import datetime
import json
from bson import json_util, ObjectId


@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'Start Game'      : '/start_game/<str:difficulty>/<str:player_ids>/<str:data_structures>/<bool:online>',
        'Game Board'      : '/board/<int:id>',
        'Re-balance Tree' : '/rebalance/<str:graph>/<str:player_id>/<str:game_id>',
        'Action'          : '/action/<str:card>/<str:player_id>/<str:game_id>'
    }
    return Response(api_urls)


@api_view(['GET', 'POST'])
def start_game(request, difficulty, player_ids, data_structures, online):

    if difficulty not in config.DIFFICULTY_LEVELS:
        return Response({'error': 'Difficulty level not found!',
                         'options': config.DIFFICULTY_LEVELS})

    player_ids = player_ids.split(',')
    data_structures = data_structures.split(',')

    try:
        game_id = db.create_game(utils.new_board(difficulty, player_ids, data_structures, online))
        game_id = json.loads(json_util.dumps(game_id))
        return Response({'game_id': game_id})
    except Exception as e:
        return Response({'error': str(e)})


@api_view(['GET'])
def board(request, game_id):

    Error, board = utils.load_board(game_id)
    if Error:
        return Response({'error': board})

    return Response(board)


@api_view(['GET', 'POST'])
def rebalance(request, graph, game_id):

    Error, board = utils.load_board(game_id)
    if Error:
        return Response({'error': board})

    cheat, reason = utils.cheat_check(game_board=board, rebalance=True)
    if cheat:
        return Response({'cheat_detected': reason})

    # Do the rebalance action with Nick's AVL lib here
    graph =  {'nodes': 'node4(node2(node3)(node1))(node6(node5))',
              'node_points': {'node1': 1, 'node2': 2, 'node3': 3, 'node4': 4, 'node5': 5, 'node6': 6},
              'gold_node': 'node5',
              'root_node': 'node3',
              'balanced': True}
    board['graph'] = graph

    try:
        db_response = db.update_game(game_id, board)
    except Exception as e:
        return Response({'error': str(e)})

    return Response(board)


@api_view(['GET', 'POST'])
def action(request, card, game_id):

    Error, board = utils.load_board(game_id)
    if Error:
        return Response({'error': board})

    cheat, reason = utils.cheat_check(game_board=board, card=card)
    if cheat:
        return Response({'cheat_detected': reason})

    # Do the card action with Nick's AVL lib here
    graph =  {'nodes': 'node4(node2(node3)(node1))(node6(node5))',
              'node_points': {'node1': 1, 'node2': 2, 'node3': 3, 'node4': 4, 'node5': 5, 'node6': 6},
              'gold_node': 'node5',
              'root_node': 'node3',
              'balanced': False}
    board['graph'] = graph

    # Remove the played card
    board['cards'][board['turn']].remove(card)
    # Pick a new card
    board['cards'][board['turn']].append(utils.pick_a_card(board))
    # Change turn
    next_player_index = (board['player_ids'].index(board['turn']) + 1) % len(board['player_ids'])
    board['turn'] = board['player_ids'][next_player_index]

    try:
        db_response = db.update_game(game_id, board)
    except Exception as e:
        return Response({'error': str(e)})

    return Response(board)
