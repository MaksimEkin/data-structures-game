from . import config
import random

def generate_cards(player_ids, nodes, data_structure, cards_per, difficulty):
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

    # Pick cards for each player
    for player in player_ids:
        # cards (actions) for the current player
        cards = random.choices(config.CARDS[str(data_structure)], k=int(cards_per))
        cards_= list()

        for card in cards:
            # node specific action
            if 'node#' in card:
                cards_.append(card.replace('node#', str(random.choice(nodes))))
            # point dependent action
            else:
                cards_.append(card.replace('#', str(random.randint(min_point, max_point))))
        # assign the cards to the player
        board_cards[str(player)] = cards_

    return board_cards

def new_card(data_structure, nodes, difficulty):
    '''
    Pick a new card.

    :string data_structure: current data structure
    :list nodes: nodes in the graph
    :string difficulty: game difficulty. See config.py
    :return: string card
    '''
    # Minimum and maximum possible node value
    min_point = config.POINTS[str(difficulty)]['min']
    max_point = config.POINTS[str(difficulty)]['max']

    # Pick a card
    card = random.choice(config.CARDS[str(data_structure)])

    # node specific action
    if 'node#' in card:
        card_ = card.replace('node#', str(random.choice(nodes)))
    # point dependent action
    else:
        card_ = card.replace('#', str(random.randint(min_point, max_point)))

    return card_

