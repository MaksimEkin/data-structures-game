"""
Removes games older than a day from the mongo db from a Rasberry Pi
"""

import os
import datetime as dt
from pymongo import MongoClient

DATABASE_URL1 = os.environ.get('DATABASE_URL1')
print(DATABASE_URL1)
client = MongoClient(DATABASE_URL1)

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
    value_returned = client.InitialDB.Active_Games.delete_one({"game_id": game_id}).deleted_count

    if value_returned == 0:
        return 'nah bro idk about it'

    return value_returned

def purge_old_games():
    """
    Checks the datetime of games, deletes anything older than 1 day

    Parameters:
    None

    Returns:
        int: 0
    """
    yesterday = (dt.datetime.now() - dt.timedelta(days=1))
    mongo_cursor = client.InitialDB.Active_Games.find({},{'_id':0, 'game_id': 1, 'time_created':1})

    print("Purging...")
    for game in mongo_cursor:
        try:
            game_date = game['time_created']
            game_datetime_obj = dt.datetime.strptime(game_date,"%d/%m/%Y %H:%M:%S")
            if game_datetime_obj < yesterday:
                print(game, "Removed")
                remove_game(game['game_id'])

        except:
            with open("purge_exception_log.txt", "a") as file:
                file.write("Could not process " + str( game ) + " in purge\n")
            print("Exception logged - Purge")

    print("Purge Complete")
    return 0

if __name__ == '__main__':
    purge_old_games()
