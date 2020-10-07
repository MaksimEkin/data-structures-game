from . import config
from .database import game_board_db as db

from datetime import datetime
from bson import json_util, ObjectId

import random
import uuid
import json

def load_board(game_id):
    '''
    Load a game board state from database.

    :string game_id: id of the game board
    :return: game board dict or error
    '''
    try:
        # game_board = mock_db.read_game('game_id1234')
        game_board = db.read_game(str(game_id))
        if game_board == "nah bro idk about it":
            return True, 'Game Not Found!'

        # Serialize
        game_board = json.loads(json_util.dumps(game_board))

        # Remove the database entry ID
        del game_board['_id']

    except Exception as e:
        return True, str(e)

    return False, game_board


def new_board(difficulty, player_ids, data_structures, online):
    '''
    Create new board dictionary.

    :string difficulty: difficulty of the game
    :list player_ids: list of player ids
    :list data_structures: list of data structures
    :string online: multiplater/online
    :return: game board dict
    '''

    # Call Nick's AVL lib here
    graph =  {'nodes': 'node4(node2(node3)(node1))(node6(node5))',
              'node_points': {'node1': 1, 'node2': 2, 'node3': 3, 'node4': 4, 'node5': 5, 'node6': 6},
              'gold_node': 'node5', 'balanced': True}

    board = {
        'game_id': str(uuid.uuid1()),
        'graph': graph,
        'player_ids': player_ids,
        'player_names': [''],
        'player_points': {str(id):0 for id in player_ids},
        'turn': random.choice(player_ids),
        'cards': distribute_cards(player_ids, list(graph['node_points'].keys()), data_structures[0], difficulty),
        'gold_node': False,
        'difficulty': difficulty,
        'num_players': len(player_ids),
        'online': online,
        'curr_data_structure': data_structures[0],
        'selected_data_structures': data_structures,
        'timed_game': False,
        'seconds_until_next_ds': 60,
        'time_created': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        'end_game': False
    }

    return board


def cheat_check(game_board, card=-1, player_id=-1, rebalance=-1):
    '''
    Check if the action that is attempted is valid.

    :dict game_board:
    :string card:
    :string player_id:
    :bool rebalance:
    :return: True if invalid action, and string for reason.
    '''

    # Check if the game have ended
    if game_board['end_game'] == True:
        return True, str('Game has finished!')

    # Check if the user is in the game
    if player_id != -1 and (player_id not in game_board['player_ids']):
        return True, str('Player ' + str(player_id) + ' is not in the game!')

    # Check if it is the given player's turn
    if game_board['turn'] != player_id:
        return True, str('Player ' + str(player_id) + ' can not play now!')

    # Check if the user has the claimed card
    if card != -1 and (card not in game_board['cards'][str(player_id)]):
        return True, str('Player does not have the card ' + str(card) + '!')

    # Check if the graph is in rebalance state
    if rebalance != -1 and (game_board['graph']['balanced'] == True):
        return True, str('Tree is already balanced!')

    # No cheat detected
    return False, ''


def distribute_cards(player_ids, nodes, data_structure, difficulty):
    '''
    Distribute cards to the users.

    :list player_ids: player IDs
    :list nodes: graph nodes
    :string data_structure: current data structure
    :int cards_per: how many cards per player
    :string difficulty: game difficulty. See config.py
    :return: dict of cards per player
    '''
    board_cards = dict()

    # Minimum and maximum possible node value
    min_point = config.POINTS[str(difficulty)]['min']
    max_point = config.POINTS[str(difficulty)]['max']
    # Card types for the DS
    card_types = config.CARDS[str(data_structure)]

    # generate the deck of cards
    cards = list()
    for ii in range(len(player_ids) * config.CARDS_PER_PLAYER):
        # can not pick node dependent anymore
        if len(nodes) == 0:
            card_types = [action for action in card_types if "node#" not in action]

        # pick a card
        picked_card = random.choice(card_types)

        # node specific action
        if 'node#' in picked_card:
            node_choice = str(random.choice(nodes))
            nodes.remove(node_choice)
            cards.append(picked_card.replace('node#', node_choice))
        # point dependent action
        else:
            cards.append(picked_card.replace('#', str(random.randint(min_point, max_point))))

    # Shuffle the deck of cards
    random.shuffle(cards)

    # pick cards for each player
    for player in player_ids:
        # assign the cards to the player
        player_cards = list()
        for ii in range(config.CARDS_PER_PLAYER):
            player_cards.append(cards.pop())

        board_cards[str(player)] = player_cards

    return board_cards


def pick_a_card(game_board):
    '''
    Pick a new card.

    :dict game_board: game board state
    :return: string card
    '''
    # Minimum and maximum possible node value
    min_point = config.POINTS[str(game_board['difficulty'])]['min']
    max_point = config.POINTS[str(game_board['difficulty'])]['max']
    # Card types for the DS
    card_types = config.CARDS[str(game_board['data_structure'])]

    nodes = list(game_board['graph']['node_points'].keys())
    for key, value in game_board['cards'].items():
        # remove the node based action card from options
        if 'node' in value:
            node = value.split(' ')
            nodes.remove(node[1])

        # no available nodes left for the node based action cards
        if len(nodes) == 0:
            card_types = [action for action in card_types if "node#" not in action]
            break

    # Pick a card
    card = random.choice(card_types)

    # node specific action
    if 'node#' in card:
        card_ = card.replace('node#', str(random.choice(nodes)))
    # point dependent action
    else:
        card_ = card.replace('#', str(random.randint(min_point, max_point)))

    return card_

