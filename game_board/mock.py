from datetime import datetime

class MockDB():
    def read_game(game_id):
        board = {
            'id_'                       : 'database_id',
            'game_id'                   : str(game_id),
            'graph'                     : {'nodes': 'node4(node2(node3)(node1))(node6(node5))',
                                          'node_points': {'node1': 1, 'node2': 2, 'node3': 3, 'node4': 4, 'node5': 5, 'node6': 6},
                                          'gold_node': 'node5', 'balanced': True},
            'player_ids'                : ['id2', 'id3', 'id4', 'id5'],
            'player_names'              : ['naomi', 'kulsoom', 'nick', 'ryan'],
            'player_points'             : {'id2': 2, 'id3': 2, 'id4': 3, 'id5': 10},
            'turn'                      : 'id2',
            'cards'                     : {'id2' : ['card1', 'card2', 'card3'], 'id3': ['card1', 'card2', 'card3'],
                                           'id4' : ['card1', 'card2', 'card3'], 'id5': ['card1', 'card2', 'card3']},
            'gold_node'                 : False,
            'difficulty'                : 'Medium',
            'num_players'               : 4,
            'online'                    : True,
            'curr_data_structure'       : 'AVL',
            'selected_data_structures'  : ['AVL', 'Stack'],
            'timed_game'                : False,
            'seconds_until_next_ds'     : 60,
            'time_created'              : datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            'end_game'                  : False
        }
        return board