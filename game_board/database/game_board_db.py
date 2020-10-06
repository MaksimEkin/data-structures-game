from pymongo import MongoClient
import os
import random

MAX_GAMES_ACTIVE_AT_ONE_TIME = 100

def create_game(id1: int, id2: int, id3: int, id4: int, gameState: str):
    DATABASE_URL1 = os.environ.get('DATABASE_URL1')
    client = MongoClient(DATABASE_URL1)
    Game_collection = client.InitialDB.Active_Games
    Lobby_collection = client.InitialDB.Lobby

    ready = False
    user_list = [id1, id2, id3, id4]

    while not ready:
        gameid = random.randrange(0, MAX_GAMES_ACTIVE_AT_ONE_TIME)
        returned_data = Game_collection.find_one({"game id": gameid})
        if returned_data is None:
            test_document =  {"game id": gameid, 'users':user_list, 'points': 0, 'game state': gameState, 'player id current turn': id1}

            #Remove the players from the lobby
            for id in user_list:
                Lobby_collection.find_one_and_delete({"user id": id})
                #What happenes when the player is being added to the game but not in the Lobby?

            Game_collection.insert_one(test_document).inserted_id
            return gameid

def update_game(game_id : int, gameState: str):
    DATABASE_URL1 = os.environ.get('DATABASE_URL1')
    client = MongoClient(DATABASE_URL1)
    return client.InitialDB.Active_Games.find_one_and_update({"game id": game_id}, { '$set':{'game state': gameState}})

def read_game(game_id: int):
    DATABASE_URL1 = os.environ.get('DATABASE_URL1')
    client = MongoClient(DATABASE_URL1)
    return client.InitialDB.Active_Games.find_one({"game id": game_id})

def remove_game(game_id: int):
    DATABASE_URL1 = os.environ.get('DATABASE_URL1')
    client = MongoClient(DATABASE_URL1)
    return client.InitialDB.Active_Games.delete_one({"game id": game_id}).acknowledged
