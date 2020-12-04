"""
Sets all user rankings from a Raspberry Pi
command to run: python get_and_set_rankings.py
"""
import os
from pymongo import MongoClient, DESCENDING, ReturnDocument

DATABASE_URL1 = os.environ.get('DATABASE_URL1')
client = MongoClient(DATABASE_URL1)

def set_ranking(user_id: str, new_rank: int):
    """
    Allows an active user's rank to be updated in the database

    Parameters:
    user_id (str): unique identification for the user
    new_rank (int): New rank relative to other players

    Returns:
    On Success:
        Boolean: True
    On Fail:
        Boolean: False
    """

    value_returned = client.InitialDB.User_Profile.find_one_and_update(
        {"user_id": user_id},
        {"$set":{"rank":new_rank}},
        {'_id':0, 'rank':1},
        upsert=False, return_document = ReturnDocument.AFTER
    )

    if value_returned["rank"] == new_rank:
        return True

    return False


def get_rankings():
    """
    Allows all user profiles to be passed back to the API.
    Passes them back in order from highest to lowest based on the number of points they have
    Refrains from passing data that will not be displayed in rankings

    Parameters: None
    Returns: cursor: to iterate  all user profile documents
    """
    return client.InitialDB.User_Profile.find(
    {},{'_id':0,'user_id': 1, 'points':1}
    ).sort('points', DESCENDING)


if __name__ == '__main__':
    rank_cursor = get_rankings()
    rank_iterator = 1

    for user_rank in get_rankings():
        try:
            set_ranking(user_rank["user_id"], rank_iterator)
            rank_iterator +=1
        except:
            with open("rank_exception_log.txt", "a") as file:
                file.write("Could not process " + str( user_rank ) + " in rankings\n")
            print("Exception logged - Ranking")
