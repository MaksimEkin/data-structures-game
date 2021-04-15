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
        'Game Board': '/board/<str:id>',
        'Spawn Ant': '/spawn_ant/<str:game_id>',
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


    # Check if the number of players request is valid
    if len(player_ids) > config.LLIST_MAX_NUM_PLAYERS:
        return Response({'error': 'Too many players requested!',
                         'options': config.LLIST_MAX_NUM_PLAYERS},
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

@api_view(['GET'])
def dig_tunnel(request, game_id, origin, destination):
    """
    Attempts to dig a tunnel from the requested node to a requested destination
    :param game_id: unique identifier of the board
    :param origin: the node that the player wishes to dig from
    :param destination: the place that the player wishes to dig to (node name, 'surface', or 'none'
    """
    # Game must exist
    # Load the game board from database
    response_status = utils.load_board_db(game_id)
    if response_status['error']:
        return Response({'error': response_status['reason']},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    board = response_status['game_board']

    # origin and destination MUST be different
    if origin is destination:
        return Response({'invalid_action': 'origin cannot match destination'},
                        status=status.HTTP_400_BAD_REQUEST)

    # Player must still have dig 'energy' for that day
    if board['time_tracks']['dig_tunnel_track'] == 0:
        return Response({'invalid_action': 'no dig energy'},
                        status=status.HTTP_400_BAD_REQUEST)
    # Origin must exist
    if origin is not 'surface' and origin not in board['graph']['node_list']:
        return Response({'invalid_action': 'origin does not exist'},
                        status=status.HTTP_400_BAD_REQUEST)

    # If destination is NOT 'none', it must exist (node OR surface)
    if destination is not 'none' and destination not in board['graph']['node_list']:
        return Response({'invalid_action': 'destination does not exist'},
                        status=status.HTTP_400_BAD_REQUEST)

    # If Origin is surface, colony_entrance MUST be False
    if origin is 'surface' and board['colony_entrance'] is True:
        return Response({'invalid_action': 'colony_entrance already exists'},
                        status=status.HTTP_400_BAD_REQUEST)

    # There must be at least one ant at origin
    if origin is 'surface' and board['total_surface_ants'] == 0:
        return Response({'invalid_action': 'no ants on surface'},
                        status=status.HTTP_400_BAD_REQUEST)
    if board['graph']['num_ants'][origin] == 0:
        return Response({'invalid_action': 'no ants at origin'},
                        status=status.HTTP_400_BAD_REQUEST)

    # If destination is NOT none, there must be an ant at the destination
    if destination is not 'none' and board['graph']['num_ants'][destination] == 0:
        return Response({'invalid_action': 'no ants at destination'},
                        status=status.HTTP_400_BAD_REQUEST)

    # Origin node must NOT already have an exit tunnel
    if board['graph']['num_tunnels'][origin]['exit'] is True:
        return Response({'invalid_action': 'exit tunnel exists'},
                            status=status.HTTP_400_BAD_REQUEST)

    # destination must NOT already have an entrance tunnel
    if destination is not 'none' and board['graph']['num_tunnels'][destination]['entrance'] is True:
        return Response({'invalid_action': 'exit tunnel exists'},
                            status=status.HTTP_400_BAD_REQUEST)

    # if ALL checks are passed, create new tunnel and update ALL relevant gameboard parameters

    # num_tunnels
    board['graph']['num_tunnels'][origin]['exit'] = True
    board['graph']['num_tunnels'][origin]['next'] = destination
    if destination is not 'none':
        board['graph']['num_tunnels'][destination]['entrance'] = True


    if origin is 'surface':
        board['colony_entrance'] = True
    if destination is 'surface':
        board['colony_exit'] = True

    board['time_tracks']['dig_tunnel_track'] -= 1

    
    user_id = board['player_ids']
    token = -1

    # Update the board on database
    response_status = utils.update_board_db(board, user_id, token)
    if response_status['error']:
        return Response({'error': response_status['reason']},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    board_response = response_status['game_board']
    return Response(board_response)

@api_view(['GET'])
def spawn_ant(request, game_id):
    """
    Spawns an ant given the game ID
    :param game_id: unique identifier of the board
    :return game board JSON:
    """

    # Load the game board from database
    response_status = utils.load_board_db(game_id)
    if response_status['error']:
        return Response({'error': response_status['reason']},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    board = response_status['game_board']


    if not board['queen_at_head']:
        return Response({'invalid_action': 'lost queen'},
                        status=status.HTTP_400_BAD_REQUEST)

    # Make sure there is enough food to spawn a new ant
    if board['total_food'] < config.ANT_SPAWN_VAL:
        return Response({'invalid_action': 'not enough food'},
                        status=status.HTTP_400_BAD_REQUEST)


    # Take away food, if they have food that can be
    curr_food_types = board['total_food_types']

    # If player has a donut take it
    if curr_food_types[config.FORAGE_TYPES[2]] > 0:
        board['total_food_types'][config.FORAGE_TYPES[2]] -= 1
        board['total_food'] -= config.ANT_SPAWN_VAL
    # If player has at least one berry and one crumb, take one of each
    elif curr_food_types[config.FORAGE_TYPES[1]] > 0 and curr_food_types[config.FORAGE_TYPES[0]] > 0:
        board['total_food_types'][config.FORAGE_TYPES[1]] -= 1
        board['total_food_types'][config.FORAGE_TYPES[0]] -= 1
        board['total_food'] -= config.ANT_SPAWN_VAL
    # If player only has crumbs take it
    elif curr_food_types[config.FORAGE_TYPES[0]] >= config.ANT_SPAWN_VAL:
        board['total_food_types'][config.FORAGE_TYPES[0]] -= config.ANT_SPAWN_VAL
    # If this case is reached, the player has enough food, but only in berry form (not divisible by 3)
    elif curr_food_types[config.FORAGE_TYPES[1]] >= 2:
        board['total_food_types'][config.FORAGE_TYPES[1]] -= 2
        board['total_food_types'][config.FORAGE_TYPES[0]] += 1;
        board['total_food'] -= config.ANT_SPAWN_VAL
    else:
        return Response({'invalid_action': 'error occurred'},
                        status=status.HTTP_400_BAD_REQUEST)

    # if control reaches here, then spawning an ant is successful. Update both total and surface ant values.
    board['total_ants'] += 1
    board['total_surface_ants'] += 1

    user_id = board['player_ids']
    token = -1
    # Update the board on database
    response_status = utils.update_board_db(board, user_id, token)
    if response_status['error']:
        return Response({'error': response_status['reason']},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    board_response = response_status['game_board']
    return Response(board_response)

