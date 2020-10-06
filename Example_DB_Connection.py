from pymongo import MongoClient
import pprint
import os
import random

PROFILE_DOCUMENT_TEMPLATE = {'name': '', 'id' : 0, 'email': '','password hash': '','save games':['','','',], 'points': 0,'rank': '','badges': [], 'friends':	[], 'current story level': 1 }
ACTIVE_GAMES_DOCUMENT_TEMPLATE = {"game id":'', 'users':['user 1 id', 'user 2 id', 'user 3 id', 'user 4 id'], 'points': 0, 'game state':'', 'player id current turn': 'user 1 id'}
LOBBY_DOCUMENT_TEMPLATE = {'user id':'', 'user name': ''}
#HOMEPAGE_DOCUMENT_TEMPLATE = {'ranking':['player':['name':'','points':0, 'league':''],]}

DATABASE_URL1 = os.environ.get('DATABASE_URL1')

def test_create(db_collection, this_name, this_email, pass_hash ='hf992384h'):
    #test_document = {"tester": "Ryan", "information": "My first DB test!", "list_test": ["Pandamic", "CMSC 447", "pymongo"]}


    returned_data = db_collection.find_one({"email": this_email})
    if returned_data is None:
        #test_document = {'name': this_name, 'id' : 700, 'email': this_email','password hash': pass_hash,'save games':['4(2(3)(1))(6(5))','4(2(3)(1))(6(5))','4(2(3)(1))(6(5))'], 'points': 900,'rank': 'silver','badges': [3,4,8], 'friends':	['Kulsoom','Nick','Maksim','Naomi',], 'current story level': 7 }
        test_document = {'name': "ryan", 'id' : 700, 'email': "ryanb4@umbc.edu",'password hash': 'hf992384h','save games':['4(2(3)(1))(6(5))','4(2(3)(1))(6(5))','4(2(3)(1))(6(5))'], 'points': 900,'rank': 'silver','badges': [3,4,8], 'friends':	['Kulsoom','Nick','Maksim','Naomi',], 'current story level': 7 }

        test_document_id = db_collection.insert_one(test_document).inserted_id
        print("test_document_id =",test_document_id)

    else:
        print(this_name, "with", this_email, "already exists.")

def test_read(db_collection, field, value):
    print()
    returned_data = db_collection.find_one({field: value})
    pprint.pprint(returned_data)
    print()

def test_update(db_collection, field, value):
    #return_document = db_collection.find_one_and_update({field: value}, { '$set':{'name': 'Ryan',"Extra Field": "added just on the fly", 'id' : 700, 'email': 'ryanb4@umbc.edu','password hash': 'hf992384h','save games':['4(2(3)(1))(6(5))','4(2(3)(1))(6(5))','4(2(3)(1))(6(5))',], 'points': 900,'rank': 'silver','badges': [3,4,8,], 'friends':	['Kulsoom','Nick','Maksim','Naomi',], 'current story level': 7 }}, upsert=True)
    #return_document = db_collection.find_one_and_update({field: value}, { '$unset':{'name': 'Ryan',"Extra Field": "added just on the fly", 'id' : 700, 'email': 'ryanb4@umbc.edu','password hash': 'hf992384h','save games':['4(2(3)(1))(6(5))','4(2(3)(1))(6(5))','4(2(3)(1))(6(5))',], 'points': 900,'rank': 'silver','badges': [3,4,8,], 'friends':	['Kulsoom','Nick','Maksim','Naomi',], 'current story level': 7 }}, upsert=True)

    #return_document = db_collection.find_one_and_update({field: value}, { '$set':{"Extra Field 2": "Testing setting just one field at a time"}}, upsert=True)
    return_document = db_collection.find_one_and_update({field: value}, { '$unset':{"Extra Field 2": "Testing setting just one field at a time"}}, upsert=True)

    pprint.pprint(return_document)

def add_Activegame(db, id1:int, id2:int, id3:int, id4:int, gamestate:str):
    game_made = False
    Game_collection = db.Active_Games
    Lobby_collection = db.Lobby

    while not game_made:
        gameid = random.randrange(0, 100)
        returned_data = Game_collection.find_one({"game id": gameid})
        if returned_data is None:
            test_document =  {"game id": gameid, 'users':[id1, id2, id3, id4], 'points': 0, 'game state':gamestate, 'player id current turn': id2}

            #Remove the players from the lobby
            for id in [id1, id2, id3, id4]:
                Lobby_collection.find_one_and_delete({"user id": id})
                #What happenes when the player is being added to the game but not in the Lobby?

            Game_collection.insert_one(test_document).inserted_id
            return gameid


def add_player_to_lobby(db, id, name):
    Lobby_collection = db.Lobby
    already_in_lobby = Lobby_collection.find_one({"user id": id})

    Game_collection = db.Active_Games
    already_in_game = Game_collection.find_one({"user id": id})

    #Make sure the user is not in the lobby or in a game then add them to lobby
    if already_in_lobby is None and already_in_game is None:
        test_document = {"user id": id, "user name": name}
        return Lobby_collection.insert_one(test_document).inserted_id

    else:
        print(name, "is already in the lobby or in a game")

def get_rankings(db_collection):
    return db_collection.find({},{'password hash': 0, 'save games': 0, 'badges': 0, 'friends': 0, 'current story level': 0,}).sort('points')


if __name__ == '__main__':

    print("\nTesting DB connection\n")

    #Connect to mongo
    client = MongoClient(DATABASE_URL1)

    #Access the database
    db = client.InitialDB

    #Access a colelction
    User_collection = db.User_profile

    test_create(User_collection, "Ryan", "ryanb4@umbc.edu")
    test_read(User_collection, "email", "ryanb4@umbc.edu")
    #test_update(User_collection, "email", "ryanb4@umbc.edu")

    Game_collection = db.Active_Games

    add_Activegame(db, 1,2,3,4,'4(2(3)(1))(6(5))')

    add_player_to_lobby(db, 1, "Nick")
    add_player_to_lobby(db, 2, "Naomi")
    add_player_to_lobby(db, 3, "Maksim")
    add_player_to_lobby(db, 4, "Kulsoom")

    for user in get_rankings(User_collection):
        pprint.pprint(user)
