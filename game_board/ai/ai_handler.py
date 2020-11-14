""" AI for CMSC 447 DSG, Fall 2020

Min-Max AI for DSG Game
"""
import re
import math
from game_board.avl import avl_handler as avl
from .. import config


class AIHandler():
    """ Implementation of the AI """
    def __init__(self, state, game_type, cards, deck, max_depth):
        """
        :param state:       the original state of the game on which the AI is called
        :param game_type:   type of data structure game being played. As of 11/13/20
                            only 'AVL' is being supported
        :param cards:       formatted dictionary of hands. cards[0] is assumed to be
                            the original hand of the maximizing player
        :param deck:        deck of cards not yet claimed by any player
        :param max_depth:   maximum recursive depth on the minimax call
        """
        self.game_type = game_type
        self.original_state = self.parse_state(state)
        self.cards = cards
        self.deck = deck
        self.max_depth = max_depth
        self.num_players = len(cards)
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

    def next_player(self, player):
        """ finds the next ordered player """
        return (player + 1) % self.num_players

    def evaluate_move(self, card):
        """ calculate the value of a move
        The evaluation function that ultimately controls the decision making of the AI
        Currently the goal is just to maximize point value

        :param card:    a possible move
        :return score:  the value of the move
        """
        generic_card = re.sub('\d+', '#', card, 1)  # replace number in card with '#'
        if generic_card not in config.CARDS[self.game_type]:
            raise Exception(f'Given unsupported card \"{card}\" for game type: {self.game_type}')

        move = card.split(' ')
        if move[0] in config.GAIN_TIMES[self.game_type]:
            return int(move[1])
        else:
            return 0

    def find_possible_moves(self, player, seen=None):
        """ find the list of possible moves for the next player that will be going.

        :param player: player for which we will be finding possible moves
        :param seen:   cards that have already been played

        :return moves: list of possible moves for the to take
        """
        if seen is None:
            seen = []

        original_hand = self.cards[player]
        if not bool(set(original_hand) & set(seen)):  # could be a bug here when deck contains a card that is present in the deck
            return original_hand

        deck = self.deck
        all_options = [*original_hand, *deck]  # concat the two lists

        filter_set = set(seen)
        moves = [c for c in all_options if c not in filter_set]
        return moves

    def minimax(self, state, player, moves, depth, alpha, beta, seen=None):
        """ minimax to find best move

        :param state:   current state of the game
        :param player:  player number. must be on [0, self.num_players - 1]
        :param moves:   list of possible moves the player can make this turn
        :param depth:   current recursive depth
        :param alpha:   saved alpha value for alpha-beta pruning
        :param beta:    saved beta value for alpha-beta pruning
        :param seen:    list of already played cards
        """
        print("WE IN MINIMAX")
        if seen is None:
            seen = []

        if self.game_type != 'AVL':
            raise Exception(f'Given unsupported game type: {self.game_type}')

        if (depth == 0 or
                state['gold_node'] == state['root_node'] or
                len(moves) == 0):
            return 0

        if player == 0:
            best_val = -math.inf
            best_move = None
            for move in moves:
                seen.append(move)
                updated_state = avl.avlAction(move, state, balance=True)
                next_player = self.next_player(player)
                updated_moves = self.find_possible_moves(next_player, seen)
                val = (self.minimax(updated_state, next_player, updated_moves, depth-1, alpha, beta, seen) +
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

        else:
            best_val = math.inf
            for move in moves:
                seen.append(move)
                updated_state = avl.avlAction(move, state, balance=True)
                next_player = self.next_player(player)
                updated_moves = self.find_possible_moves(next_player, seen)
                val = (self.minimax(updated_state, next_player, updated_moves, depth - 1, alpha, beta, seen) -
                       self.evaluate_move(move))
                best_val = min(val, best_val)
                beta = min(beta, best_val)
                if beta <= alpha:
                    break

            return best_val


""" AI API CALL(S) """
def select_move(game_state, game_type, cards, deck, max_depth=5):
    """ call on ai to make a move

    :param game_state: game board state as it currently stands
    :param game_type: the type of game being played. currently only AVL supported
    :param maximizer: player id for which AI will maximize points on this call
    :param cards: dictionary of lists where each list contains the cards available to the player
                  this dictionary needs to have been processed by the ai_format_hands function
    :param deck: deck of available cards to draw from
    :return card: game-specific action that the AI found works best
    """
    ai = AIHandler(game_state, game_type, cards, deck, max_depth)
    print('HANDLER INITIALIZED')
    ai.minimax(ai.original_state, 0, ai.cards[0], ai.max_depth, -math.inf, math.inf)
    return ai.best_move
