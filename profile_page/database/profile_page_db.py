from pymongo import MongoClient, ReturnDocument
import os

# Gets database & it's authorization from the environment
DATABASE_URL1 = os.environ.get('DATABASE_URL1')
client = MongoClient(DATABASE_URL1)

def create_user(user: dict):
    """
    Saves a new user into the database after being passed through the Django API

    Parameters:
    user (dictionary): user infromation, such as email, creation date, points, badges, saved games, etc

    Returns:
    On Success:
        str: unique identification for the user
    On Fail:
        str: friendly response to inform of an error
    """
    user_id = user["user_id"]

    User_Profile_collection = client.InitialDB.User_Profile
    #User_Saves_collection = client.InitialDB.User_Game_Saves

    returned_data = User_Profile_collection.find_one({"user_id": user_id})
    if returned_data is None:
        User_Profile_collection.insert_one(user)

        #save_allocations = {"user_id":user_id, "save_games":["game_one":{}, "game_two":{}, "game_three":{}]}
        #User_Saves_collection.insert_one(save_allocations)
        return user_id
    else:
        return 'nah bro idk about it'

def update_user(user_id : str, user: dict):
    """
    Finds an active user in the Database and updates the values to reflect player's new data

    Parameters:
    user_id (str): unique identification for the user
    user (dictionary): user infromation, such as email, creation date, points, badges, saved games, etc

    Returns:
    On Success:
        dictionary: original user document
    On Fail:
        str: friendly response to infrom of an error
    """
    value_returned = client.InitialDB.User_Profile.find_one_and_replace({"user_id": user_id}, user)
    if value_returned == None:
        return 'nah bro idk about it'
    return value_returned

def read_one_user(user_id: str):
    """
    Allows an active user to be extracted from the database and passed back to the API

    Parameters:
    user_id (str): unique identification for the user

    Returns:
    On Success:
        dictionary: an active user document
    On Fail:
        str: friendly response to inform of an error
    """

    value_returned = client.InitialDB.User_Profile.find_one({"user_id": user_id})
    if value_returned == None:
        return 'nah bro idk about it'
    return value_returned

def read_user_name(user_id: str):
    """
    Allows an active user's name to be extracted from the database and passed back to the API

    Parameters:
    user_id (str): unique identification for the user

    Returns:
    On Success:
        str: user's name
    On Fail:
        str: friendly response to inform of an error
    """

    value_returned = client.InitialDB.User_Profile.find_one({"user_id": user_id}, {'_id':0, 'user_name':1})
    if value_returned == None:
        return 'nah bro idk about it'
    return value_returned

def remove_user(user_id: str):
    """
    Allows an active user to be located and then deleted from the database

    Parameters:
    user_id (str): unique identification for the user

    Returns:
    On Success:
        int: number of deleted user documents
    On Fail:
        str: friendly response to inform of an error
    """
    value_returned = client.InitialDB.User_Profile.delete_one({"user_id": user_id}).deleted_count
    if value_returned == 0:
        return 'nah bro idk about it'
    return value_returned

def list_users():
    """
    Allows unique ids of all active users to be passed back to the API

    Parameters:
    None

    Returns:
        cursor: to iterate user ids and names
    """
    return client.InitialDB.User_Profile.find({},{'_id':0, 'user_id': 1 , 'user_name':1})

def update_user_game(user_id : str, user_game_id: str, game_data: dict):
    """
    Finds an active user in the Database and updates a specific game

    Parameters:
    user_id (str): unique identification for the user
    game_index (int): locates which save game to overwrite
    game_data (dictionary): game board dictionary

    Returns:
    On Success:
        dictionary: original user game
    On Fail:
        str: friendly response to infrom of an error
    """


    value_returned = client.InitialDB.User_Profile.find_one_and_update(
        {"user_id": user_id},
        {"$set":{"save_games.$[index]":game_data}},
        upsert=False, return_document = ReturnDocument.AFTER,
        array_filters=[{"index.game_id":{"$eq": user_game_id}}]
    )
    
    if value_returned == None:
        return 'nah bro idk about it'
    return value_returned

def find_user_game(user_id : str, user_game_id: str):
    """
    Finds an active user in the Database and returns a specific game to the API

    Parameters:
    user_id (str): unique identification for the user
    game_index (int): locates which save game to overwrite

    Returns:
    On Success:
        dictionary: original user game
    On Fail:
        str: friendly response to infrom of an error
    """

    value_returned = client.InitialDB.User_Profile.find_one(
        {"user_id": user_id},
        {'_id':0,"save_games":1}
    )

    if value_returned == None:
        return 'nah bro idk about it'

    """
    Find the correct game from its idea
    -- Pymongo cannot further reduce the db response using an array filter,
    so an iteration of user saves is required to find the correct game
    """
    for game in value_returned["save_games"]:
        if game["game_id"] == user_game_id:
            return game

    # Found the user, but none of the games match the game_id
    return 'nah bro idk about it'

def list_user_games(user_id : str):
    """
    Finds an active user in the Database and updates a specific game

    Parameters:
    user_id (str): unique identification for the user

    Returns:
    On Success:
        list: all original user games
    On Fail:
        str: friendly response to infrom of an error
    """

    value_returned = client.InitialDB.User_Profile.find_one(
        {"user_id": user_id},
        {'_id':0,"save_games":1}
    )

    if value_returned == None:
        return 'nah bro idk about it'
    else:
        return value_returned["save_games"]

def update_user_game_graph(user_id : str, user_game_id: str, graph_data: dict):
    """
    Finds an active user in the Database and updates a specific game's graph

    Parameters:
    user_id (str): unique identification for the user
    game_index (int): locates which save game to overwrite
    graph_data (dictionary): game board graph dictionary

    Returns:
    On Success:
        dictionary: original user game
    On Fail:
        str: friendly response to infrom of an error
    """
    value_returned = client.InitialDB.User_Profile.find_one_and_update(
        {"user_id": user_id},
        {"$set":{"save_games.$[index].graph":graph_data}},
        upsert=False, return_document = ReturnDocument.AFTER,
        array_filters=[{"index.game_id":{"$eq": user_game_id}}]
    )

    if value_returned == None:
        return 'nah bro idk about it'
    return value_returned

def find_user_game_graph(user_id : str, user_game_id: str):
    """
    Finds an active user in the Database and returns a specific game to the API

    Parameters:
    user_id (str): unique identification for the user
    game_index (int): locates which save game to overwrite

    Returns:
    On Success:
        dictionary: original user game
    On Fail:
        str: friendly response to infrom of an error
    """

    value_returned = client.InitialDB.User_Profile.find_one(
        {"user_id": user_id},
        {'_id':0,"save_games":1}
    )

    if value_returned == None:
        return 'nah bro idk about it'

    """
    Find the correct game from its idea
    -- Pymongo cannot further reduce the db response using an array filter,
    so an iteration of user saves is required to find the correct game graph
    """
    for game in value_returned["save_games"]:
        if game["game_id"] == user_game_id:
            return game["graph"]

    # Found the user, but none of the games match the game_id
    return 'nah bro idk about it'

def delete_user_game_graph(user_id : str, user_game_id: str):
    """
    Finds an active user in the Database and deletes a specific game's graph

    Parameters:
    user_id (str): unique identification for the user
    game_index (int): locates which save game to overwrite

    Returns:
    On Success:
        dictionary: original user game
    On Fail:
        str: friendly response to infrom of an error
    """
    value_returned = client.InitialDB.User_Profile.find_one_and_update(
        {"user_id": user_id},
        {"$set":{"save_games.$[index].graph":{}}},
        upsert=False,
        array_filters=[{"index.game_id":{"$eq": user_game_id}}]
    )

    if value_returned == None:
        return 'nah bro idk about it'
    return 1

def delete_user_game(user_id : str, user_game_id: str):
    """
    Finds an active user in the Database and deletes a specific game

    Parameters:
    user_id (str): unique identification for the user
    game_index (int): locates which save game to overwrite
    game_data (dictionary): game board dictionary

    Returns:
    On Success:
        dictionary: original user game
    On Fail:
        str: friendly response to infrom of an error
    """

    value_returned = client.InitialDB.User_Profile.find_one_and_update(
        {"user_id": user_id},
        {"$set":{"save_games.$[index]":{}}},
        upsert=False,
        array_filters=[{"index.game_id":{"$eq": user_game_id}}]
    )

    if value_returned == None:
        return 'nah bro idk about it'
    return 1

def share_user_game(user_id : str, user_game_id: str):
    """
    Finds an active user's game graph to share and gives to the API

    Parameters:
    user_id (str): unique identification for the user
    game_index (int): locates which save game to overwrite

    Returns:
    On Success:
        dictionary: original user game
    On Fail:
        str: friendly response to infrom of an error
    """
    return find_user_game(user_id, user_game_id)

def share_user_graph(user_id : str, user_game_id: str):
    """
    Finds an active user's game graph to share and gives to the API

    Parameters:
    user_id (str): unique identification for the user
    game_index (int): locates which save game to overwrite

    Returns:
    On Success:
        dictionary: original user game
    On Fail:
        str: friendly response to infrom of an error
    """
    return find_user_game_graph(user_id, user_game_id)
