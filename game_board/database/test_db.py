"""
python manage.py test game_board.database.test_db
"""

from django.test import TestCase
from game_board.database import game_board_db as mongo
import datetime as dt

class BColors:
    """ Main test colors """

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

class DBCreate(TestCase):
    """ Main test for board create """
    def setUp(self):
        """ creates game data needed for tests """

        self.board = {"game_id": "60afce36-085a-11eb-b6ab-acde48001122",
        "graph": {"nodes": "node4(node2(node3)(node1))(node6(node5))",
        "node_points": {"node1": 1,"node2": 2,"node3": 3,"node4": 4,"node5": 5,"node6": 6},
        "gold_node": "node5","balanced": True},"player_ids": ["id2","id3","id4","id5"],
        "player_names": ["naomi","kulsoom","nick","ryan"],
        "player_points": {"id2": 2,"id3": 2,"id4": 3,"id5": 10},"turn": "id2",
        "cards": {"id2": ["card1","card2","card3"],"id3": ["card1","card2","card3"],
        "id4":["card1","card2","card3"],"id5": ["card1","card2","card3"]},
        "gold_node": False,"difficulty": "Medium","num_players": 4,"online": True,
        "curr_data_structure": "AVL","selected_data_structures": ["AVL","Stack"],
        "timed_game": False,"seconds_until_next_ds": 60,"time_created": "07/10/2020 00:05:47",
        "end_game": False}

        self.fail_phrase = 'nah bro idk about it'

        #Make sure the game is cleared out
        mongo.remove_game(self.board["game_id"])

    def test_create(self):
        """ The gamboard document was created in the database """
        created_game = mongo.create_game( self.board )

        self.assertEqual( created_game, "60afce36-085a-11eb-b6ab-acde48001122",
            msg=f'{BColors.FAIL}\t[-]\tGame was not created in the Database!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass gameboard database save.{BColors.ENDC}")

    def test_duplicatecreate(self):
        """ The document is a duplicate and should fail creation in the database """
        created_game = mongo.create_game( self.board )
        created_game = mongo.create_game( self.board )

        self.assertEqual( created_game, self.fail_phrase,
            msg=f'{BColors.FAIL}\t[-]\tGame was not created in the Database!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass gameboard database save duplicate.{BColors.ENDC}")

    def tearDown(self):
        """ Removes game data needed in tests """
        mongo.remove_game(self.board["game_id"])

class DBRead(TestCase):
    """ Main test for board read """
    def setUp(self):
        """ creates game data needed for tests """

        self.board = {"game_id": "60afce36-085a-11eb-b6ab-acde48001122",
        "graph": {"nodes": "node4(node2(node3)(node1))(node6(node5))",
        "node_points": {"node1": 1,"node2": 2,"node3": 3,"node4": 4,"node5": 5,"node6": 6},
        "gold_node": "node5","balanced": True},"player_ids": ["id2","id3","id4","id5"],
        "player_names": ["naomi","kulsoom","nick","ryan"],
        "player_points": {"id2": 2,"id3": 2,"id4": 3,"id5": 10},"turn": "id2",
        "cards": {"id2": ["card1","card2","card3"],"id3": ["card1","card2","card3"],
        "id4":["card1","card2","card3"],"id5": ["card1","card2","card3"]},
        "gold_node": False,"difficulty": "Medium","num_players": 4,"online": True,
        "curr_data_structure": "AVL","selected_data_structures": ["AVL","Stack"],
        "timed_game": False,"seconds_until_next_ds": 60,"time_created": "07/10/2020 00:05:47",
        "end_game": False}

        self.fail_phrase = 'nah bro idk about it'

        mongo.create_game( self.board )

    def test_read_correct(self):
        """ The document was read from the database """
        read_game = mongo.read_game( "60afce36-085a-11eb-b6ab-acde48001122" )

        self.assertEqual( read_game["game_id"], self.board["game_id"],
            msg=f'{BColors.FAIL}\t[-]\tGame Id returned from read board does not equal expected!\
            {BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass gameboard database read.{BColors.ENDC}")

    def test_read_nonexist(self):
        """ The document should not be read from the database """
        read_game = mongo.read_game(
            "This name should really not exist in the database, and if it does, YEESH!" )

        self.assertEqual( read_game, self.fail_phrase,
            msg=f'{BColors.FAIL}\t[-]\tIncorrect return for non-existant game!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass gameboard database read nonexistant.{BColors.ENDC}")

    def tearDown(self):
        """ Removes game data needed in tests """
        mongo.remove_game(self.board["game_id"])

class DBUpdate(TestCase):
    """ Main test for board read """
    def setUp(self):
        """ creates game data needed for tests """

        self.board = {"game_id": "60afce36-085a-11eb-b6ab-acde48001122",
        "graph": {"nodes": "node4(node2(node3)(node1))(node6(node5))",
        "node_points": {"node1": 1,"node2": 2,"node3": 3,"node4": 4,"node5": 5,"node6": 6},
        "gold_node": "node5","balanced": True},"player_ids": ["id2","id3","id4","id5"],
        "player_names": ["naomi","kulsoom","nick","ryan"],
        "player_points": {"id2": 2,"id3": 2,"id4": 3,"id5": 10},"turn": "id2",
        "cards": {"id2": ["card1","card2","card3"],"id3": ["card1","card2","card3"],
        "id4":["card1","card2","card3"],"id5": ["card1","card2","card3"]},
        "gold_node": False,"difficulty": "Medium","num_players": 4,"online": True,
        "curr_data_structure": "AVL","selected_data_structures": ["AVL","Stack"],
        "timed_game": False,"seconds_until_next_ds": 60,"time_created": "07/10/2020 00:05:47",
        "end_game": False}

        self.board2 = {"game_id": "60afce36-085a-11eb-b6ab-acde48001122",
        "graph": {"nodes": "node4(node2(node3)(node1))(node6(node5))",
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

        self.fail_phrase = 'nah bro idk about it'

        mongo.create_game( self.board )

    def test_update_correct(self):
        """ The document is updated in the database """
        updated_game = mongo.update_game( self.board["game_id"], self.board2 )

        self.assertEqual( updated_game["game_id"], self.board2["game_id"],
            msg=f'{BColors.FAIL}\t[-]\tGame Id returned from read board does not equal expected!\
            {BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass gameboard database update.{BColors.ENDC}")

    def test_update_nonexist(self):
        """ The document should not be updated from the database """
        updated_game = mongo.update_game(
            "This name should not exist in the database, and if it does, YEESH!", self.board )

        self.assertEqual( updated_game, self.fail_phrase,
            msg=f'{BColors.FAIL}\t[-]\tIncorrect return for non-existant game!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass gameboard database update nonexistant.{BColors.ENDC}")

    def tearDown(self):
        """ Removes game data needed in tests """
        mongo.remove_game(self.board2["game_id"])

class DBDelete(TestCase):
    """ Main test for board delete """
    def setUp(self):
        """ creates game data needed for tests """

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
        "seconds_until_next_ds": 60,"time_created": "07/10/2020 00:05:47","end_game": False}

        self.fail_phrase = 'nah bro idk about it'

        mongo.create_game( self.board )

    def test_delete_correct(self):
        """ The document was deleted in the database """
        deleted_game = mongo.remove_game( "60afce36-085a-11eb-b6ab-acde48001122" )

        self.assertEqual( deleted_game, 1,
            msg=f'{BColors.FAIL}\t[-]\tDatabase was not able to delete the game!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass gameboard database delete.{BColors.ENDC}")

    def test_delete_nonexist(self):
        """ The document should not be deleted from the database """
        deleted_game = mongo.remove_game(
            "This name should'nt exist in the database, and if it does, it deserves to be deleted" )

        self.assertEqual( deleted_game, self.fail_phrase,
            msg=f'{BColors.FAIL}\t[-]\tIncorrect return for non-existant game!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass gameboard database delete nonexistant.{BColors.ENDC}")

class DBList(TestCase):
    """ Main test for board list """
    def setUp(self):
        """ creates game data needed for tests """

        self.board = {"game_id": "60afce36-085a-11eb-b6ab-acde48001122",
        "graph": {"nodes": "node4(node2(node3)(node1))(node6(node5))",
        "node_points": {"node1": 1,"node2": 2,"node3": 3,"node4": 4,"node5": 5,"node6": 6},
        "gold_node": "node5","balanced": True},"player_ids": ["id2","id3","id4","id5"],
        "player_names": ["naomi","kulsoom","nick","ryan"],
        "player_points": {"id2": 2,"id3": 2,"id4": 3,"id5": 10},"turn": "id2",
        "cards": {"id2": ["card1","card2","card3"],"id3": ["card1","card2","card3"],
        "id4":["card1","card2","card3"],"id5": ["card1","card2","card3"]},
        "gold_node": False,"difficulty": "Medium","num_players": 4,"online": True,
        "curr_data_structure": "AVL","selected_data_structures": ["AVL","Stack"],
        "timed_game": False,"seconds_until_next_ds": 60,"time_created": "07/10/2020 00:05:47",
        "end_game": False}

        self.fail_phrase = 'nah bro idk about it'

        mongo.create_game( self.board )

    def test_list_correct(self):
        """ The document was added to the list and appears in the returned list """
        found = False
        game_cursor = mongo.list_games()
        for gameid in game_cursor:
            if self.board["game_id"] == gameid["game_id"]:
                found = True

        self.assertEqual( found, True,
            msg=f'{BColors.FAIL}\t[-]\tAdded game was not in the listed games!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass gameboard database list.{BColors.ENDC}")

    def tearDown(self):
        """ Removes game data needed in tests """
        mongo.remove_game(self.board["game_id"])


class DBRemoveOldGames(TestCase):
    """ Main test for removing old games from the database list """
    def setUp(self):
        """ creates game data needed for tests """

        self.board = {"game_id": "oh look a new id, how novel",
        "graph": {"nodes": "node4(node2(node3)(node1))(node6(node5))",
        "node_points": {"node1": 1,"node2": 2,"node3": 3,"node4": 4,"node5": 5,"node6": 6},
        "gold_node": "node5","balanced": True},"player_ids": ["id2","id3","id4","id5"],
        "player_names": ["naomi","kulsoom","nick","ryan"],
        "player_points": {"id2": 2,"id3": 2,"id4": 3,"id5": 10},"turn": "id2",
        "cards": {"id2": ["card1","card2","card3"],"id3": ["card1","card2","card3"],
        "id4":["card1","card2","card3"],"id5": ["card1","card2","card3"]},
        "gold_node": False,"difficulty": "Medium","num_players": 4,"online": True,
        "curr_data_structure": "AVL","selected_data_structures": ["AVL","Stack"],
        "timed_game": False,"seconds_until_next_ds": 60,"time_created": "07/10/2020 00:05:47",
        "end_game": False}
        self.board2 = {"game_id": "i changed the id again",
        "graph": {"nodes": "node4(node2(node3)(node1))(node6(node5))",
        "node_points": {"node1": 1,"node2": 2,"node3": 3,"node4": 4,"node5": 5,"node6": 6},
        "gold_node": "node5","balanced": True},"player_ids": ["id2","id3","id4","id5"],
        "player_names": ["naomi","kulsoom","nick","ryan"],
        "player_points": {"id2": 2,"id3": 2,"id4": 3,"id5": 10},"turn": "id2",
        "cards": {"id2": ["card1","card2","card3"],"id3": ["card1","card2","card3"],
        "id4":["card1","card2","card3"],"id5": ["card1","card2","card3"]},
        "gold_node": False,"difficulty": "Medium","num_players": 4,"online": True,
        "curr_data_structure": "AVL","selected_data_structures": ["AVL","Stack"],
        "timed_game": False,"seconds_until_next_ds": 60,
        "time_created": dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "end_game": False}
        self.fail_phrase = 'nah bro idk about it'

        mongo.create_game( self.board )
        mongo.create_game( self.board2 )

    def test_remove_old_games(self):
        """ The old document was successfully deleted """

        mongo.purge_old_games()
        read_game = mongo.read_game( self.board["game_id"] )

        self.assertEqual( read_game, self.fail_phrase,
            msg=f'{BColors.FAIL}\t[-]\tStill found old game after purge!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass gameboard database purge old games.{BColors.ENDC}")

    def test_purge_new_games(self):
        """ The new document was successfully retained """
        mongo.purge_old_games()
        read_game = mongo.read_game( self.board2["game_id"] )

        self.assertEqual( read_game, self.board2,
            msg=f'{BColors.FAIL}\t[-]\t New game not found after purge!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass gameboard database purge, new game remains.{BColors.ENDC}")

    def tearDown(self):
        """ Removes game data needed in tests """
        mongo.remove_game(self.board["game_id"])

        # Called in case purge fails
        mongo.remove_game(self.board2["game_id"])
