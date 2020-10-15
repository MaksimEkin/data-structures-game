from django.test import TestCase
from rest_framework.test import APIClient
from game_board import config
from game_board.database import game_board_db as db
from time import sleep
import random
import string

class RunTests(TestCase):
    def test_index_loads_properly(self):
        """The index page loads properly"""
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_invalid_api_request(self):
        """Invalid API request fields"""

        # Test non existing difficulty level
        response = self.client.get('/game_board/api/start_game/Supper Easy/ID1/AVL')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'error': 'Difficulty level not found!',
                                         'options': config.DIFFICULTY_LEVELS})

    def test_start_game(self):
        """Start new games"""
        random.seed(42)

        print('\nStarting and ending games...')
        for ii in range(20):
            try:
                difficulty = random.choice(config.DIFFICULTY_LEVELS)
                players = list()
                num_players = random.randint(1, 4)
                for num in range(num_players):
                    name = random.choice(string.ascii_letters)
                    players.append("ID"+str(name))

                players = ','.join(players)

                url = "/game_board/api/start_game/" + difficulty + '/' + players + '/AVL'
                response = self.client.get(url)

                self.assertEqual(response.status_code, 200)
                self.assertIn('game_id', response.data.keys())

                db.remove_game(response.data['game_id'])
                sleep(0.1)

            except Exception as e:
                print(str(e))


# ========================================================================
# START TESTS
# ========================================================================
RunTests()