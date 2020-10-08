from pymongo import MongoClient
import os

def create_game(board):
    gameid = board["game_id"]
    user_list = board["player_ids"]

    DATABASE_URL1 = os.environ.get('DATABASE_URL1')
    client = MongoClient(DATABASE_URL1)
    Game_collection = client.InitialDB.Active_Games
    Lobby_collection = client.InitialDB.Lobby

    returned_data = Game_collection.find_one({"game_id": gameid})
    if returned_data is None:

        #Remove the players from the lobby
        for id in user_list:
            Lobby_collection.find_one_and_delete({"user_id": id})
            #What happens when the player is being added to the game but not in the Lobby?

        Game_collection.insert_one(board)
        return gameid
    else:
        return 'nah bro idk about it'

def update_game(game_id: str, board):
    DATABASE_URL1 = os.environ.get('DATABASE_URL1')
    client = MongoClient(DATABASE_URL1)
    value_returned = client.InitialDB.Active_Games.find_one_and_replace({"game_id": game_id}, board)
    if value_returned == None:
        return 'nah bro idk about it'
    return value_returned

def read_game(game_id: str):
    DATABASE_URL1 = os.environ.get('DATABASE_URL1')
    client = MongoClient(DATABASE_URL1)

    value_returned = client.InitialDB.Active_Games.find_one({"game_id": game_id})
    if value_returned == None:
        return 'nah bro idk about it'
    return value_returned

def remove_game(game_id: str):
    DATABASE_URL1 = os.environ.get('DATABASE_URL1')
    client = MongoClient(DATABASE_URL1)
    value_returned = client.InitialDB.Active_Games.delete_one({"game_id": game_id}).acknowledged
    if value_returned == False:
        return 'nah bro idk about it'
    return value_returned

'''
# Example Usage
if __name__ == '__main__':
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
            "balanced": true
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
        "gold_node": false,
        "difficulty": "Medium",
        "num_players": 4,
        "online": true,
        "curr_data_structure": "AVL",
        "selected_data_structures": [
            "AVL",
            "Stack"
        ],
        "timed_game": false,
        "seconds_until_next_ds": 60,
        "time_created": "07/10/2020 00:05:47",
        "end_game": false
    }


    create_game(board)
    update_board("60afce36-085a-11eb-b6ab-acde48001122", board)
    read_game("60afce36-085a-11eb-b6ab-acde48001122")
    print(remove_game("60afce36-085a-11eb-b6ab-acde48001122"))

'''
