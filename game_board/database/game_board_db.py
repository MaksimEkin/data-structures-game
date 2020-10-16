from pymongo import MongoClient
import os

# Gets database & it's authorization from the environment
DATABASE_URL1 = os.environ.get('DATABASE_URL1')
client = MongoClient(DATABASE_URL1)

def create_game(board):
    """
    Saves a new game into the database after being passed through the Django API

    Parameters:
    board (dictionary): cornicopia of game information such as current graph, players,
                    turn data, and time data

    Returns:
    On Success:
        str: unique identification for the game
    On Fail:
        str: friendly response to inform of an error
    """
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
    """
    Finds an active game in the Database and updates the values to reflect players'
    in-game decisions

    Parameters:
    game_id (str): unique identification for the game
    board (dictionary): cornicopia of game information such as current graph, players,
                    turn data, and time data
    Returns:
    On Success:
        dictionary: original game document
    On Fail:
        str: friendly response to infrom of an error
    """
    value_returned = client.InitialDB.Active_Games.find_one_and_replace({"game_id": game_id}, board)
    if value_returned == None:
        return 'nah bro idk about it'
    return value_returned

def read_game(game_id: str):
    """
    Allows an active game to be extracted from the database and passed back to the API

    Parameters:
    game_id (str): unique identification for the game

    Returns:
    On Success:
        dictionary: an active game document
    On Fail:
        str: friendly response to inform of an error
    """
    DATABASE_URL1 = os.environ.get('DATABASE_URL1')
    client = MongoClient(DATABASE_URL1)

    value_returned = client.InitialDB.Active_Games.find_one({"game_id": game_id})
    if value_returned == None:
        return 'nah bro idk about it'
    return value_returned

def remove_game(game_id: str):
    """
    Allows an active game to be located and then deleted from the database

    Parameters:
    game_id (str): unique identification for the game

    Returns:
    On Success:
        int: number of deleted game documents
    On Fail:
        str: friendly response to inform of an error
    """
    value_returned = client.InitialDB.Active_Games.delete_one({"game_id": game_id}).acknowledged
    if value_returned == False:
        return 'nah bro idk about it'
    return value_returned

def list_games():
    """
    Allows unique ids of all active games to be passed back to the API

    Parameters:
    None
    
    Returns:
        cursor: to iterate game ids
    """
    return client.InitialDB.Active_Games.find({},{'_id':0, 'game_id': 1})
