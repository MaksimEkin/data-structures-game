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
MAX_NUM_PLAYERS = 5     # For avl game
LLIST_MAX_NUM_PLAYERS = 1   # For linnked list game
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
    'AVL': ['Insert #', 'Delete node#'],
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
# Loss-Gain Points for rebalance action
#   LOSS/GAIN : Each key is a difficulty from DIFFICULTY_LEVELS, and
#            its value is the number of points to lose/gain for invalid action
# ========================================================================
LOSS = {
    DIFFICULTY_LEVELS[0] : 40,
    DIFFICULTY_LEVELS[1] : 30,
    DIFFICULTY_LEVELS[2] : 20
}

GAIN = {
    DIFFICULTY_LEVELS[0] : 30,
    DIFFICULTY_LEVELS[1] : 20,
    DIFFICULTY_LEVELS[2] : 10
}


# ========================================================================
# When to gain points for card actions
#   GAIN_TIMES/GAIN_TIMES_POINTS : Each key is a data structure and its value is list of card
#                types that gains points to the player.
# ========================================================================
GAIN_TIMES = {
    'AVL'  : ['Delete', 'Insert'],
    'STACK': ['Pop']
}

GAIN_TIMES_POINTS = {
    'Insert' : 5,
    'Delete' : 5
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



# ========================================================================
# LINKED LIST GAME MODE CONFIGURATIONS FROM HERE ON
# LINKED LIST GAME MODE CONFIGURATIONS FROM HERE ON  
# LINKED LIST GAME MODE CONFIGURATIONS FROM HERE ON                 
# ========================================================================
# ========================================================================
# General: Configuration constants particular to the llist game mode
#   INIT_NUM_FOOD:  Starting number of food for players
#   FOOD_TYPES: The type of food that can be grabbed from a forrage
#
# ========================================================================
INIT_NUM_FOOD = 6
FORAGE_TYPES = ['crumb', 'berry', 'donut', 'attack']

# ========================================================================
# Chances of coming under attack when foraging for each difficulty
#   FORAGE_CHANCE:  Chance of shit happening under a forage
#                   
# ========================================================================
FORAGE_CHANCE = {
    DIFFICULTY_LEVELS[0] : {
        FORAGE_TYPES[0]: .35,
        FORAGE_TYPES[1]: .30,
        FORAGE_TYPES[2]: .15,
        FORAGE_TYPES[3]: .20
    },
    DIFFICULTY_LEVELS[1] : {
        FORAGE_TYPES[0]: .325,
        FORAGE_TYPES[1]: .325,
        FORAGE_TYPES[2]: .20,
        FORAGE_TYPES[3]: .15
    },
    DIFFICULTY_LEVELS[2] : {
        FORAGE_TYPES[0]: .30,
        FORAGE_TYPES[1]: .35,
        FORAGE_TYPES[2]: .25,
        FORAGE_TYPES[3]: .10
    }
}


FOOD_VALUE = {
    FORAGE_TYPES[0]: 1,
    FORAGE_TYPES[1]: 2,
    FORAGE_TYPES[2]: 3,
    FORAGE_TYPES[3]: -1
}




