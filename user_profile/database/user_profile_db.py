from pymongo import MongoClient
import os

# Gets database & it's authorization from the environment
DATABASE_URL1 = os.environ.get('DATABASE_URL1')
client = MongoClient(DATABASE_URL1)

def create_user(user):
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

    returned_data = User_Profile_collection.find_one({"user_id": user_id})
    if returned_data is None:
        User_Profile_collection.insert_one(user)
        return user_id
    else:
        return 'nah bro idk about it'

def update_user(user_id : str, user):
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
