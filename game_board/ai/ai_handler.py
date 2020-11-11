""" AI for CMSC 447 DSG, Fall 2020

Min-Max AI for DSG Game
"""
import re
import math
from game_board.avl import avl_handler as avl
from .. import config


class AIHandler():
    """ Implementation of the AI """

    def __init__(self, state, game_type, num_players, max_depth, deck, played_cards):
        self.num_players = num_players
        self.max_depth = max_depth
        self.game_type = game_type
        self.deck = deck
        self.played_cards = played_cards
        self.original_state = self.parse_state(state)
        self.mstate = self.compute_mstate()
        self.best_move = None

    def parse_state(self, state):
        """ Verifies that the state has all expecte keys. """
        if self.game_type == 'AVL':
            expected_keys = ['adjacency_list', 'node_points', 'gold_node',
                             'root_node', 'balanced', 'uid']
            for key in expected_keys:
                if key not in state:
                    raise Exception(f'Expected key in AVL state not found: {key}')
            return state

        else:
            raise Exception(f'Given unsupported game type: {self.game_type}')

    def compute_mstate(self):
        """ create move state that stores possible moves as well as all other state info """
        filter_set = set(self.played_cards)
        available_cards = [x for x in self.deck if x not in filter_set]
        mstate = self.original_state
        mstate['moves'] = available_cards
        return mstate

    def is_player_minimizing(self, player_num):
        """ determine whether the player is minimizing or not """
        return (player_num % self.num_players) != 0

    def evaluate_move(self, card):
        """ calculate the value of a move """
        generic_card = re.sub('\d+', '#', card, 1)  # replace number in card with '#'
        if generic_card not in config.CARDS[self.game_type]:
            raise Exception(f'Given unsupported card \"{card}\" for game type: {self.game_type}')

        move = card.split(' ')
        if move[0] in config.GAIN_TIMES[self.game_type]:
            return int(move[1])
        else:
            return 0

    def minimax(self, mstate, depth, player_num, alpha, beta):
        """ minimax to find best move """
        if self.game_type is not 'AVL':
            raise Exception(f'Given unsupported game type: {self.game_type}')

        if (depth == 0 or
                mstate['gold_node'] == mstate['root_node'] or
                len(mstate['moves'] == 0)):
            return self.evaluate_move(mstate['moves'][0])

        moves = mstate['moves']
        mstate.pop('moves', None)
        is_minimizing = self.is_player_minimizing(player_num)
        if is_minimizing:
            best_val = math.inf
            for move in moves:
                updated_moves = moves.remove(move)
                updated_state = avl.avlAction(move, mstate, balance=True)
                updated_state['moves'] = updated_moves
                val = (self.minimax(updated_state, depth - 1, (player_num + 1) % self.num_players, alpha, beta) -
                       self.evaluate_move(move))
                best_val = min(val, best_val)
                beta = min(beta, best_val)
                if beta <= alpha:
                    break

            return best_val

        else:
            best_val = math.inf
            best_move = None
            for move in moves:
                updated_moves = moves.remove(move)
                updated_state = avl.avlAction(move, mstate, balance=True)
                updated_state['moves'] = updated_moves
                val = (self.minimax(updated_state, depth - 1, (player_num + 1) % self.num_players, alpha, beta) +
                       self.evaluate_move(move))
                if val > best_val:
                    best_move = move
                best_val = max(val, best_val)
                alpha = max(alpha, best_val)
                if beta <= alpha:
                    break

            if depth == self.max_depth:
                self.best_move = best_move
            return best_val

#### AI CALL ####
def ai_move(state, deck, type, num_players, seen_moves = None, max_depth = 5):
    """ call on ai to make a move """
    ai = AIHandler(state, type, num_players, max_depth, deck, seen_moves)
    ai.minimax(ai.mstate, ai.max_depth, ai.num_players, -math.inf, math.inf)
    return ai.best_move