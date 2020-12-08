"""
Allows the homepage to retrive information from the highest ranked players to display
"""

import os
from pymongo import MongoClient, DESCENDING

# Gets database & it's authorization from the environment
DATABASE_URL1 = os.environ.get('DATABASE_URL1')
client = MongoClient(DATABASE_URL1)

def get_rankings(record_limit = 50):
    """
    Allows all user profiles to be passed back to the API.
    Passes them back in order from highest to lowest based on the number of points they have
    Refrains from passing data that will not be displayed in rankings

    Parameters: None
    Returns: cursor: to iterate  all user profile documents
    """
    return client.InitialDB.User_Profile.find(
    {},{'_id':0,'user_id': 1, 'points':1}
    ).limit(record_limit).sort('points', DESCENDING)
