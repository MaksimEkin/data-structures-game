"""
Run: python manage.py test
Refrence: https://www.django-rest-framework.org/api-guide/testing/
"""

from django.test import TestCase
from rest_framework.test import APIClient
from game_board import config
from game_board.database import game_board_db as db
from time import sleep
import random
import string
import json

class RunTests(TestCase):
    """
    Tests the Game Board API
    """
    def test_index_loads_properly(self):
        """The index page loads properly"""

        response = self.client.get('')
        self.assertEqual(response.status_code, 200, msg='Response was not 200!')
        print("[+] Pass return code api_overview.")

    def test_invalid_api_request(self):
        """Invalid API request fields"""

        # Test non existing difficulty level
        response = self.client.get('/game_board/api/start_game/Supper Easy/ID1/AVL')

        self.assertEqual(response.status_code, 200, msg='Response was not 200!')
        print("[+] Pass returning the correct response code.")

        self.assertEqual(response.data, {'error': 'Difficulty level not found!',
                                         'options': config.DIFFICULTY_LEVELS},
                                          msg='Invalid difficulty level got accepted!')
        print("[+] Pass not accepting invalid difficulty level.")

    def test_start_game(self):
        """Tests starting new games"""

        random.seed(42)
        fail = False

        for ii in range(20):
            try:
                # Create players
                difficulty = random.choice(config.DIFFICULTY_LEVELS)
                players = list()
                num_players = random.randint(1, 4)
                for num in range(num_players):
                    name = random.choice(string.ascii_letters)
                    players.append("ID"+str(name))
                players = ','.join(players)

                # Start a new game
                url = "/game_board/api/start_game/" + difficulty + '/' + players + '/AVL'
                response = self.client.get(url)

                self.assertEqual(response.status_code, 200, msg='Response was not 200!')
                self.assertIn('game_id', response.data.keys(), msg='Game ID was not returned!')

                # Remove the test game from the database
                sleep(0.2)
                db.remove_game(response.data['game_id'])

            except Exception as e:
                print("[-] Fail creating games: ", str(e))
                fail = True
        if fail == False:
            print("[+] Pass generating games.")

    def test_game_board_state(self):
        """Tests if the game configured as requested"""

        # create a new game
        created_game = self.client.get('/game_board/api/start_game/Easy/ID1,ID2/AVL')
        # load the game
        response = self.client.get('/game_board/api/board/' + str(created_game.data['game_id']))

        board = response.data
        self.assertEqual(board['difficulty'], 'Easy', msg='Difficulty does not match!')
        print("[+] Pass choosing the difficulty level.")

        self.assertEqual(board['curr_data_structure'], 'AVL', msg='Current data structure is invalid!')
        print("[+] Pass setting the data structure.")

        self.assertIn(board['turn'], ['ID1', 'ID2'], msg='Turn is assigned to a non existing user!')
        print("[+] Pass choosing the player turn.")

        self.assertEqual(board['player_ids'], ['ID1', 'ID2'], msg='Incorrect user ID(s)!')
        print("[+] Pass choosing user IDs.")

        self.assertIsNot(board['graph']['gold_node'], board['graph']['root_node'],
                         msg='Golden node and root node are same!')
        print("[+] Pass choosing the nodes so that golden node is not at the root.")

        self.assertEqual(board['graph']['balanced'], True, msg='Initial tree is unbalanced!')
        print("[+] Pass balancing the initial tree.")

        # remove the created game
        sleep(0.2)
        db.remove_game(created_game.data['game_id'])

    def test_invalid_play(self):
        """Test if API will accept playing an invalid action"""

        # create a new game
        created_game = self.client.get('/game_board/api/start_game/Easy/ID1,ID2/AVL')

        # play invalid card
        response = self.client.get('/game_board/api/action/Insert -1/' + str(created_game.data['game_id']))
        self.assertEqual(response.data, {'invalid_action': 'Player does not have the card Insert -1!'},
                         msg='Allowed playing an invalid card!')
        print("[+] Pass attempting to play an invalid card.")

        # attempt to balance a balanced tree
        post_data = json.dumps({'adjacency_list': 'test'})
        response = self.client.post('/game_board/api/rebalance/' + str(created_game.data['game_id']),
                                    post_data, content_type='application/json')
        self.assertEqual(response.data, {'invalid_action': 'Tree is already balanced!'},
                         msg='Tree is already balanced!')
        print("[+] Pass attempting to balance an already balanced tree.")

        # remove the created game
        sleep(0.2)
        db.remove_game(created_game.data['game_id'])

    def test_simple_game_play(self):
        """Tests game play by simulating a simple game"""
        pass

# ========================================================================
# START TESTS
# ========================================================================
RunTests()