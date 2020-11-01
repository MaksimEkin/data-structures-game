"""
python manage.py test profile_page.database.test_db
"""

import sys
from django.test import TestCase
from profile_page.database import profile_page_db as mongo

def where():
    """ Prints line location of the calling test function """
    return " -- test on line "+str(sys._getframe(1).f_lineno)

class BColors:
    """ Colors for printing """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class DBCreateUserProfile( TestCase ):
    """ Test for user profile creation """

    def setUp( self ):
        """ creates user data needed for tests """

        self.user = {"user_id":"5f7d1b1d8fd2b816c48c148b","badges":[31,24,83],
        "current_story_level":9,"email":"ryanb777@umbc.edu",
        "friends":["Kulsoom2","Nick2","Maksim2","Naomi2"],
        "user_name":"ryan2","password_hash":"well,hello there","points":98274,"rank":"diamond",
        "save_games":["4(2(3)(no))(6(5))","4(2(3)(1))(6(5))","4(2(3)(1))(6(5))"]}

        self.user2 = {"auth_token":"cool!", "user_id":"second_guy","badges":[31,24,83],
        "current_story_level":9,"email":"ryan@umbc.edu",
        "friends":["Kulsoom2","Nick2","Maksim2","Naomi2"],
        "user_name":"ryan2","password_hash":"well,hello there","points":98274,"rank":"diamond",
        "save_games":["4(2(3)(no))(6(5))","4(2(3)(1))(6(5))","4(2(3)(1))(6(5))"]}

    def test_save( self ):
        """ The user document was saved in the database """
        created_user = mongo.save_user( self.user )
        self.assertEqual( created_user, True,
        msg=f'{BColors.FAIL}\t[-]\tUser was not created in the Database!{BColors.ENDC}' + where() )
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database save user.{BColors.ENDC}")

    def test_duplicate_save( self ):
        """ The user document is a duplicate and should fail saving in the database """
        created_user = mongo.save_user( self.user )
        created_user = mongo.save_user( self.user )

        self.assertEqual( created_user, False,
        msg=f'{BColors.FAIL}\t[-]\tGame was not created in the Database!{BColors.ENDC}' + where() )
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database save user duplicate.\
            {BColors.ENDC}")

    def test_create( self ):
        """ The user document was created in the database """
        created_user = mongo.create_user( self.user2["user_id"],
            self.user2["password_hash"], self.user2["email"], self.user2["auth_token"] )

        self.assertEqual( created_user, True,
            msg=f'{BColors.FAIL}\t[-]\tUser was not created in the Database!\
            {BColors.ENDC}' + where() )
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database create user.{BColors.ENDC}")

    def test_create_duplicate_uid( self ):
        """ The user document was not created, duplicate user id the database """
        created_user = mongo.save_user( self.user )
        created_user = mongo.create_user( self.user["user_id"], self.user2["password_hash"],
            self.user2["email"], self.user2["auth_token"] )

        mongo.remove_user(self.user["user_id"])
        self.assertEqual( created_user, False, msg=f'{BColors.FAIL}\t[-]\
            \tDuplicate user was created in the Database!{BColors.ENDC}' + where() )
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database create user duplicate id.\
            {BColors.ENDC}")

    def test_create_duplicate_email( self ):
        """ The user document was not created, duplicate user email in the database """
        created_user = mongo.save_user( self.user )
        created_user = mongo.create_user( self.user2["user_id"],
            self.user2["password_hash"], self.user["email"], self.user2["auth_token"] )
        mongo.remove_user(self.user["user_id"])

        self.assertEqual( created_user, False, msg=f'{BColors.FAIL}\
            \t[-]\tDuplicate user was created in the Database!{BColors.ENDC}' + where() )
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database create duplicate user email.\
            {BColors.ENDC}")

    def tearDown( self ):
        """ Removes users needed in tests """
        mongo.remove_user(self.user["user_id"])
        mongo.remove_user(self.user2["user_id"])

class DBReadUserProfile( TestCase ):
    """ Test for reading profile """

    def setUp( self ):
        """ creates user data needed for tests """

        self.user = {"user_id":"5f7d1b1d8fd2b816c48c148b","badges":[31,24,83],
        "current_story_level":9,"email":"ryanb777@umbc.edu",
        "friends":["Kulsoom2","Nick2","Maksim2","Naomi2"],
        "user_name":"ryan2","password_hash":"well,hello there","points":98274,"rank":"diamond",
        "save_games":["4(2(3)(no))(6(5))","4(2(3)(1))(6(5))","4(2(3)(1))(6(5))"]}

        mongo.save_user( self.user )

    def test_read_correct( self ):
        """ The user document was read from the database """
        read_user = mongo.read_one_user( self.user["user_id"] )

        self.assertEqual( read_user["user_id"], self.user["user_id"], msg=f'{BColors.FAIL}\
            \t[-]\tGame Id returned from read board does not equal expected!\
            {BColors.ENDC}' + where() )
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database read.{BColors.ENDC}" )

    def test_read_nonexist( self ):
        """ The user document should not be read from the database """
        read_user = mongo.read_one_user(
            "This name should really not exist in the database, and if it does, YEESH!" )

        self.assertEqual( read_user, False, msg=f'{BColors.FAIL}\
            \t[-]\tIncorrect return for non-existant user!{BColors.ENDC}' + where() )
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database read nonexistant.{BColors.ENDC}")

    def test_read_user_name( self ):
        """ The user's name was read from the database """
        read_user_name = mongo.read_user_name( self.user["user_id"] )

        self.assertEqual( read_user_name["user_name"], self.user["user_name"],
            msg=f'{BColors.FAIL}\t[-]\tUsername returned from read board does not equal expected!\
            {BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database read-name.{BColors.ENDC}")

    def test_read_user_name_nonexist( self ):
        """ The user-name document should not be read from the database """
        read_user = mongo.read_user_name(
            "This id should really not exist in the database, and if it does, YEESH!" )

        self.assertEqual( read_user, False, msg=f'{BColors.FAIL}\
            \t[-]\tIncorrect return for non-existant user id!{BColors.ENDC}' + where() )
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database read-name nonexistant.\
            {BColors.ENDC}")

    def tearDown( self ):
        """ Removes user needed in tests """
        mongo.remove_user(self.user["user_id"])

class DBUpdateUserProfile( TestCase ):
    """ Test for updating all profile data """

    def setUp( self ):
        """ creates user data needed for tests """

        self.user = {"user_id":"5f7d1b1d8fd2b816c48c148b","badges":[31,24,83],
        "current_story_level":9,"email":"ryanb777@umbc.edu",
        "friends":["Kulsoom2","Nick2","Maksim2","Naomi2"],
        "user_name":"ryan2","password_hash":"well,hello there","points":98274,"rank":"diamond",
        "save_games":["4(2(3)(no))(6(5))","4(2(3)(1))(6(5))","4(2(3)(1))(6(5))"]}

        self.user2 = {"user_id":"5f7d1b1d8fd2b816c48c148b","badges":[989879879831,24,83],
        "current_story_level":9,"email":"ryanb777@umbc.edu",
        "friends":["Kulsoom2","Nick2","Maksim2","Naomi2"],
        "user_name":"ryan2","password_hash":"well,hello there","points":98274,"rank":"diamond",
        "save_games":["4(2(3)(no))(6(5))","4(2(3)(1))(6(5))","4(2(3)(1))(6(5))"]}

        mongo.save_user( self.user )

    def test_update_correct( self ):
        """ The user document is updated in the database """
        updated_user = mongo.update_user( self.user["user_id"], self.user2 )

        self.assertEqual( updated_user["user_id"], self.user2["user_id"],
            msg=f'{BColors.FAIL}\t[-]\tUser Id returned from read user does not equal expected!\
            {BColors.ENDC}' + where() )
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database update.{BColors.ENDC}")

    def test_update_nonexist( self ):
        """ The user document should not be updated from the database """
        updated_user = mongo.update_user(
            "This name should really not exist in the database, and if it does, YEESH!", self.user )

        self.assertEqual( updated_user, False, msg=f'{BColors.FAIL}\
            \t[-]\tIncorrect return for non-existant user!{BColors.ENDC}' + where() )
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database update nonexistant.\
            {BColors.ENDC}")

    def tearDown(self):
        """ Removes user needed in tests """
        mongo.remove_user(self.user["user_id"])

class DBUpdateUserGame( TestCase ):
    """ Test for updating a user game in the profile """

    def setUp( self ):
        """ creates user data needed for tests """

        self.board = {"game_id": "60afce36-085a-11eb-b6ab-acde48001122",
        "graph": {"nodes": "node4(node2(node3)(node1))(node6(node5))",
        "node_points": {"node1": 1,"node2": 2,"node3": 3,"node4": 4,"node5": 5,"node6": 6},
        "gold_node": "node5","balanced": True},"player_ids": ["id2","id3","id4","id5"],
        "player_names": ["naomi","kulsoom","nick","ryan"],
        "player_points": {"id2": 2,"id3": 2,"id4": 3,"id5": 10},"turn": "id2",
        "cards": {"id2": ["card1","card2","card3"],"id3": ["card1","card2","card3"],
        "id4":["card1","card2","card3"],"id5": ["card1","card2","card3"]},"gold_node": False,
        "difficulty": "Medium","num_players": 4,"online": True,"curr_data_structure": "AVL",
        "selected_data_structures": ["AVL","Stack"],"timed_game": False,
        "seconds_until_next_ds": 60,"time_created": "07/10/2020 00:05:47",
        "end_game": False}

        self.board2 = {"game_id": "60afce36-085a-11eb-b6ab-acde48001122",
        "graph": {"nodes": "DID ITnode4(node2(node3)(node1))(node6(node5))",
        "node_points": {"node1": 1,"node2": 2,"node3": 3,"node4": 4,"node5": 5,"node6": 6},
        "gold_node": "node5","balanced": True},"player_ids": ["changed player","id3","id4","id5"],
        "player_names": ["naomi","kulsoom","nick","ryan"],
        "player_points": {"id2": 2,"id3": 2,"id4": 3,"id5": 10},"turn": "id2",
        "cards": {"id2": ["card1","card2","card3"],"id3": ["card1","card2","card3"],
        "id4":["card1","card2","card3"],"id5": ["card1","card2","card3"]},
        "gold_node": False,"difficulty": "Medium","num_players": 4,"online": True,
        "curr_data_structure": "AVL","selected_data_structures": ["AVL","Stack"],
        "timed_game": False,"seconds_until_next_ds": 60,"time_created": "07/10/2020 00:05:47",
        "end_game": False}

        self.user = {"user_id":"5f7d1b1d8fd2b816c48c148b",
        "badges":[31,24,83],"current_story_level":9,"email":"ryanb777@umbc.edu",
        "friends":["Kulsoom2","Nick2","Maksim2","Naomi2"],"user_name":"ryan2",
        "password_hash":"well,hello there","points":98274,"rank":"diamond",
        "save_games":[self.board,"4(2(3)(1))(6(5))","4(2(3)(1))(6(5))"]}

        self.new_graph = {"nodes": "DID IT WRETITREE ???5))"}

        mongo.save_user( self.user )

    def test_update_game_correct( self ):
        """ The user document is updated in the database """
        original_user = self.user
        updated_game = mongo.update_user_game( self.user["user_id"],
            self.board["game_id"], self.board2 )

        self.assertEqual( updated_game != original_user, True,
            msg=f'{BColors.FAIL}\t[-]\tUser Id returned from read user does not equal expected!\
            {BColors.ENDC}' + where() )
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database update.{BColors.ENDC}")

    def test_update_game_nonexist( self ):
        """ The user document should not be updated from the database """
        updated_user = mongo.update_user_game( self.user["user_id"],
            "This name should really not exist in the database, and if it does, YEESH!",
            self.board2)

        self.assertEqual( updated_user, False, msg=f'{BColors.FAIL}\
            \t[-]\tIncorrect return for non-existant user!{BColors.ENDC}' + where() )
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database update game nonexistant.\
            {BColors.ENDC}")

    def tearDown( self ):
        """ Removes user needed in tests """
        mongo.remove_user(self.user["user_id"])

class DBDeleteUser( TestCase ):
    """ Test for deleting a user profile """

    def setUp( self ):
        """ creates user data needed for tests """

        self.user = {"user_id":"5f7d1b1d8fd2b816c48c148b","badges":[31,24,83],
        "current_story_level":9,"email":"ryanb777@umbc.edu",
        "friends":["Kulsoom2","Nick2","Maksim2","Naomi2"],
        "user_name":"ryan2","password_hash":"well,hello there",
        "points":98274,"rank":"diamond",
        "save_games":[{'game_id': '60afce36-085a-11eb-b6ab-acde48001122',
        'graph': {'nodes': 'DID IT WRETITREE ???5))'},
        'player_ids': ['id2', 'id3', 'id4', 'id5'],
        'player_names': ['naomi', 'kulsoom', 'nick', 'ryan'],
        'player_points': {'id2': 2, 'id3': 2, 'id4': 3, 'id5': 10}, 'turn': 'id2',
        'cards': {'id2': ['card1', 'card2', 'card3'], 'id3': ['card1', 'card2', 'card3'],
        'id4': ['card1', 'card2', 'card3'], 'id5': ['card1', 'card2', 'card3']},
        'gold_node': False, 'difficulty': 'Medium', 'num_players': 4, 'online': True,
        'curr_data_structure': 'AVL', 'selected_data_structures': ['AVL', 'Stack'],
        'timed_game': False, 'seconds_until_next_ds': 60, 'time_created': '07/10/2020 00:05:47',
        'end_game': False},"4(2(3)(1))(6(5))","4(2(3)(1))(6(5))"]}

        mongo.save_user( self.user )

    def test_delete_correct( self ):
        """ The user document was deleted in the database """
        deleted_user = mongo.remove_user( self.user["user_id"] )

        self.assertEqual( deleted_user, 1, msg=f'{BColors.FAIL}\
            \t[-]\tDatabase was not able to delete the user!{BColors.ENDC}' + where() )
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database delete.{BColors.ENDC}")

    def test_delete_nonexist( self ):
        """ The user document should not be deleted from the database """
        deleted_user = mongo.remove_user(
            "This name shouldn't exist in the database, and if it does, it deserves to be deleted" )

        self.assertEqual( deleted_user, False,
            msg=f'{BColors.FAIL}\t[-]\tIncorrect return for non-existant user!\
            {BColors.ENDC}' + where() )
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database delete nonexistant.\
            {BColors.ENDC}")

class DBDeleteGames( TestCase ):
    """ Test for deleting a game in the user profile """

    def setUp( self ):
        """ creates user data needed for tests """

        self.user = {"user_id":"5f7d1b1d8fd2b816c48c148b","badges":[31,24,83],
        "current_story_level":9,"email":"ryanb777@umbc.edu",
        "friends":["Kulsoom2","Nick2","Maksim2","Naomi2"],
        "user_name":"ryan2","password_hash":"well,hello there","points":98274,
        "rank":"diamond","save_games":[{'game_id': '60afce36-085a-11eb-b6ab-acde48001122',
        'graph': {'nodes': 'DID IT WRETITREE ???5))'}, 'player_ids': ['id2', 'id3', 'id4', 'id5'],
        'player_names': ['naomi', 'kulsoom', 'nick', 'ryan'], 'player_points': {'id2': 2, 'id3': 2,
        'id4': 3, 'id5': 10}, 'turn': 'id2', 'cards': {'id2': ['card1', 'card2', 'card3'],
        'id3': ['card1', 'card2', 'card3'], 'id4': ['card1', 'card2', 'card3'],
        'id5': ['card1', 'card2', 'card3']}, 'gold_node': False, 'difficulty': 'Medium',
        'num_players': 4, 'online': True, 'curr_data_structure': 'AVL',
        'selected_data_structures': ['AVL', 'Stack'], 'timed_game': False,
        'seconds_until_next_ds': 60, 'time_created': '07/10/2020 00:05:47',
        'end_game': False},"4(2(3)(1))(6(5))","4(2(3)(1))(6(5))"]}

        mongo.save_user( self.user )

    def test_delete_correct( self ):
        """ The user document was deleted in the database """
        deleted_user = mongo.delete_game(
            self.user["user_id"], self.user['save_games'][0]["game_id"])

        self.assertEqual( deleted_user, 1, msg=f'{BColors.FAIL}\
            \t[-]\tDatabase was not able to delete the user!{BColors.ENDC}' + where() )
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database delete.{BColors.ENDC}")

    def test_delete_nonexist( self ):
        """ The user document should not be deleted from the database """
        deleted_user = mongo.delete_game(
            "This name shouldn't exist in the database, and if it does, it desrves to be deleted",
            self.user['save_games'][0]["game_id"] )

        self.assertEqual( deleted_user, False,
            msg=f'{BColors.FAIL}\t[-]\tIncorrect return for non-existant user!\
            {BColors.ENDC}' + where() )
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database delete nonexistant.\
            {BColors.ENDC}")

class DBList( TestCase ):
    """ Test for listing games in a user profile """

    def setUp( self ):
        """ creates user data needed for tests """

        self.user = {"user_id":"5f7d1b1d8fd2b816c48c148b","badges":[31,24,83],
        "current_story_level":9,"email":"ryanb777@umbc.edu",
        "friends":["Kulsoom2","Nick2","Maksim2","Naomi2"],
        "user_name":"ryan2","password_hash":"well,hello there","points":98274,
        "rank":"diamond","save_games":[{'game_id': '60afce36-085a-11eb-b6ab-acde48001122',
        'graph': {'nodes': 'DID IT WRETITREE ???5))'},
        'player_ids': ['id2', 'id3', 'id4', 'id5'],
        'player_names': ['naomi', 'kulsoom', 'nick', 'ryan'],
        'player_points': {'id2': 2, 'id3': 2, 'id4': 3, 'id5': 10},
        'turn': 'id2', 'cards': {'id2': ['card1', 'card2', 'card3'],
        'id3': ['card1', 'card2', 'card3'],
        'id4': ['card1', 'card2', 'card3'], 'id5': ['card1', 'card2', 'card3']},
        'gold_node': False, 'difficulty': 'Medium', 'num_players': 4, 'online': True,
        'curr_data_structure': 'AVL', 'selected_data_structures': ['AVL', 'Stack'],
        'timed_game': False, 'seconds_until_next_ds': 60,
        'time_created': '07/10/2020 00:05:47',
        'end_game': False},"4(2(3)(1))(6(5))","4(2(3)(1))(6(5))"]}

        mongo.save_user( self.user )

    def test_list_users_correct( self ):
        """ The user document was added to the list and appears in the returned list """
        found = False

        game_cursor = mongo.list_users()
        for gameid in game_cursor:
            if self.user["user_id"] == gameid["user_id"]:
                found = True

        self.assertEqual( found, True,
            msg=f'{BColors.FAIL}\t[-]\tAdded user was not in the listed games!{BColors.ENDC}'
             + where() )
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database list.{BColors.ENDC}")

    def test_list_user_games_correct( self ):
        """ The user's games appears in the returned list """
        user_games = mongo.list_user_games(self.user["user_id"])

        self.assertEqual(user_games[0], self.user["save_games"][0], msg=f'{BColors.FAIL}\
            \t[-]\tAdded user was not in the listed games!{BColors.ENDC}' + where() )
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database list.{BColors.ENDC}")

    def tearDown( self ):
        """ Removes user needed in tests """
        mongo.remove_user(self.user["user_id"])

class DBSaveUserGames( TestCase ):
    """ Test for saving a game in a user profile """

    def setUp( self ):
        """ creates user data needed for tests """

        self.board = {"game_id": "60afce36-085a-11eb-b6ab-acde48001122",
        "graph": {"nodes": "node4(node2(node3)(node1))(node6(node5))",
        "node_points": {"node1": 1,"node2": 2,"node3": 3,"node4": 4,"node5": 5,"node6": 6},
        "gold_node": "node5","balanced": True},"player_ids": ["id2","id3","id4","id5"],
        "player_names": ["naomi","kulsoom","nick","ryan"],
        "player_points": {"id2": 2,"id3": 2,"id4": 3,"id5": 10},"turn": "id2",
        "cards": {"id2": ["card1","card2","card3"],"id3": ["card1","card2","card3"],
        "id4":["card1","card2","card3"],"id5": ["card1","card2","card3"]},"gold_node": False,
        "difficulty": "Medium","num_players": 4,"online": True,"curr_data_structure": "AVL",
        "selected_data_structures": ["AVL","Stack"],"timed_game": False,
        "seconds_until_next_ds": 60,"time_created": "07/10/2020 00:05:47",
        "end_game": False}

        self.board2 = {"game_id": "new board id",
        "graph": {"nodes": "DID ITnode4(node2(node3)(node1))(node6(node5))",
        "node_points": {"node1": 1,"node2": 2,"node3": 3,"node4": 4,"node5": 5,"node6": 6},
        "gold_node": "node5","balanced": True},"player_ids": ["changed player","id3","id4","id5"],
        "player_names": ["naomi","kulsoom","nick","ryan"],
        "player_points": {"id2": 2,"id3": 2,"id4": 3,"id5": 10},"turn": "id2",
        "cards": {"id2": ["card1","card2","card3"],"id3": ["card1","card2","card3"],
        "id4":["card1","card2","card3"],"id5": ["card1","card2","card3"]},
        "gold_node": False,"difficulty": "Medium","num_players": 4,"online": True,
        "curr_data_structure": "AVL","selected_data_structures": ["AVL","Stack"],
        "timed_game": False,"seconds_until_next_ds": 60,"time_created": "07/10/2020 00:05:47",
        "end_game": False}

        self.user = {"sharing": True, "auth_token":"cool!","user_id":"5f7d1b1d8fd2b816c48c148b",
        "badges":[31,24,83],"current_story_level":9,"email":"ryanb777@umbc.edu",
        "friends":["Kulsoom2","Nick2","Maksim2","Naomi2"],
        "user_name":"ryan2","password_hash":"well,hello there","points":98274,"rank":"diamond",
        "save_games":[self.board,"4(2(3)(1))(6(5))","4(2(3)(1))(6(5))"]}

        mongo.save_user( self.user )

    def tearDown( self ):
        """ Removes user needed in tests """
        mongo.remove_user(self.user["user_id"])

    def test_save_game_correct( self ):
        """ The user 's new game is saved in the database """
        saved_game = mongo.save_game( self.user["user_id"], self.board2 )

        self.assertEqual( saved_game, True, msg=f'{BColors.FAIL}\
            \t[-]\tUser\'s new game was not saved!{BColors.ENDC}' + where() )
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database save new game.{BColors.ENDC}")

    def test_save_game_duplicate( self ):
        """ The user 's new game is saved in the database """
        saved_game = mongo.save_game( self.user["user_id"], self.board )

        self.assertEqual( saved_game, False, msg=f'{BColors.FAIL}\
            \t[-]\tUser\'s duplicate game was saved!{BColors.ENDC}' + where() )
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database save duplicate game.\
            {BColors.ENDC}")

class DBReadUserGames( TestCase ):
    """ Test for reading a game in a user profile """

    def setUp( self ):
        """ creates user data needed for tests """

        self.user = {"sharing": True, "auth_token":"cool!","user_id":"5f7d1b1d8fd2b816c48c148b",
        "badges":[31,24,83],"current_story_level":9,"email":"ryanb777@umbc.edu",
         "friends":["Kulsoom2","Nick2","Maksim2","Naomi2"],
        "user_name":"ryan2","password_hash":"well,hello there","points":98274,"rank":"diamond",
        "save_games":[{'game_id': '60afce36-085a-11eb-b6ab-acde48001122',
        'graph': {'nodes': 'DID IT WRETITREE ???5))'},
        'player_ids': ['id2', 'id3', 'id4', 'id5'],
        'player_names': ['naomi', 'kulsoom', 'nick', 'ryan'],
        'player_points': {'id2': 2, 'id3': 2, 'id4': 3, 'id5': 10}, 'turn': 'id2',
        'cards': {'id2': ['card1', 'card2', 'card3'], 'id3': ['card1', 'card2', 'card3'],
        'id4': ['card1', 'card2', 'card3'], 'id5': ['card1', 'card2', 'card3']},
        'gold_node': False, 'difficulty': 'Medium', 'num_players': 4, 'online': True,
        'curr_data_structure': 'AVL', 'selected_data_structures': ['AVL', 'Stack'],
        'timed_game': False, 'seconds_until_next_ds': 60, 'time_created': '07/10/2020 00:05:47',
        'end_game': False},"4(2(3)(1))(6(5))","4(2(3)(1))(6(5))"]}

        mongo.save_user( self.user )

    def test_load_board( self ):
        """ The user game document was found """
        user_game = mongo.load_board( self.user["user_id"], self.user['save_games'][0]["game_id"] )

        self.assertEqual( user_game, self.user["save_games"][0], msg=f'{BColors.FAIL}\
            \t[-]\tUser game save was not found!{BColors.ENDC}' + where() )
        print( f"{BColors.OKGREEN}\t[+]\tPass User-Profile database load game.{BColors.ENDC}" )

    def test_share_user_game( self ):
        """ The user game was shared """
        user_share_game = mongo.load_board(
            self.user["user_id"], self.user['save_games'][0]["game_id"] )

        self.assertEqual( user_share_game, self.user["save_games"][0],
            msg=f'{BColors.FAIL}\t[-]\tUser game save was not found!{BColors.ENDC}' + where() )
        print( f"{BColors.OKGREEN}\t[+]\tPass User-Profile database share game.{BColors.ENDC}" )

    def tearDown( self ):
        """ Removes user needed in tests """
        mongo.remove_user( self.user["user_id"] )

class DBUserAuthentication( TestCase ):
    """ Test for user profile authentication """

    def setUp( self ):
        """ creates user data needed for tests """

        self.user = {"sharing": True, "auth_token":"cool!","user_id":"5f7d1b1d8fd2b816c48c148b",
        "badges":[31,24,83],"current_story_level":9,"email":"ryanb777@umbc.edu",
        "friends":["Kulsoom2","Nick2","Maksim2","Naomi2"],"user_name":"ryan2",
        "password_hash":"well,hello there","points":98274,"rank":"diamond",
        "save_games":[{'game_id': '60afce36-085a-11eb-b6ab-acde48001122',
        'graph': {'nodes': 'DID IT WRETITREE ???5))'}, 'player_ids': ['id2', 'id3', 'id4', 'id5'],
        'player_names': ['naomi', 'kulsoom', 'nick', 'ryan'],
        'player_points': {'id2': 2, 'id3': 2, 'id4': 3, 'id5': 10},
        'turn': 'id2', 'cards': {'id2': ['card1', 'card2', 'card3'],
        'id3': ['card1', 'card2', 'card3'], 'id4': ['card1', 'card2', 'card3'],
        'id5': ['card1', 'card2', 'card3']}, 'gold_node': False, 'difficulty': 'Medium',
        'num_players': 4, 'online': True, 'curr_data_structure': 'AVL',
        'selected_data_structures': ['AVL', 'Stack'],
        'timed_game': False, 'seconds_until_next_ds': 60, 'time_created': '07/10/2020 00:05:47',
        'end_game': False},"4(2(3)(1))(6(5))","4(2(3)(1))(6(5))"]}

        mongo.save_user( self.user )

    def test_check_uid_email( self ):
        """ The user's name and email are found in the database """
        user_exists = mongo.user_or_email( self.user["user_id"], self.user["email"] )

        self.assertEqual( user_exists, True,
            msg=f'{BColors.FAIL}\t[-]\tUser doesn\'t exist!{BColors.ENDC}' + where() )
        print( f"{BColors.OKGREEN}\t[+]\tPass User-Profile database user or email found.\
            {BColors.ENDC}" )

    def test_check_uid( self ):
        """ The user's name is found in the database """
        user_exists = mongo.user_or_email( self.user["user_id"], "none" )

        self.assertEqual( user_exists, True,
            msg=f'{BColors.FAIL}\t[-]\tUser id doesn\'t exist!{BColors.ENDC}' + where() )
        print( f"{BColors.OKGREEN}\t[+]\tPass User-Profile database user found.{BColors.ENDC}" )

    def test_check_email( self ):
        """ The user's email is found in the database """
        user_exists = mongo.user_or_email( "none", self.user["email"] )

        self.assertEqual( user_exists, True,
            msg=f'{BColors.FAIL}\t[-]\tUser email doesn\'t exist!{BColors.ENDC}' + where() )
        print( f"{BColors.OKGREEN}\t[+]\tPass User-Profile database email found.{BColors.ENDC}" )

    def test_check_uid_email_incorrect( self ):
        """ The user's name and email are not found in the database """
        user_exists = mongo.user_or_email( "none", "also none" )

        self.assertEqual( user_exists, False,
            msg=f'{BColors.FAIL}\t[-]\tUser doesn\'t exist!{BColors.ENDC}' + where() )
        print( f"{BColors.OKGREEN}\t[+]\tPass User-Profile database user or email nonexist.\
            {BColors.ENDC}" )

    def test_login_correct( self ):
        """ The user's password hash match the database record """
        logged_in = mongo.login( self.user["user_id"], self.user["password_hash"] )

        self.assertEqual( logged_in, True,
            msg=f'{BColors.FAIL}\t[-]\tUser password doesn\'t match!{BColors.ENDC}' + where() )
        print( f"{BColors.OKGREEN}\t[+]\tPass User-Profile database login.{BColors.ENDC}" )

    def test_login_incorrect( self ):
        """ The user's password hash does not match the database record """
        logged_in = mongo.login( self.user["user_id"], "none" )

        self.assertEqual( logged_in, False,
            msg=f'{BColors.FAIL}\t[-]\tUser\'s fake password was accepted!{BColors.ENDC}'
            + where() )
        print( f"{BColors.OKGREEN}\t[+]\tPass User-Profile database login incorrect.\
            {BColors.ENDC}" )

    def test_login_invalid( self ):
        """ The invalid user's password hash should not be checked """
        logged_in = mongo.login( "none", "none" )

        self.assertEqual( logged_in, False,
            msg=f'{BColors.FAIL}\t[-]\tFake user\'s fake password was accepted!{BColors.ENDC}'
            + where() )
        print( f"{BColors.OKGREEN}\t[+]\tPass User-Profile database login invalid user & password.\
            {BColors.ENDC}" )

    def test_update_token( self ):
        """ The user's token was updated """
        new_token = mongo.update_token( self.user["user_id"], "new_token22" )

        self.assertEqual( new_token, True,
            msg=f'{BColors.FAIL}\t[-]\tUser\'s new token was not saved!{BColors.ENDC}' + where() )
        print( f"{BColors.OKGREEN}\t[+]\tPass User-Profile database update token.{BColors.ENDC}" )

    def test_update_token_incorrect( self ):
        """ The user's is invalid, so no token is updated """
        new_token = mongo.update_token( "fake user", "new_token22" )

        self.assertEqual( new_token, False,
            msg=f'{BColors.FAIL}\t[-]\tFake user\'s new token was saved!{BColors.ENDC}' + where() )
        print( f"{BColors.OKGREEN}\t[+]\tPass User-Profile database update token, fake user.\
            {BColors.ENDC}" )

    def test_check_user( self ):
        """ The user's token is valid """
        is_valid_tok = mongo.check_user( self.user["user_id"], self.user["auth_token"] )

        self.assertEqual( is_valid_tok, True,
            msg=f'{BColors.FAIL}\t[-]\tUser\'s token is not valid!{BColors.ENDC}' + where() )
        print( f"{BColors.OKGREEN}\t[+]\tPass User-Profile database check token.{BColors.ENDC}" )

    def test_check_user_incorrect( self ):
        """ The user's token is invalid """
        is_valid_tok = mongo.check_user( self.user["user_id"], "new_token22" )

        self.assertEqual( is_valid_tok, False,
            msg=f'{BColors.FAIL}\t[-]\tUser\'s invalid token was valid!{BColors.ENDC}' + where() )
        print( f"{BColors.OKGREEN}\t[+]\tPass User-Profile database check token, invalid token.\
            {BColors.ENDC}" )

    def tearDown( self ):
        """ Removes user needed in tests """
        mongo.remove_user( self.user["user_id"] )

class DBUserProfileGeneral( TestCase ):
    """ Test for user misc. profile functions """

    def setUp( self ):
        """ creates user data needed for tests """

        self.user = {"sharing": True, "auth_token":"cool!","user_id":"5f7d1b1d8fd2b816c48c148b",
        "badges":[31,24,83],"current_story_level":9,"email":"ryanb777@umbc.edu",
        "friends":["Kulsoom2","Nick2","Maksim2","Naomi2"],"user_name":"ryan2",
        "password_hash":"well,hello there","points":98274,"rank":"diamond",
        "save_games":[{'game_id': '60afce36-085a-11eb-b6ab-acde48001122',
        'graph': {'nodes': 'DID IT WRETITREE ???5))'}, 'player_ids': ['id2', 'id3', 'id4', 'id5'],
        'player_names': ['naomi', 'kulsoom', 'nick', 'ryan'],
        'player_points': {'id2': 2, 'id3': 2, 'id4': 3, 'id5': 10},
        'turn': 'id2', 'cards': {'id2': ['card1', 'card2', 'card3'],
        'id3': ['card1', 'card2', 'card3'],
        'id4': ['card1', 'card2', 'card3'], 'id5': ['card1', 'card2', 'card3']}, 'gold_node': False,
        'difficulty': 'Medium', 'num_players': 4, 'online': True, 'curr_data_structure': 'AVL',
        'selected_data_structures': ['AVL', 'Stack'],
        'timed_game': False, 'seconds_until_next_ds': 60,
        'time_created': '07/10/2020 00:05:47', 'end_game': False},
        "4(2(3)(1))(6(5))","4(2(3)(1))(6(5))"]}

        self.user2 = {"sharing": True, "auth_token":"second auth!","user_id":"useridneedswork",
        "badges":[31,24,83],"current_story_level":9,"email":"ryacmon man@umbc.edu",
        "friends":["Kulsoom2","Nick2","Maksim2","Naomi2"],"user_name":"ryan2",
        "password_hash":"well,hello there","points":98274,"rank":"diamond",
        "save_games":[{'game_id': 'not the same as the other user\'s game',
        'graph': {'nodes': 'DID IT WRETITREE ???5))'}, 'player_ids': ['id2', 'id3', 'id4', 'id5'],
        'player_names': ['naomi', 'kulsoom', 'nick', 'ryan'], 'player_points': {'id2': 2, 'id3': 2,
        'id4': 3, 'id5': 10}, 'turn': 'id2', 'cards': {'id2': ['card1', 'card2', 'card3'],
        'id3': ['card1', 'card2', 'card3'], 'id4': ['card1', 'card2', 'card3'],
        'id5': ['card1', 'card2', 'card3']}, 'gold_node': False, 'difficulty': 'Medium',
        'num_players': 4, 'online': True, 'curr_data_structure': 'AVL',
        'selected_data_structures': ['AVL', 'Stack'], 'timed_game': False,
        'seconds_until_next_ds': 60, 'time_created': '07/10/2020 00:05:47',
        'end_game': False},"4(2(3)(1))(6(5))","4(2(3)(1))(6(5))"]}

        mongo.save_user( self.user )
        mongo.save_user( self.user2 )

    def test_change_password( self ):
        """ The user's password is changed in the database """
        new_passhash = mongo.change_password( self.user["user_id"], "new password hash" )

        self.assertEqual( new_passhash, True,
            msg=f'{BColors.FAIL}\t[-]\tUser\'s cannot reset passhash!{BColors.ENDC}' + where() )
        print( f"{BColors.OKGREEN}\t[+]\tPass User-Profile database change passhash.\
            {BColors.ENDC}" )

    def test_change_sharing( self ):
        """ The user's share setting is changed in the database """
        sharable = mongo.change_share_setting( self.user["user_id"], False )
        mongo.change_share_setting( self.user["user_id"], True )

        self.assertEqual( sharable, True,
            msg=f'{BColors.FAIL}\t[-]\tUser\'s cannot change sharing!{BColors.ENDC}' + where() )
        print( f"{BColors.OKGREEN}\t[+]\tPass User-Profile database change sharing .\
            {BColors.ENDC}" )

    def test_check_share( self ):
        """ The user is willing to share games """
        can_share = mongo.check_user_share_setting( self.user["user_id"] )

        self.assertEqual( can_share, True,
            msg=f'{BColors.FAIL}\t[-]\tUser\'s cannot share when they should be able to!\
            {BColors.ENDC}' + where() )
        print( f"{BColors.OKGREEN}\t[+]\tPass User-Profile database check share.{BColors.ENDC}" )

    def test_share_board(self ):
        """ The user is able to share games """
        game_shared = mongo.share_game_board( self.user["user_id"],
            self.user2["user_id"], self.user['save_games'][0]["game_id"] )

        self.assertEqual( game_shared, True,
            msg=f'{BColors.FAIL}\t[-]\tUser\'s game was not shared!{BColors.ENDC}'  + where())
        print( f"{BColors.OKGREEN}\t[+]\tPass User-Profile database share game.{BColors.ENDC}" )

    def test_share_board_invalid_source( self ):
        """ The game is not shared, invalid source """
        game_shared = mongo.share_game_board(
            "Fake user 1", self.user2["user_id"], self.user['save_games'][0]["game_id"])

        self.assertEqual( game_shared, False,
            msg=f'{BColors.FAIL}\t[-]\tFake User\'s game was shared!{BColors.ENDC}' + where() )
        print( f"{BColors.OKGREEN}\t[+]\tPass User-Profile database share game, fake user 1.\
            {BColors.ENDC}" )

    def test_share_board_invalid_dest( self ):
        """ The game is not shared, invalid destination """
        game_shared = mongo.share_game_board(
            self.user["user_id"], "Fake user 2", self.user['save_games'][0]["game_id"])

        self.assertEqual( game_shared, False,
            msg=f'{BColors.FAIL}\t[-]\tUser\'s game was shared to fake user!{BColors.ENDC}'
            + where() )
        print( f"{BColors.OKGREEN}\t[+]\tPass User-Profile database share game, fake user 2.\
            {BColors.ENDC}" )

    def test_share_board_invalid_gameid( self ):
        """ The game is not shared, invalid source game id """
        game_shared = mongo.share_game_board(
            self.user["user_id"], self.user2["user_id"], "Fake Game" )

        self.assertEqual( game_shared, False,
            msg=f'{BColors.FAIL}\t[-]\tUser\'s fake game was shared!{BColors.ENDC}' + where() )
        print( f"{BColors.OKGREEN}\t[+]\tPass User-Profile database share invalid game.\
            {BColors.ENDC}" )

    def tearDown( self ):
        """ Removes users needed in tests """
        mongo.remove_user( self.user["user_id"] )
        mongo.remove_user( self.user2["user_id"] )
