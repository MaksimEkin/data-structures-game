from pymongo import MongoClient, DESCENDING
import os

# Gets database & it's authorization from the environment
DATABASE_URL1 = os.environ.get('DATABASE_URL1')
client = MongoClient(DATABASE_URL1)
RECORD_LIMIT = 50

def get_rankings():
    """
    Allows all user profiles to be passed back to the API.
    Passes them back in order from highest to lowest based on the number of points they have
    Refrains from passing data that will not be displayed in rankings

    Parameters:
    None

    Returns:
        cursor: to iterate  all user profile documents
    """
    return client.InitialDB.User_Profile.find({},{'_id':0,'user_id': 1, 'points':1}).limit(RECORD_LIMIT).sort('points', DESCENDING)
