from django.shortcuts import render

from django.http import HttpResponse
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .database import game_board_db as db
from .mock import MockDB as mock_db
from . import utils

from datetime import datetime


@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'Start Game'      : '/start_game/<str:difficulty>/<str:player_ids>/<str:data_structures>/<bool:online>',
        'Game Board'      : '/board/<int:id>',
        'Re-balance Tree' : '/rebalance/<str:graph>',
        'Action'          : '/action/<str:card>'
    }
    return Response(api_urls)


@api_view(['GET', 'POST'])
def start_game(request, difficulty, player_ids, data_structures, online):

    player_ids = player_ids.split(',')
    data_structures = data_structures.split(',')
    nodes = ['node1', 'node2', 'node3']

    Cards = utils.generate_cards(player_ids, nodes, data_structures[0], 3, difficulty)

    sample = {
        'to-do' : 'Currently being implemented!',
        'Cards' : Cards,
        'pick' : utils.new_card(data_structures[0], nodes, difficulty)
    }
    return Response(sample)


@api_view(['GET'])
def board(request, game_id):

    try:
        # game_board = db.read_game(int(game_id))
        game_board = mock_db.read_game('game_id1234')

        # Remove the database entry ID
        del game_board['id_']

    except Exception as e:
        return Response({'Error': str(e)})

    if game_board == None:
        return Response({'Not Found!'})

    return Response(game_board)


@api_view(['GET', 'POST'])
def rebalance(request, graph):
    sample = {
        'to-Do'     : 'Currently being implemented!'
    }
    return Response(sample)


@api_view(['GET', 'POST'])
def action(request, card):
    sample = {
        'to-Do'      : 'Currently being implemented!'
    }
    return Response(sample)
