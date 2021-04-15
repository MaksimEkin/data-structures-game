from time import sleep
import random
import string
import json
from django.test import TestCase
from game_board import config
from game_board.database import game_board_db as db
from .. import config


class BColors:
    """Colors for printing"""
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
    """Tests calls related to the overview of the API."""

    def test_index_loads_properly(self):
        """The index page loads properly"""

        response = self.client.get('')
        self.assertEqual(response.status_code, 200, msg=f'{BColors.FAIL}\t[-]\tResponse was not 200!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass return code api_overview.{BColors.ENDC}")


class GameActions(TestCase):
    """Tests the API calls that is related to game actions."""
    """Tests will be expanded upon once create chamber function is implemented"""

    def test_spawn(self):
        # create a new game
        created_game = self.client.get('/game_board/llist_api/start_game/Easy/ID1lltest/LLIST')
        # load the game
        response = self.client.get('/game_board/llist_api/board/' + str(created_game.data['game_id']))
        # call spawn ant function
        response = self.client.get('/game_board/temp-david/spawn_ant/' + str(response.data['game_id']))

        board = response.data

        # make sure there was an error since there isn't enough food
        self.assertEqual(response.status_code, 400, msg=f'{BColors.FAIL}\t[-]\tResponse was not 400!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass returning the correct response code.{BColors.ENDC}")


        # remove the created game
        sleep(0.2)
        db.remove_game(created_game.data['game_id'])

    def test_dig_tunnel(self):
        # create a new game
        created_game = self.client.get('/game_board/llist_api/start_game/Easy/ID1lltest/LLIST')
        # load the game
        response = self.client.get('/game_board/llist_api/board/' + str(created_game.data['game_id']))
        # call spawn ant function
        response = self.client.get('/game_board/temp-david/dig_tunnel/' + str(response.data['game_id']) + '/node1/node2')
        
        board = response.data

        # make sure there was an error because nodes do not exist
        self.assertEqual(response.status_code, 400, msg=f'{BColors.FAIL}\t[-]\tResponse was not 400!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass returning the correct response code.{BColors.ENDC}")

        # remove the created game
        sleep(0.2)
        db.remove_game(created_game.data['game_id'])