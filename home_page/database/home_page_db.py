from pymongo import MongoClient, DESCENDING
import pprint
import os

DATABASE_URL1 = os.environ.get('DATABASE_URL1')
client = MongoClient(DATABASE_URL1)
    
def get_rankings():
    return client.InitialDB.User_profile.find({},{'password hash': 0, 'save games': 0, 'badges': 0, 'friends': 0, 'current story level': 0,}).sort('points', DESCENDING)
