from rest_framework.decorators import api_view
from rest_framework.response import Response

from game_board.api import utils
from .. import config

import json
from bson import json_util


@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'Start Game'      : '/start_game/<str:difficulty>/<str:player_ids>/<str:data_structures>',
        'Game Board'      : '/board/<str:id>',
        'Re-balance Tree' : '/rebalance/<str:graph>/<str:game_id>',
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

    return Response(board)


@api_view(['GET'])
def rebalance(request, graph, game_id):

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
    # correct_graph = avl.rebalance(graph)
    # correct_graph['nodes'] == graph
    graph =  {'nodes': 'node4(node2(node3)(node1))(node6(node5))',
              'node_points': {'node1': 1, 'node2': 2, 'node3': 3, 'node4': 4, 'node5': 5, 'node6': 6},
              'gold_node': 'node5',
              'root_node': 'node3',
              'balanced': True}
    board['graph'] = graph

    # Update board
    status = utils.update_board_db(board)
    if status['error']:
        return Response({'error': status['reason']})
    board = status['game_board']

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

    # Do the card action with Nick's AVL lib here
    # if board['curr_datastructure'] == 'AVL'
    #   new_graph = avl.action('Delete node2', old_graph)

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

    # Update board
    status = utils.update_board_db(board)
    if status['error']:
        return Response({'error': status['reason']})
    board = status['game_board']

    return Response(board)
