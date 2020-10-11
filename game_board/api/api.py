from rest_framework.decorators import api_view
from rest_framework.response import Response

from game_board.api import utils
from game_board.avl import avl_handler as avl
from .. import config

import json
from bson import json_util


@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'Start Game'      : '/start_game/<str:difficulty>/<str:player_ids>/<str:data_structures>',
        'Game Board'      : '/board/<str:id>',
        'Re-balance Tree' : '/rebalance/<str:game_id>',
        'Action'          : '/action/<str:card>/<str:game_id>'
    }
    return Response(api_urls)


@api_view(['GET'])
def start_game(request, difficulty, player_ids, data_structures):

    if difficulty not in config.DIFFICULTY_LEVELS:
        return Response({'error': 'Difficulty level not found!',
                         'options': config.DIFFICULTY_LEVELS})

    player_ids = player_ids.split(',')
    data_structures = data_structures.split(',')

    new_board = utils.new_board(difficulty, player_ids, data_structures)

    status = utils.create_board_db(new_board)
    if status['error']:
        return Response({'error': status['reason']})

    return Response({'game_id': status['game_id']})


@api_view(['GET'])
def board(request, game_id):

    status = utils.load_board_db(game_id)
    if status['error']:
        return Response({'error': status['reason']})

    # remove nicks ?? uid
    del status['game_board']['graph']['uid']

    return Response(status['game_board'])


@api_view(['POST'])
def rebalance(request, game_id):
    '''
    Example call:

    import requests
    import json

    url = 'http://127.0.0.1:8000/game_board/api/rebalance/b0fc6e00-0b55-11eb-934e-acde48001122'
    myobj = {'adjacency_list':{'node2':['node0'],'node0':['node5','node3'],'node5':[],'node3':[]}}

    headers = {'content-type': 'application/json'}
    r=requests.post(url, data=json.dumps(myobj), headers=headers)

    print(r.text)
    '''

    adjacency_list = json.loads(request.body)['adjacency_list']

    # Load the game board from database
    status = utils.load_board_db(game_id)
    if status['error']:
        return Response({'error': status['reason']})
    board = status['game_board']

    # Check DS
    if board['curr_data_structure'] != 'AVL':
        return Response({'invalid_action':'Rebalance can be performed for an AVL!'})

    # Check for invalid action
    check = utils.cheat_check(game_board=board, rebalance=True)
    if check['cheat']:
        return Response({'invalid_action': check['reason']})

    # Do the rebalance action with Nick's AVL lib here
    if board['curr_data_structure'] == 'AVL':
        graph = avl.avlRebalance(board['graph'])
    board['graph'] = graph

    # If not correct lose points
    if board['graph']['adjacency_list'] != adjacency_list:
        board['player_points'][board['turn']] -= config.LOSS[str(board['difficulty'])]

    # Change turn
    next_player_index = (board['player_ids'].index(board['turn']) + 1) % len(board['player_ids'])
    board['turn'] = board['player_ids'][next_player_index]

    # Update board
    status = utils.update_board_db(board)
    if status['error']:
        return Response({'error': status['reason']})
    board = status['game_board']

    # remove nicks ?? uid
    del status['game_board']['graph']['uid']

    return Response(board)


@api_view(['GET'])
def action(request, card, game_id):

    # Load the game board from database
    status = utils.load_board_db(game_id)
    if status['error']:
        return Response({'error': status['reason']})
    board = status['game_board']

    # Check for invalid action
    check = utils.cheat_check(game_board=board, card=card)
    if check['cheat']:
        return Response({'invalid_action': check['reason']})

    # Give the points
    if config.GAIN_TIMES[board['curr_data_structure']] in card:
        point = board['graph']['node_points'][card.split()[1]]
        board['player_points'][board['turn']] += point

    # Do the card action with Nick's AVL lib here
    if board['curr_data_structure'] == 'AVL':
        graph = avl.avlAction(card, board['graph'])
    else:
        graph = avl.avlAction(card, board['graph'])

    board['graph'] = graph

    # Remove the played card
    board['cards'][board['turn']].remove(card)
    # Pick a new card
    board['cards'][board['turn']].append(utils.pick_a_card(board))
    # Change turn
    next_player_index = (board['player_ids'].index(board['turn']) + 1) % len(board['player_ids'])
    board['turn'] = board['player_ids'][next_player_index]

    # Update board
    status = utils.update_board_db(board)
    if status['error']:
        return Response({'error': status['reason']})
    board = status['game_board']

    # remove nicks ?? uid
    del status['game_board']['graph']['uid']

    return Response(board)
