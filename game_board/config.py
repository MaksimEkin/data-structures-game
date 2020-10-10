# ========================================================================
# General
# ========================================================================
DIFFICULTY_LEVELS = ['Hard', 'Medium', 'Easy']
CARDS_PER_PLAYER = 3


# ========================================================================
# Available cards (actions) for each data structure.
# ========================================================================
CARDS = {
    'AVL'  : ['Insert #', 'Delete node#'],
    'STACK': ['Pop', 'Push #']
}


# ========================================================================
# Node points for game difficulty.
# ========================================================================
POINTS = {
    DIFFICULTY_LEVELS[0] : {'min':1, 'max':100},
    DIFFICULTY_LEVELS[1] : {'min':1, 'max':50},
    DIFFICULTY_LEVELS[2] : {'min':1, 'max':25}
}


# ========================================================================
# Number of nodes given the difficulty
# ========================================================================
HEIGHT = {
    DIFFICULTY_LEVELS[0] : 6,
    DIFFICULTY_LEVELS[1] : 4,
    DIFFICULTY_LEVELS[2] : 3
}
