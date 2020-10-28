"""
Run: python manage.py test game_board.api.tests_api
Reference: https://www.django-rest-framework.org/api-guide/testing/
"""

from django.test import TestCase
from rest_framework.test import APIClient
from game_board import config
from game_board.database import game_board_db as db
from time import sleep
import random
import string
import json


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


class APIOverview(TestCase):
    def test_index_loads_properly(self):
        """The index page loads properly"""

        response = self.client.get('')
        self.assertEqual(response.status_code, 200, msg=f'{BColors.FAIL}\t[-]\tResponse was not 200!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass return code api_overview.{BColors.ENDC}")


class StartGame(TestCase):
    def test_invalid_api_request(self):
        """Invalid API request fields"""

        # Test non existing difficulty level
        response = self.client.get('/game_board/api/start_game/Super Easy/ID1/AVL')

        self.assertEqual(response.status_code, 400, msg=f'{BColors.FAIL}\t[-]\tResponse was not 200!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass returning the correct response code.{BColors.ENDC}")

        self.assertEqual(response.data, {'error': 'Difficulty level not found!',
                                         'options': config.DIFFICULTY_LEVELS},
                         msg=f'{BColors.FAIL}\t[-]\tInvalid difficulty level got accepted!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass not accepting invalid difficulty level.{BColors.ENDC}")

    def test_start_game(self):
        """Tests starting new games"""
        random.seed(42)
        fail = False

        print(f"{BColors.OKBLUE}\t[i]\tStarting 20 games and ending them...{BColors.ENDC}")
        for ii in range(20):
            try:
                # Create players
                difficulty = random.choice(config.DIFFICULTY_LEVELS)
                players = list()
                num_players = random.randint(1, 4)
                for num in range(num_players):
                    name = random.choice(string.ascii_letters)
                    players.append("ID" + str(name))
                players = ','.join(players)

                # Start a new game
                url = "/game_board/api/start_game/" + difficulty + '/' + players + '/AVL'
                response = self.client.get(url)

                self.assertEqual(response.status_code, 200, msg=f'{BColors.FAIL}\t[-]\tResponse was not 200!{BColors.ENDC}')
                self.assertIn('game_id', response.data.keys(), msg=f'{BColors.FAIL}\t[-]\tGame ID was not returned!{BColors.ENDC}')

                # Remove the test game from the database
                sleep(0.2)
                db.remove_game(response.data['game_id'])

            except Exception as e:
                print(f"{BColors.FAIL}\t[-]\tFail creating games: {BColors.ENDC}", str(e))
                fail = True
        if fail == False:
            print(f"{BColors.OKGREEN}\t[+]\tPass generating games.{BColors.ENDC}")

    def test_game_board_state(self):
        """Tests if the game configured as requested"""

        # create a new game
        created_game = self.client.get('/game_board/api/start_game/Easy/ID1,ID2/AVL')
        # load the game
        response = self.client.get('/game_board/api/board/' + str(created_game.data['game_id']))

        board = response.data
        self.assertEqual(board['difficulty'], 'Easy', msg=f'{BColors.FAIL}\t[-]\tDifficulty does not match!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass choosing the difficulty level.{BColors.ENDC}")

        self.assertEqual(board['curr_data_structure'], 'AVL', msg=f'{BColors.FAIL}\t[-]\tCurrent data structure is invalid!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass setting the data structure.{BColors.ENDC}")

        self.assertIn(board['turn'], ['ID1', 'ID2'], msg=f'{BColors.FAIL}\t[-]\tTurn is assigned to a non existing user!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass choosing the player turn.{BColors.ENDC}")

        self.assertEqual(board['player_ids'], ['ID1', 'ID2'], msg=f'{BColors.FAIL}\t[-]\tIncorrect user ID(s)!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass choosing user IDs.{BColors.ENDC}")

        self.assertIsNot(board['graph']['gold_node'], board['graph']['root_node'],
                         msg=f'{BColors.FAIL}\t[-]\tGolden node and root node are same!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass choosing the nodes so that golden node is not at the root.{BColors.ENDC}")

        self.assertEqual(board['graph']['balanced'], True, msg=f'{BColors.FAIL}\t[-]\tInitial tree is unbalanced!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass balancing the initial tree.{BColors.ENDC}")

        # remove the created game
        sleep(0.2)
        db.remove_game(created_game.data['game_id'])


class Action(TestCase):
    def test_invalid_card(self):
        """Test if API will accept playing an invalid action"""

        # create a new game
        created_game = self.client.get('/game_board/api/start_game/Easy/ID1,ID2/AVL')

        # play invalid card
        response = self.client.get('/game_board/api/action/Insert -1/' + str(created_game.data['game_id']))
        self.assertEqual(response.data, {'invalid_action': 'Player does not have the card Insert -1!'},
                         msg=f'{BColors.FAIL}\t[-]\tAllowed playing an invalid card!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass attempting to play an invalid card.{BColors.ENDC}")

        # attempt to balance a balanced tree
        post_data = json.dumps({'adjacency_list': 'test'})
        response = self.client.post('/game_board/api/rebalance/' + str(created_game.data['game_id']),
                                    post_data, content_type='application/json')
        self.assertEqual(response.data, {'invalid_action': 'Tree is already balanced!'},
                         msg=f'{BColors.FAIL}\t[-]\tTree is already balanced!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass attempting to balance an already balanced tree.{BColors.ENDC}")

        # remove the created game
        sleep(0.2)
        db.remove_game(created_game.data['game_id'])


class Rebalance(TestCase):
    def test_invalid_rebalance(self):
        """Test if API will accept playing an invalid action"""

        # create a new game
        created_game = self.client.get('/game_board/api/start_game/Easy/ID1,ID2/AVL')

        # attempt to balance a balanced tree
        post_data = json.dumps({'adjacency_list': 'test'})
        response = self.client.post('/game_board/api/rebalance/' + str(created_game.data['game_id']),
                                    post_data, content_type='application/json')
        self.assertEqual(response.data, {'invalid_action': 'Tree is already balanced!'},
                         msg=f'{BColors.FAIL}\t[-]\tTree is already balanced!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass attempting to balance an already balanced tree.{BColors.ENDC}")

        # remove the created game
        sleep(0.2)
        db.remove_game(created_game.data['game_id'])
        
        
class PlayGame(TestCase):
    def setUp(self):
        # create a new game
        self.game = self.client.get('/game_board/api/start_game/Easy/ID1,ID2,ID3/AVL').data

    def tearDown(self):
        # remove the created game
        db.remove_game(self.game['game_id'])

    def test_game_simulation(self):
        """Simulates a simple game for 50 rounds max or until the game ends to test the game play"""
        print(f"{BColors.OKBLUE}\t[i]\tSimulating a simple game play (max 50 rounds)...{BColors.ENDC}")
        game_ended = False

        for ii in range(50):
            sleep(0.5)
            board = self.client.get('/game_board/api/board/' + str(self.game['game_id'])).data

            # tree is balanced, play a card
            if board['graph']['balanced']:
                picked_card = random.choice(board['cards'][board['turn']])
                response = self.client.get('/game_board/api/action/' + picked_card + '/' + str(self.game['game_id'])).data

                # game ended
                if response['end_game']:
                    print(f"{BColors.OKCYAN}\t[+]\tPass simulating a game. Game ended.{BColors.ENDC}")
                    game_ended = True

                    self.assertEqual(response['graph']['gold_node'], response['graph']['root_node'],
                                     msg=f'{BColors.FAIL}\t[-]\tGolden node was not at root when game ended!{BColors.ENDC}')

                    self.assertEqual(response['turn'], board['turn'],
                                     msg=f'{BColors.FAIL}\t[-]\tWrong winner!{BColors.ENDC}')
                    break

                # delete node action
                if "Delete" in picked_card:
                    deleted_node = picked_card.split(' ')[1]
                    self.assertNotIn(deleted_node, response['graph']['node_points'].keys(),
                                     msg=f'{BColors.FAIL}\t[-]\tDeleted node was still in the tree!{BColors.ENDC}')

                # insert node action
                elif "Insert" in picked_card:
                    new_node = response['graph']['node_points'].keys() - board['graph']['node_points'].keys()
                    self.assertEqual(response['graph']['node_points']["".join(new_node)], int(picked_card.split(' ')[1]),
                                     msg=f'{BColors.FAIL}\t[-]\tFailed inserting node!{BColors.ENDC}')

            # balance tree action
            else:
                post_data = json.dumps({'adjacency_list': 'test'})
                response = self.client.post('/game_board/api/rebalance/' + str(self.game['game_id']),
                                            post_data, content_type='application/json').data

                self.assertEqual(response['graph']['balanced'], True,
                                 msg=f'{BColors.FAIL}\t[-]\tFailed balancing the tree!{BColors.ENDC}')

                # game ended
                if response['end_game']:
                    print(f"{BColors.OKCYAN}\t[+]\tPass simulating a game. Game ended.{BColors.ENDC}")
                    game_ended = True

                    self.assertEqual(response['graph']['gold_node'], response['graph']['root_node'],
                                     msg=f'{BColors.FAIL}\t[-]\tGolden node was not at root when game ended!{BColors.ENDC}')

                    self.assertEqual(response['turn'], board['turn'],
                                     msg=f'{BColors.FAIL}\t[-]\tWrong winner!{BColors.ENDC}')

                    break

        if game_ended == False:
            print(f"{BColors.OKGREEN}\t[+]\tPass simulating a game. Reach max iterations.{BColors.ENDC}")
