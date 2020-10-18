from user_profile_db import *

# Example Usage
if __name__ == '__main__':

    #Create Data
    board = {
        "game_id": "id12dawda8",
        "graph": {
            "nodes": "node4(node2(node3)(node1))(node6(node5))",
            "node_points": {
                "node1": 1,
                "node2": 2,
                "node3": 3,
                "node4": 4,
                "node5": 5,
                "node6": 6
            },
            "gold_node": "node5",
            "balanced": True
        },
        "player_ids": [
            "id2",
            "id3",
            "id4",
            "id5"
        ],
        "player_names": [
            "naomi",
            "kulsoom",
            "nick",
            "ryan"
        ],
        "player_points": {
            "id2": 2,
            "id3": 2,
            "id4": 3,
            "id5": 10
        },
        "turn": "id2",
        "cards": {
            "id2": [
                "card1",
                "card2",
                "card3"
            ],
            "id3": [
                "card1",
                "card2",
                "card3"
            ],
            "id4": [
                "card1",
                "card2",
                "card3"
            ],
            "id5": [
                "card1",
                "card2",
                "card3"
            ]
        },
        "gold_node": False,
        "difficulty": "Medium",
        "num_players": 4,
        "online": True,
        "curr_data_structure": "AVL",
        "selected_data_structures": [
            "AVL",
            "Stack"
        ],
        "timed_game": False,
        "seconds_until_next_ds": 60,
        "time_created": "07/10/2020 00:05:47",
        "end_game": False
    }

    # CREATE A GAME
    create_game(board)

    # UPDATE A GAME
    print(update_game("60afce36-085a-11eb-b6ab-acde48001122", board))

    # READ A GAME
    read_game("60afce36-085a-11eb-b6ab-acde48001122")

    # DELETE A GAME
    print(remove_game("60afce36-085a-11eb-b6ab-acde48001122"))

    # LIST ALL GAMES IDS
    for game in list_games():
        print(game['game_id'])
