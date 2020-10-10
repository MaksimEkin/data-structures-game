# ========================================================================
# General game rules that is not DS specific
# ========================================================================
def general(game_board, card=-1):

    # Check if the user has the claimed card
    if card != -1 and (card not in game_board['cards'][game_board['turn']]):
        return {'cheat': True, 'reason': str('Player does not have the card ' + str(card) + '!')}

    # No cheat detected
    return {'cheat': False}


# ========================================================================
# Addional game rules when the DS is AVL
# ========================================================================
def AVL(game_board, rebalance=-1):

    # Check if the graph is in rebalance state
    if rebalance != -1 and (game_board['graph']['balanced'] == True):
        return {'cheat': True, 'reason': str('Tree is already balanced!')}

    # Check if user is attempting to do an action while tree is not balanced
    if rebalance == -1 and (game_board['graph']['balanced'] == False):
        return {'cheat': True, 'reason': str('You must balance the tree first!')}

    # No cheat detected
    return {cheat': False}