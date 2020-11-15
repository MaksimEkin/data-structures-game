"""
    This document defines the game settings.
"""

# ========================================================================
# General
#   DIFFICULTY_LEVELS: Game difficulty. Establishes the number of nodes in
#                      the game or the height of the tree. See HEIGHT.
#   CARD_IN_DECK:      How many cards are stored in the game deck
#                      Number of action choices each player have.
#   MAX_NUM_PLAYERS:   Maximum number of players in the game.
#   BOT_NAME_PREFIX:   Players with this prefix can access the AI api call
#   BOT_SLEEP_TIME:    Duration in seconds that an AI API call will sleep
#                      to simulate time spent thinking
# ========================================================================
DIFFICULTY_LEVELS = ['Hard', 'Medium', 'Easy']
CARDS_PER_PLAYER = 3
MAX_NUM_PLAYERS = 5
BOT_NAME_PREFIX = "bot"
BOT_SLEEP_TIME = 2

# ========================================================================
# Size of the deck of cards for each difficulty level
#   CARDS_IN_DECK : Each key is a difficulty from DIFFICULTY_LEVELS, and
#                   its value is the number of cards to be put in the deck
#                   for a game of the difficulty
# ========================================================================
CARDS_IN_DECK = {
    DIFFICULTY_LEVELS[0] : 54,
    DIFFICULTY_LEVELS[1] : 36,
    DIFFICULTY_LEVELS[2] : 22
}

# ========================================================================
# Available cards (actions) for each data structure.
#   CARDS : Each key is a data structure, and its value is a
#           list of actions (cards).
#
#           Keywords:
#           <#> is point specific action, replaced with intiger
#           <node#> node specific action
# ========================================================================
CARDS = {
    'AVL'  : ['Insert #', 'Delete node#'],
    'STACK': ['Pop', 'Push #']
}


# ========================================================================
# Node points for game difficulty.
#   POINTS : Each key is a difficulty from DIFFICULTY_LEVELS, and
#            its value is a dictionary look-up for minimum and
#            maximum points.
# ========================================================================
POINTS = {
    DIFFICULTY_LEVELS[0] : {'min':1, 'max':100},
    DIFFICULTY_LEVELS[1] : {'min':1, 'max':50},
    DIFFICULTY_LEVELS[2] : {'min':1, 'max':25}
}


# ========================================================================
# Number of nodes given the difficulty
#   HEIGHT : Each key is a difficulty from DIFFICULTY_LEVELS, and
#            its value is the height of the tree.
# ========================================================================
HEIGHT = {
    DIFFICULTY_LEVELS[0] : 6,
    DIFFICULTY_LEVELS[1] : 5,
    DIFFICULTY_LEVELS[2] : 4
}


# ========================================================================
# Loss Points
#   LOSS : Each key is a difficulty from DIFFICULTY_LEVELS, and
#            its value is the number of points to lose for invalid action
# ========================================================================
LOSS = {
    DIFFICULTY_LEVELS[0] : 25,
    DIFFICULTY_LEVELS[1] : 10,
    DIFFICULTY_LEVELS[2] : 5
}


# ========================================================================
# When to gain points
#   GAIN_TIMES : Each key is a data structure and its value is list of card
#                types that gains points to the player.
# ========================================================================
GAIN_TIMES  = {
    'AVL'  : ['Delete'],
    'STACK': ['Pop']
}

# ========================================================================
# Chances of correctly rebalancing (in %) for each difficultu
#   REBAL_CHANCE : The number of times out of 100 an AI of difficulty level
#                  will be able to correctly rebalance itself
# ========================================================================
REBAL_CHANCE = {
    DIFFICULTY_LEVELS[0] : 80,
    DIFFICULTY_LEVELS[1] : 65,
    DIFFICULTY_LEVELS[2] : 50
}