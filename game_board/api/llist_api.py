"""
    API for Game Board that allows interaction with boards.
"""
import json
import random
from time import sleep
import uuid
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle
from rest_framework.throttling import UserRateThrottle
from rest_framework.decorators import throttle_classes
from game_board.api import utils
from .. import config


@api_view(['GET'])
def api_overview(request):
    """
    Overview of the API calls exist.

    :param request:
    :return: Response, list of API URLs.
    """
    api_urls = {
        'Start Game': '/start_game/<str:difficulty>/<str:player_ids>/<str:data_structures>',
        'Game Board': '/board/<str:id>'
    }
    return Response(api_urls)


@api_view(['GET'])
@throttle_classes([AnonRateThrottle])
@throttle_classes([UserRateThrottle])
def start_game(request, difficulty, player_ids, data_structures):
    """
    Creates a new game board.

    :param request:
    :param difficulty: game difficulty level
    :param player_ids: string of player IDs, comma seperated if more than one
    :param data_structures: string of data structures, comma seperated if more than one
    :return game board id:
    """

    # Chosen difficulty does not exist
    if difficulty not in config.DIFFICULTY_LEVELS:
        return Response({'error': 'Difficulty level not found!',
                         'options': config.DIFFICULTY_LEVELS},
                        status=status.HTTP_400_BAD_REQUEST)

    # Convert the string fields into list. Separate by comma if provided
    player_ids_temp = player_ids.split(',')
    data_structures = data_structures.split(',')

    player_ids = list()
    for pl_id in player_ids_temp:
        pl_id = str(pl_id).strip()

        # If empty player_ids is passed
        if len(pl_id) == 0:
            random_player = 'RedPanda_' + str(uuid.uuid1())[:5]
            while random_player in player_ids:
                random_player = 'RedPanda_' + str(uuid.uuid1())[:5]
            player_ids.append(random_player)
        else:
            player_ids.append(pl_id)

    # Shuffle players
    #random.shuffle(player_ids)

    # Check if the number of players request is valid
    if len(player_ids) > config.MAX_NUM_PLAYERS:
        return Response({'error': 'Too many players requested!',
                         'options': config.MAX_NUM_PLAYERS},
                        status=status.HTTP_400_BAD_REQUEST)

    # Create new game board JSON (dict), and store it in the database
    new_board = utils.new_board(difficulty, player_ids, data_structures)
    response_status = utils.create_board_db(new_board)

    if response_status['error']:
        return Response({'error': response_status['reason']},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'game_id': response_status['game_id']})




@api_view(['GET'])
def board(request, game_id):
    """
    Returns the current game board state.

    :param request:
    :param game_id: unique identifier of the board
    :return game board JSON:
    """

    response_status = utils.load_board_db(game_id)
    if response_status['error']:
        return Response({'error': response_status['reason']},
                        status=status.HTTP_400_BAD_REQUEST)

    # hide the UID used by data structure backend from user
    # del response_status['game_board']['graph']['uid']

    return Response(response_status['game_board'])
