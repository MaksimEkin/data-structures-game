"""
    API for Game Board that allows interaction with boards.
"""
import json
import random
from time import sleep
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle
from rest_framework.throttling import UserRateThrottle
from rest_framework.decorators import throttle_classes
from game_board.api import utils
from game_board.avl import avl_handler as avl
from game_board.ai import ai_handler as ai
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
        'Re-balance Tree': '/rebalance/<str:game_id>',
        'Action': '/action/<str:card>/<str:game_id>'
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
    player_ids = player_ids.split(',')
    data_structures = data_structures.split(',')

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
    del response_status['game_board']['graph']['uid']

    return Response(response_status['game_board'])


@api_view(['POST'])
def rebalance(request, game_id):
    """
    Re-balance a un-balanced AVL tree.

    :param request:
    :param game_id: unique identifier of the board
    :return game board JSON:
    """

    # Get the POST request
    post_request = json.loads(request.body)
    try:
        adjacency_list = post_request['adjacency_list']
    except Exception as err:
        return Response({'error': str(err)},
                        status=status.HTTP_400_BAD_REQUEST)

    # Load the game board from database
    response_status = utils.load_board_db(game_id)
    if response_status['error']:
        return Response({'error': response_status['reason']},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    board = response_status['game_board']

    #  Check for invalid action
    if board['curr_data_structure'] != 'AVL':
        return Response({'invalid_action': 'Re-balance can be performed for an AVL!'})

    check = utils.cheat_check(game_board=board, rebalance=True)
    if check['cheat']:
        return Response({'invalid_action': check['reason']},
                        status=status.HTTP_400_BAD_REQUEST)

    # Do the re-balance action and get the new state of the graph
    if board['curr_data_structure'] == 'AVL':
        graph = avl.avlRebalance(board['graph'])
    else:
        graph = avl.avlRebalance(board['graph']) # change this if adding stack
    board['graph'] = graph

    # If not correct lose points
    if board['graph']['adjacency_list'] != adjacency_list:
        board['player_points'][board['turn']] -= config.LOSS[str(board['difficulty'])]
    else:
        board['player_points'][board['turn']] += config.GAIN[str(board['difficulty'])]

    # Update board
    response_status = utils.update_board_db(board)
    if response_status['error']:
        return Response({'error': response_status['reason']},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    board_response = response_status['game_board']

    return Response(board_response)


@api_view(['GET'])
def action(request, card, game_id):
    """
    Perform action on the Data Structure using a card

    :param request:
    :param card: what action to be performed
    :param game_id: unique identifier of the board
    :return game board JSON:
    """

    # Load the game board from database
    response_status = utils.load_board_db(game_id)
    if response_status['error']:
        return Response({'error': response_status['reason']},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    board = response_status['game_board']

    # Check for invalid action
    check = utils.cheat_check(game_board=board, card=card)
    if check['cheat']:
        return Response({'invalid_action': check['reason']},
                        status=status.HTTP_400_BAD_REQUEST)

    # Give the points
    if card.split(' ')[0] in config.GAIN_TIMES[board['curr_data_structure']]:
        point = config.GAIN_TIMES_POINTS[card.split(' ')[0]]
        board['player_points'][board['turn']] += point

    # Perform the action on the data structure
    if board['curr_data_structure'] == 'AVL':
        graph = avl.avlAction(card, board['graph'], balance=False)
    # Currently only AVL supported
    else:
        graph = avl.avlAction(card, board['graph'], balance=False)

    # Update the graph with the new graph state
    board['graph'] = graph
    # Make sure deck is not empty
    if len(board['deck']) == 0:  # for now this checks deck so everyone always has 3 cards.
                                 # Could check hand but not sure how that will affect frontend
        pass

    # Pick a new card
    else:
        board['cards'][board['turn']].remove(card)
        new_card = board['deck'].pop(0)
        board['cards'][board['turn']].append(new_card)

    # Update the board on database
    response_status = utils.update_board_db(board)
    if response_status['error']:
        return Response({'error': response_status['reason']},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    board_response = response_status['game_board']
    return Response(board_response)


@api_view(['GET'])
def ai_pick(request, game_id):
    """
    Have an AI pick a move to execute

    :param request:
    :param game_id: unique identifier of the board
    :return card: string that represents a valid action for current player to take
    """
    # Load the game board from database
    response_status = utils.load_board_db(game_id)
    if response_status['error']:
        return Response({'error': response_status['reason']},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Grab the board
    board = response_status['game_board']
    if not board['turn'].replace(" ", "").lower().startswith(config.BOT_NAME_PREFIX):
        return Response({'error': 'The current player is not a BOT'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # tree is unbalanced,
    if not board['balanced']:

        # calculate the balance decision threshold
        # if it is higher than the limit for the difficulty, points will be lost
        balance_thresh = random.randint(1, 100)
        if balance_thresh <= config.REBAL_CHANCE[str(board['difficulty'])]:

            # Do the re-balance action and get the new state of the graph
            if board['curr_data_structure'] == 'AVL':
                graph = avl.avlRebalance(board['graph'])
            else:
                graph = avl.avlRebalance(board['graph'])  # change this if adding stack
            board['graph'] = graph

    # tree is balanced, can pick a move
    else:
        ordered_cards = utils.ai_format_hands(board)
        card = ai.select_move(board['graph'],
                              board['curr_data_structure'],
                              ordered_cards,
                              board['deck'],
                              max_depth=20)  # not sure what an appropriate search depth would be... 5 is pretty fast

        # Give the points
        if card.split(' ')[0] in config.GAIN_TIMES[board['curr_data_structure']]:
            point = board['graph']['node_points'][card.split()[1]]
            board['player_points'][board['turn']] += point

        # Perform the action on the data structure
        if board['curr_data_structure'] == 'AVL':
            graph = avl.avlAction(card, board['graph'], balance=True)
        # Currently only AVL supported
        else:
            graph = avl.avlAction(card, board['graph'], balance=True)

        # Update the graph with the new graph state
        board['graph'] = graph
        # Make sure deck is not empty
        if len(board['deck']) == 0:  # for now this checks deck so everyone always has 3 cards.
                                     # Could check hand but not sure how that will affect frontend
            pass

        # Pick a new card
        else:
            board['cards'][board['turn']].remove(card)
            new_card = board['deck'].pop(0)
            board['cards'][board['turn']].append(new_card)

    # Update the board on database
    response_status = utils.update_board_db(board)
    if response_status['error']:
        return Response({'error': response_status['reason']},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    board_response = response_status['game_board']
    sleep(config.BOT_SLEEP_TIME)
    return Response(board_response)
