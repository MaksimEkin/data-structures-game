from pymongo import MongoClient
import os

DATABASE_URL1 = os.environ.get('DATABASE_URL1')
client = MongoClient(DATABASE_URL1)

def create_game(board):
    gameid = board["game_id"]
    user_list = board["player_ids"]

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

    value_returned = client.InitialDB.Active_Games.delete_one({"game_id": game_id}).acknowledged
    if value_returned == False:
        return 'nah bro idk about it'
    return value_returned

def list_games():
    return client.InitialDB.Active_Games.find({},{'_id':0, 'game_id': 1})
