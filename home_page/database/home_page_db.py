from pymongo import MongoClient, DESCENDING
import pprint
import os

# Gets database & it's authorization from the environment
DATABASE_URL1 = os.environ.get('DATABASE_URL1')
client = MongoClient(DATABASE_URL1)

def get_rankings():
    """
    Allows all user profiles to be passed back to the API.
    Passes them back in order from highest to lowest based on the numebr of points they have
    Refrains from passing data that will not be displayed in rankings

    Parameters:
    None

    Returns:
        cursor: to iterate  all user profile documents
    """
    return client.InitialDB.User_profile.find({},{'password hash': 0, 'save games': 0, 'badges': 0, 'friends': 0, 'current story level': 0,}).sort('points', DESCENDING)
