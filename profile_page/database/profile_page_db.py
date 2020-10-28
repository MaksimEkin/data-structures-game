"""
Allows users to have a profile in the datastucture game, builds in basic authentication features
"""

import os
from pymongo import MongoClient, ReturnDocument

# Gets database & it's authorization from the environment
DATABASE_URL1 = os.environ.get('DATABASE_URL1')
client = MongoClient(DATABASE_URL1)

def save_user(user: dict):
    """
    Saves a new user into the database after being passed through the Django API

    Parameters:
    user (dictionary): user infromation, such as email, creation date, points,
                        badges, saved games, etc

    Returns:
    On Success:
        Boolean: True
    On Fail:
        Boolean: False
    """
    info_used = user_or_email( user["user_id"],  user["email"])

    if info_used:
        return False

    return client.InitialDB.User_Profile.insert_one(user).acknowledged

def update_user(user_id : str, user: dict):
    """
    Finds an active user in the Database and updates the values to reflect player's new data

    Parameters:
    user_id (str): unique identification for the user
    user (dictionary): user infromation, such as email, creation date, points,
                        badges, saved games, etc

    Returns:
    On Success:
        dictionary: original user document
    On Fail:
        Boolean: False
    """
    value_returned = client.InitialDB.User_Profile.find_one_and_replace({"user_id": user_id}, user)

    if value_returned is None:
        return False

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
        Boolean: False
    """

    value_returned = client.InitialDB.User_Profile.find_one({"user_id": user_id})

    if value_returned is None:
        return False

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
        Boolean: False
    """

    value_returned = client.InitialDB.User_Profile.find_one(
        {"user_id": user_id}, {'_id':0, 'user_name':1})

    if value_returned is None:
        return False

    return value_returned

def remove_user(user_id: str):
    """
    Allows an active user to be located and then deleted from the database

    Parameters:
    user_id (str): unique identification for the user

    Returns:
    On Success:
        Boolean: True
    On Fail:
        Boolean: False
    """
    value_returned = client.InitialDB.User_Profile.delete_one({"user_id": user_id}).deleted_count
    return value_returned > 0

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
        Boolean: True
    On Fail:
        Boolean: False
    """

    value_returned = client.InitialDB.User_Profile.find_one_and_update(
        {"user_id": user_id},
        {"$set":{"save_games.$[index]":game_data}},
        upsert=False, return_document = ReturnDocument.AFTER,
        array_filters=[{"index.game_id":{"$eq": user_game_id}}]
    )

    if value_returned == game_data:
        return True

    return False

def list_user_games(user_id : str):
    """
    Finds an active user in the Database and returns their games

    Parameters:
    user_id (str): unique identification for the user

    Returns:
    On Success:
        list: all original user games
    On Fail:
        Boolean: False
    """

    value_returned = client.InitialDB.User_Profile.find_one(
        {"user_id": user_id},
        {'_id':0,"save_games":1}
    )

    if value_returned is None:
        return False

    return value_returned["save_games"]

def user_or_email (user_id : str, email: str = ""):
    """
    Finds an active user in the Database and returns true if email of user id is found

    Parameters:
    user_id (str): unique identification for the user
    email (int): user's saved email address

    Returns:
    On Success:
        Boolean: True
    On Fail:
        Boolean: False
    """

    value_returned = client.InitialDB.User_Profile.find(
        {"$or": [{ "user_id": user_id},{"email": email}]}).count()

    return value_returned > 0

def create_user(user_id : str, passhash : str, email : str, token : str):
    """
    Creates user datapoints given user and API generated data

    Parameters:
    user_id (str): unique identification for the user
    passhash (str): hashed string representing the user's password
    email (int): user's saved email address
    token (str): authentication for API calls

    Returns:
    On Success:
        Boolean: True
    On Fail:
        Boolean: False
    """
    info_used = user_or_email(user_id, email)

    if info_used:
        return False

    user = {"user_id":user_id,
    "password_hash":passhash,
    "email":email,
    "auth_token": token,
    "badges":[],
    "current_story_level":1,
    "friends":[],
    "points":0,
    "rank":"Baby Panda",
    "save_games":[],
    "sharing": True
    }

    return save_user(user)

def login ( user_id : str, passhash : str ):
    """
    Validates a user's password in the database

    Parameters:
    user_id (str): unique identification for the user
    passhash (str): hashed string representing the user's password

    Returns:
    On Success:
        Boolean: True
    On Fail:
        Boolean: False
    """

    value_returned = client.InitialDB.User_Profile.find(
        {"$and": [{ "user_id": user_id}, {"password_hash": passhash}]}).count()

    return value_returned > 0

def update_token( user_id : str, token : str ):
    """
    Updates a user's API token in the database

    Parameters:
    user_id (str): unique identification for the user
    token (str): authentication for API calls

    Returns:
    On Success:
        Boolean: True
    On Fail:
        Boolean: False
    """
    value_returned = client.InitialDB.User_Profile.update_one(
        {"user_id": user_id},
        {"$set":{"auth_token":token}},
        upsert=False
    ).modified_count

    return value_returned > 0

def check_user( user_id : str, token : str ):
    """
    Validates a user's API token in the database

    Parameters:
    user_id (str): unique identification for the user
    token (str): authentication for API calls

    Returns:
    On Success:
        Boolean: True
    On Fail:
        Boolean: False
    """
    value_returned = client.InitialDB.User_Profile.find(
        {"$and": [{ "user_id": user_id}, {"auth_token": token}]}).count()

    return value_returned > 0

def remove_token ( user_id : str ):
    """
    Deletes a user's API token in the database

    Parameters:
    user_id (str): unique identification for the user

    Returns:
    On Success:
        Boolean: True
    On Fail:
        Boolean: False
    """
    value_returned = client.InitialDB.User_Profile.update_one(
        {"user_id": user_id},
        {"$unset":{"auth_token": ""}},
        upsert=False
    ).modified_count

    return value_returned > 0

def check_user_share_setting( user_id : str ):
    """
    Checks if the user is allowing sharing

    Parameters:
    user_id (str): unique identification for the user

    Returns:
    On Success:
        Boolean: True
    On Fail:
        Boolean: False
    """
    value_returned = client.InitialDB.User_Profile.find(
        {"$and": [{ "user_id": user_id}, {"sharing": True}]}).count()

    return value_returned > 0

def load_board(user_id : str, user_game_id: str):
    """
    Finds an active user in the Database and returns a specific game to the API

    Parameters:
    user_id (str): unique identification for the user
    game_index (int): locates which save game to overwrite

    Returns:
    On Success:
        dictionary: original user game
    On Fail:
        Boolean: False
    """

    value_returned = client.InitialDB.User_Profile.find_one(
        {"user_id": user_id},
        {'_id':0,"save_games":{"$elemMatch":{"game_id":user_game_id}}}
    )

    if value_returned is None:
        return False

    try:
        value_returned = value_returned['save_games'][0]
        return value_returned
    return False

def save_game( user_id : str, board : dict ):
    """
    Finds an active user in the Database and appends a specific game to saves

    Parameters:
    user_id (str): unique identification for the user
    game_data (dictionary): game board dictionary

    Returns:
    On Success:
        Boolean: True
    On Fail:
        Boolean: False
    """

     # Returns a cursor -- only reason for loop (expecting {'save_games': 1} if game exists)
    for item in client.InitialDB.User_Profile.aggregate([
        {"$match":{"user_id": user_id}},
        {"$unwind":"$save_games"},
        {"$match":{"save_games.game_id": board["game_id"]}},
        {"$count":"save_games"}
    ]):
        if item['save_games'] > 0:
            return False

    # Pushes the game to user's save game list
    value_returned = client.InitialDB.User_Profile.update_one(
        {"user_id": user_id},
        {"$push":{"save_games":board}},
        upsert = False,
    ).modified_count

    return value_returned > 0

def delete_game(user_id : str, user_game_id: str):
    """
    Finds an active user in the Database and deletes a specific game

    Parameters:
    user_id (str): unique identification for the user
    game_id (dictionary): unique game identifier

    Returns:
    On Success:
        Boolean: True
    On Fail:
        Boolean: False
    """

    value_returned = client.InitialDB.User_Profile.update_one(
        {"user_id": user_id},
        {"$pull":{"save_games":{"game_id":user_game_id}}},
        upsert = False,
    ).modified_count
    return value_returned > 0

def share_game_board(source_id : str, destination_id : str, user_game_id: str):
    """
    Finds an active user's game graph to share and gives to the API

    Parameters:
    user_id (str): unique identification for the user
    game_index (int): locates which save game to overwrite

    Returns:
    On Success:
        dictionary: original user game
    On Fail:
        Boolean: False
    """

    user1_valid = user_or_email ( source_id )
    user1_shares = check_user_share_setting( destination_id )
    user2_valid = user_or_email ( destination_id )
    game_valid = load_board ( source_id, user_game_id )

    if user1_valid and user1_shares and user2_valid and game_valid:
        return save_game ( destination_id, game_valid )
        
    return False

def change_password( user_id : str, passhash : str ):
    """
    Allows a user to update their password

    Parameters:
    user_id (str): unique identification for the user
    passhash (str): hashed string representing the user's password

    Returns:
    On Success:
        Boolean: True
    On Fail:
        Boolean: False
    """
    value_returned = client.InitialDB.User_Profile.update_one(
        {"user_id": user_id},
        {"$set":{"password_hash":passhash}},
        upsert=False
    ).modified_count

    return value_returned > 0

def change_share_setting( user_id : str, can_share : bool ):
    """
    Allows a user to update their share setting

    Parameters:
    user_id (str): unique identification for the user
    can_share (bool): new boolean to set for user sharing

    Returns:
    On Success:
        Boolean: True
    On Fail:
        Boolean: False
    """
    value_returned = client.InitialDB.User_Profile.update_one(
        {"user_id": user_id},
        {"$set":{"sharing":can_share}},
        upsert=False
    ).modified_count

    return value_returned > 0
