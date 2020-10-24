"""
python manage.py test profile_page.database.test_db
"""

from profile_page.database import profile_page_db as mongo
from django.test import TestCase

class BColors:
    # Colors for printing
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class DBCreateUserProfile(TestCase):
    def setUp(self):
        self.user = {"user_id":"5f7d1b1d8fd2b816c48c148b","badges":[31,24,83],"current_story_level":9,"email":"ryanb777@umbc.edu","friends":["Kulsoom2","Nick2","Maksim2","Naomi2"],"user_name":"ryan2","password_hash":"well,hello there","points":98274,"rank":"diamond","save_games":["4(2(3)(no))(6(5))","4(2(3)(1))(6(5))","4(2(3)(1))(6(5))"]}
        self.fail_phrase = 'nah bro idk about it'
        mongo.remove_user(self.user["user_id"]) #Make sure the game is cleared out

    def test_create(self):
        """ The user document was created in the database """
        created_user = mongo.create_user( self.user )

        self.assertEqual( created_user, self.user["user_id"], msg=f'{BColors.FAIL}\t[-]\tUser was not created in the Database!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database save.{BColors.ENDC}")

    def test_duplicatecreate(self):
        """ The user document is a duplicate and should fail creation in the database """
        created_user = mongo.create_user( self.user )
        created_user = mongo.create_user( self.user )

        self.assertEqual( created_user, self.fail_phrase, msg=f'{BColors.FAIL}\t[-]\tGame was not created in the Database!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database save duplicate.{BColors.ENDC}")

    def tearDown(self):
        mongo.remove_user(self.user["user_id"])

class DBReadUserProfile(TestCase):
    def setUp(self):
        self.user = {"user_id":"5f7d1b1d8fd2b816c48c148b","badges":[31,24,83],"current_story_level":9,"email":"ryanb777@umbc.edu","friends":["Kulsoom2","Nick2","Maksim2","Naomi2"],"user_name":"ryan2","password_hash":"well,hello there","points":98274,"rank":"diamond","save_games":["4(2(3)(no))(6(5))","4(2(3)(1))(6(5))","4(2(3)(1))(6(5))"]}
        self.fail_phrase = 'nah bro idk about it'
        mongo.create_user( self.user )

    def test_read_correct(self):
        """ The user document was read from the database """
        read_user = mongo.read_one_user( self.user["user_id"] )

        self.assertEqual( read_user["user_id"], self.user["user_id"], msg=f'{BColors.FAIL}\t[-]\tGame Id returned from read board does not equal expected!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database read.{BColors.ENDC}")

    def test_read_nonexist(self):
        """ The user document should not be read from the database """
        read_user = mongo.read_one_user( "This name should really not exist in the database, and if it does, YEESH!" )

        self.assertEqual( read_user, self.fail_phrase, msg=f'{BColors.FAIL}\t[-]\tIncorrect return for non-existant user!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database read nonexistant.{BColors.ENDC}")

    def test_read_user_name(self):
        """ The user's name was read from the database """
        read_user_name = mongo.read_user_name( self.user["user_id"] )

        self.assertEqual( read_user_name["user_name"], self.user["user_name"], msg=f'{BColors.FAIL}\t[-]\tUsername returned from read board does not equal expected!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database read-name.{BColors.ENDC}")

    def test_read_user_name_nonexist(self):
        """ The user-name document should not be read from the database """
        read_user = mongo.read_user_name( "This id should really not exist in the database, and if it does, YEESH!" )

        self.assertEqual( read_user, self.fail_phrase, msg=f'{BColors.FAIL}\t[-]\tIncorrect return for non-existant user id!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database read-name nonexistant.{BColors.ENDC}")

    def tearDown(self):
        mongo.remove_user(self.user["user_id"])

class DBUpdateUserProfile(TestCase):
    def setUp(self):
        self.user = {"user_id":"5f7d1b1d8fd2b816c48c148b","badges":[31,24,83],"current_story_level":9,"email":"ryanb777@umbc.edu","friends":["Kulsoom2","Nick2","Maksim2","Naomi2"],"user_name":"ryan2","password_hash":"well,hello there","points":98274,"rank":"diamond","save_games":["4(2(3)(no))(6(5))","4(2(3)(1))(6(5))","4(2(3)(1))(6(5))"]}
        self.user2 = {"user_id":"5f7d1b1d8fd2b816c48c148b","badges":[989879879831,24,83],"current_story_level":9,"email":"ryanb777@umbc.edu","friends":["Kulsoom2","Nick2","Maksim2","Naomi2"],"user_name":"ryan2","password_hash":"well,hello there","points":98274,"rank":"diamond","save_games":["4(2(3)(no))(6(5))","4(2(3)(1))(6(5))","4(2(3)(1))(6(5))"]}
        self.fail_phrase = 'nah bro idk about it'
        mongo.create_user( self.user )

    def test_update_correct(self):
        """ The user document is updated in the database """
        updated_user = mongo.update_user( self.user["user_id"], self.user2 )

        self.assertEqual( updated_user["user_id"], self.user2["user_id"], msg=f'{BColors.FAIL}\t[-]\tUser Id returned from read user does not equal expected!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database update.{BColors.ENDC}")

    def test_update_nonexist(self):
        """ The user document should not be updated from the database """
        updated_user = mongo.update_user( "This name should really not exist in the database, and if it does, YEESH!", self.user )

        self.assertEqual( updated_user, self.fail_phrase, msg=f'{BColors.FAIL}\t[-]\tIncorrect return for non-existant user!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database update nonexistant.{BColors.ENDC}")

    def tearDown(self):
        mongo.remove_user(self.user["user_id"])


class DBUpdateUserGameAndGraph(TestCase):
    def setUp(self):
        self.board = {"game_id": "60afce36-085a-11eb-b6ab-acde48001122","graph": {"nodes": "node4(node2(node3)(node1))(node6(node5))","node_points": {"node1": 1,"node2": 2,"node3": 3,"node4": 4,"node5": 5,"node6": 6},"gold_node": "node5","balanced": True},"player_ids": ["id2","id3","id4","id5"],"player_names": ["naomi","kulsoom","nick","ryan"],"player_points": {"id2": 2,"id3": 2,"id4": 3,"id5": 10},"turn": "id2","cards": {"id2": ["card1","card2","card3"],"id3": ["card1","card2","card3"],"id4":["card1","card2","card3"],"id5": ["card1","card2","card3"]},"gold_node": False,"difficulty": "Medium","num_players": 4,"online": True,"curr_data_structure": "AVL","selected_data_structures": ["AVL","Stack"],"timed_game": False,"seconds_until_next_ds": 60,"time_created": "07/10/2020 00:05:47","end_game": False}
        self.board2 = {"game_id": "60afce36-085a-11eb-b6ab-acde48001122","graph": {"nodes": "DID ITnode4(node2(node3)(node1))(node6(node5))","node_points": {"node1": 1,"node2": 2,"node3": 3,"node4": 4,"node5": 5,"node6": 6},"gold_node": "node5","balanced": True},"player_ids": ["changed player","id3","id4","id5"],"player_names": ["naomi","kulsoom","nick","ryan"],"player_points": {"id2": 2,"id3": 2,"id4": 3,"id5": 10},"turn": "id2","cards": {"id2": ["card1","card2","card3"],"id3": ["card1","card2","card3"],"id4":["card1","card2","card3"],"id5": ["card1","card2","card3"]},"gold_node": False,"difficulty": "Medium","num_players": 4,"online": True,"curr_data_structure": "AVL","selected_data_structures": ["AVL","Stack"],"timed_game": False,"seconds_until_next_ds": 60,"time_created": "07/10/2020 00:05:47","end_game": False}

        self.new_graph = {"nodes": "DID IT WRETITREE ???5))"}
        self.user = {"user_id":"5f7d1b1d8fd2b816c48c148b","badges":[31,24,83],"current_story_level":9,"email":"ryanb777@umbc.edu","friends":["Kulsoom2","Nick2","Maksim2","Naomi2"],"user_name":"ryan2","password_hash":"well,hello there","points":98274,"rank":"diamond","save_games":[self.board,"4(2(3)(1))(6(5))","4(2(3)(1))(6(5))"]}

        self.fail_phrase = 'nah bro idk about it'
        mongo.create_user( self.user )

    def test_update_game_correct(self):
        """ The user document is updated in the database """
        original_user = self.user
        updated_game = mongo.update_user_game( self.user["user_id"], self.board["game_id"], self.board2 )

        self.assertEqual( updated_game != original_user, True, msg=f'{BColors.FAIL}\t[-]\tUser Id returned from read user does not equal expected!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database update.{BColors.ENDC}")

    def test_update_game_nonexist(self):
        """ The user document should not be updated from the database """
        original_user = self.user
        updated_user = mongo.update_user_game( self.user["user_id"], "This name should really not exist in the database, and if it does, YEESH!", self.board2)

        self.assertEqual( updated_user, original_user, msg=f'{BColors.FAIL}\t[-]\tIncorrect return for non-existant user!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database update game nonexistant.{BColors.ENDC}")

    def test_update_graph_correct(self):
        """ The user document is updated in the database """
        original = self.user
        updated = mongo.update_user_game_graph( self.user["user_id"], self.board["game_id"], self.new_graph )

        self.assertEqual( updated != original, True, msg=f'{BColors.FAIL}\t[-]\tUser Id returned from read user does not equal expected!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database graph update.{BColors.ENDC}")

    def test_update_graph_nonexist(self):
        """ The user document should not be updated from the database """
        original_user = self.user
        updated_graph = mongo.update_user_game_graph( self.user["user_id"], "This name should really not exist in the database, and if it does, YEESH!", self.board2)

        self.assertEqual( updated_graph, original_user, msg=f'{BColors.FAIL}\t[-]\tIncorrect return for non-existant user!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database update graph nonexistant.{BColors.ENDC}")

    def tearDown(self):
        mongo.remove_user(self.user["user_id"])


class DBDeleteUser(TestCase):
    def setUp(self):
        self.user = {"user_id":"5f7d1b1d8fd2b816c48c148b","badges":[31,24,83],"current_story_level":9,"email":"ryanb777@umbc.edu","friends":["Kulsoom2","Nick2","Maksim2","Naomi2"],"user_name":"ryan2","password_hash":"well,hello there","points":98274,"rank":"diamond","save_games":[{'game_id': '60afce36-085a-11eb-b6ab-acde48001122', 'graph': {'nodes': 'DID IT WRETITREE ???5))'}, 'player_ids': ['id2', 'id3', 'id4', 'id5'], 'player_names': ['naomi', 'kulsoom', 'nick', 'ryan'], 'player_points': {'id2': 2, 'id3': 2, 'id4': 3, 'id5': 10}, 'turn': 'id2', 'cards': {'id2': ['card1', 'card2', 'card3'], 'id3': ['card1', 'card2', 'card3'], 'id4': ['card1', 'card2', 'card3'], 'id5': ['card1', 'card2', 'card3']}, 'gold_node': False, 'difficulty': 'Medium', 'num_players': 4, 'online': True, 'curr_data_structure': 'AVL', 'selected_data_structures': ['AVL', 'Stack'], 'timed_game': False, 'seconds_until_next_ds': 60, 'time_created': '07/10/2020 00:05:47', 'end_game': False},"4(2(3)(1))(6(5))","4(2(3)(1))(6(5))"]}
        self.fail_phrase = 'nah bro idk about it'
        mongo.create_user( self.user )

    def test_delete_correct(self):
        """ The user document was deleted in the database """
        deleted_user = mongo.remove_user( self.user["user_id"] )

        self.assertEqual( deleted_user, 1, msg=f'{BColors.FAIL}\t[-]\tDatabase was not able to delete the user!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database delete.{BColors.ENDC}")

    def test_delete_nonexist(self):
        """ The user document should not be deleted from the database """
        deleted_user = mongo.remove_user( "This name should really not exist in the database, and if it does, it desrves to be deleted" )

        self.assertEqual( deleted_user, self.fail_phrase, msg=f'{BColors.FAIL}\t[-]\tIncorrect return for non-existant user!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database delete nonexistant.{BColors.ENDC}")

class DBDeleteGames(TestCase):
    def setUp(self):
        self.user = {"user_id":"5f7d1b1d8fd2b816c48c148b","badges":[31,24,83],"current_story_level":9,"email":"ryanb777@umbc.edu","friends":["Kulsoom2","Nick2","Maksim2","Naomi2"],"user_name":"ryan2","password_hash":"well,hello there","points":98274,"rank":"diamond","save_games":[{'game_id': '60afce36-085a-11eb-b6ab-acde48001122', 'graph': {'nodes': 'DID IT WRETITREE ???5))'}, 'player_ids': ['id2', 'id3', 'id4', 'id5'], 'player_names': ['naomi', 'kulsoom', 'nick', 'ryan'], 'player_points': {'id2': 2, 'id3': 2, 'id4': 3, 'id5': 10}, 'turn': 'id2', 'cards': {'id2': ['card1', 'card2', 'card3'], 'id3': ['card1', 'card2', 'card3'], 'id4': ['card1', 'card2', 'card3'], 'id5': ['card1', 'card2', 'card3']}, 'gold_node': False, 'difficulty': 'Medium', 'num_players': 4, 'online': True, 'curr_data_structure': 'AVL', 'selected_data_structures': ['AVL', 'Stack'], 'timed_game': False, 'seconds_until_next_ds': 60, 'time_created': '07/10/2020 00:05:47', 'end_game': False},"4(2(3)(1))(6(5))","4(2(3)(1))(6(5))"]}
        self.fail_phrase = 'nah bro idk about it'
        mongo.create_user( self.user )

    def test_delete_correct(self):
        """ The user document was deleted in the database """
        deleted_user = mongo.delete_user_game( self.user["user_id"], self.user['save_games'][0]["game_id"])

        self.assertEqual( deleted_user, 1, msg=f'{BColors.FAIL}\t[-]\tDatabase was not able to delete the user!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database delete.{BColors.ENDC}")

    def test_delete_nonexist(self):
        """ The user document should not be deleted from the database """
        deleted_user = mongo.delete_user_game( "This name should really not exist in the database, and if it does, it desrves to be deleted", self.user['save_games'][0]["game_id"] )

        self.assertEqual( deleted_user, self.fail_phrase, msg=f'{BColors.FAIL}\t[-]\tIncorrect return for non-existant user!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database delete nonexistant.{BColors.ENDC}")

class DBDeleteGraph(TestCase):
    def setUp(self):
        self.user = {"user_id":"5f7d1b1d8fd2b816c48c148b","badges":[31,24,83],"current_story_level":9,"email":"ryanb777@umbc.edu","friends":["Kulsoom2","Nick2","Maksim2","Naomi2"],"user_name":"ryan2","password_hash":"well,hello there","points":98274,"rank":"diamond","save_games":[{'game_id': '60afce36-085a-11eb-b6ab-acde48001122', 'graph': {'nodes': 'DID IT WRETITREE ???5))'}, 'player_ids': ['id2', 'id3', 'id4', 'id5'], 'player_names': ['naomi', 'kulsoom', 'nick', 'ryan'], 'player_points': {'id2': 2, 'id3': 2, 'id4': 3, 'id5': 10}, 'turn': 'id2', 'cards': {'id2': ['card1', 'card2', 'card3'], 'id3': ['card1', 'card2', 'card3'], 'id4': ['card1', 'card2', 'card3'], 'id5': ['card1', 'card2', 'card3']}, 'gold_node': False, 'difficulty': 'Medium', 'num_players': 4, 'online': True, 'curr_data_structure': 'AVL', 'selected_data_structures': ['AVL', 'Stack'], 'timed_game': False, 'seconds_until_next_ds': 60, 'time_created': '07/10/2020 00:05:47', 'end_game': False},"4(2(3)(1))(6(5))","4(2(3)(1))(6(5))"]}
        self.fail_phrase = 'nah bro idk about it'
        mongo.create_user( self.user )

    def test_delete_graphcorrect(self):
        """ The user graph was deleted in the database """
        deleted_user = mongo.delete_user_game_graph( self.user["user_id"], self.user['save_games'][0]["game_id"] )

        self.assertEqual( deleted_user, 1, msg=f'{BColors.FAIL}\t[-]\tDatabase was not able to delete the graph!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database graph delete.{BColors.ENDC}")

    def test_delete_nonexist(self):
        """ The user graph should not be deleted from the database """
        deleted_user = mongo.delete_user_game_graph( "This name should really not exist in the database, and if it does, it desrves to be deleted", self.user['save_games'][0]["game_id"] )

        self.assertEqual( deleted_user, self.fail_phrase, msg=f'{BColors.FAIL}\t[-]\tIncorrect return for non-existant user!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database delete graph nonexistant.{BColors.ENDC}")

class DBList(TestCase):
    def setUp(self):
        self.user = {"user_id":"5f7d1b1d8fd2b816c48c148b","badges":[31,24,83],"current_story_level":9,"email":"ryanb777@umbc.edu","friends":["Kulsoom2","Nick2","Maksim2","Naomi2"],"user_name":"ryan2","password_hash":"well,hello there","points":98274,"rank":"diamond","save_games":[{'game_id': '60afce36-085a-11eb-b6ab-acde48001122', 'graph': {'nodes': 'DID IT WRETITREE ???5))'}, 'player_ids': ['id2', 'id3', 'id4', 'id5'], 'player_names': ['naomi', 'kulsoom', 'nick', 'ryan'], 'player_points': {'id2': 2, 'id3': 2, 'id4': 3, 'id5': 10}, 'turn': 'id2', 'cards': {'id2': ['card1', 'card2', 'card3'], 'id3': ['card1', 'card2', 'card3'], 'id4': ['card1', 'card2', 'card3'], 'id5': ['card1', 'card2', 'card3']}, 'gold_node': False, 'difficulty': 'Medium', 'num_players': 4, 'online': True, 'curr_data_structure': 'AVL', 'selected_data_structures': ['AVL', 'Stack'], 'timed_game': False, 'seconds_until_next_ds': 60, 'time_created': '07/10/2020 00:05:47', 'end_game': False},"4(2(3)(1))(6(5))","4(2(3)(1))(6(5))"]}
        mongo.create_user( self.user )

    def test_list_users_correct(self):
        """ The user document was added to the list and appears in the returned list """
        found = False
        game_cursor = mongo.list_users()
        for gameid in game_cursor:
            if self.user["user_id"] == gameid["user_id"]:
                found = True

        self.assertEqual( found, True, msg=f'{BColors.FAIL}\t[-]\tAdded user was not in the listed games!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database list.{BColors.ENDC}")

    def test_list_user_games_correct(self):
        user_games = mongo.list_user_games(self.user["user_id"])

        self.assertEqual(user_games[0], self.user["save_games"][0], msg=f'{BColors.FAIL}\t[-]\tAdded user was not in the listed games!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database list.{BColors.ENDC}")

    def tearDown(self):
        mongo.remove_user(self.user["user_id"])

class DBReadUserGamesAndGraphs(TestCase):
    def setUp(self):
        self.user = {"user_id":"5f7d1b1d8fd2b816c48c148b","badges":[31,24,83],"current_story_level":9,"email":"ryanb777@umbc.edu","friends":["Kulsoom2","Nick2","Maksim2","Naomi2"],"user_name":"ryan2","password_hash":"well,hello there","points":98274,"rank":"diamond","save_games":[{'game_id': '60afce36-085a-11eb-b6ab-acde48001122', 'graph': {'nodes': 'DID IT WRETITREE ???5))'}, 'player_ids': ['id2', 'id3', 'id4', 'id5'], 'player_names': ['naomi', 'kulsoom', 'nick', 'ryan'], 'player_points': {'id2': 2, 'id3': 2, 'id4': 3, 'id5': 10}, 'turn': 'id2', 'cards': {'id2': ['card1', 'card2', 'card3'], 'id3': ['card1', 'card2', 'card3'], 'id4': ['card1', 'card2', 'card3'], 'id5': ['card1', 'card2', 'card3']}, 'gold_node': False, 'difficulty': 'Medium', 'num_players': 4, 'online': True, 'curr_data_structure': 'AVL', 'selected_data_structures': ['AVL', 'Stack'], 'timed_game': False, 'seconds_until_next_ds': 60, 'time_created': '07/10/2020 00:05:47', 'end_game': False},"4(2(3)(1))(6(5))","4(2(3)(1))(6(5))"]}
        self.fail_phrase = 'nah bro idk about it'
        mongo.create_user( self.user )

    def test_find_user_game(self):
        """ The user game document was found """
        found = False
        user_game = mongo.find_user_game(self.user["user_id"], self.user['save_games'][0]["game_id"])

        self.assertEqual( user_game, self.user["save_games"][0], msg=f'{BColors.FAIL}\t[-]\tUser game save was not found!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database find game.{BColors.ENDC}")

    def test_share_user_game(self):
        """ The user game was shared """
        user_share_game = mongo.find_user_game(self.user["user_id"], self.user['save_games'][0]["game_id"])

        self.assertEqual( user_share_game, self.user["save_games"][0], msg=f'{BColors.FAIL}\t[-]\tUser game save was not found!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database share game.{BColors.ENDC}")

    def test_find_user_game_graph(self):
        """ The user graph was found """

        user_graph = mongo.find_user_game_graph(self.user["user_id"], self.user['save_games'][0]["game_id"])

        self.assertEqual(user_graph, self.user["save_games"][0]["graph"], msg=f'{BColors.FAIL}\t[-]\tUser graph was not in the listed games!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database share graph.{BColors.ENDC}")

    def test_share_user_game_graph(self):
        """ The user graph was shared """
        share_user_graph = mongo.share_user_graph(self.user["user_id"], self.user['save_games'][0]["game_id"])

        self.assertEqual(share_user_graph, self.user['save_games'][0]["graph"], msg=f'{BColors.FAIL}\t[-]\tUser graph was not in the listed games!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database share graph.{BColors.ENDC}")

    def tearDown(self):
        mongo.remove_user(self.user["user_id"])
