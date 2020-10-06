from django.shortcuts import render

from django.http import HttpResponse
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .database import game_board_db

@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'Start Game' : '/start_game/<int:difficulty>',
        'Game Status' : '/game_status/<int:id>'
    }
    return Response(api_urls)


@api_view(['GET'])
def game_status(request, game_id):

    try:
        game_state = game_board_db.read_game(int(game_id))
    except Exception as e:
        return Response({'Error': str(e)})

    if game_state == None:
        return Response({'Not Found!'})

    sample = {
        'To-Do' : 'Currently being implemented!',
        'Input' : str(game_id),
        'Game' : game_state['game id'],
        'Data Structure State' : game_state['game state'],
        'Points' : game_state['points'],
        'Turn' : game_state['player id current turn']
    }
    return Response(sample)

@api_view(['GET', 'POST'])
def start_game(request, difficulty):
    sample = {
        'To-Do' : 'Currently being implemented!',
        'Input' : str(difficulty)
    }
    return Response(sample)