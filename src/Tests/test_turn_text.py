"""
This script is a unit test that uses Selenium to verify
the content of the visual in Gameboard that displays
whose turn it is and how many points that user have,
as well as all other displayed users and their cards.
This test also verifies the deck size.

To run this test, make the below changes first:
    1- Safari --> Allow Remote Automation
    2- Change the remote url variable to local in GameBoard.js
    3- npm run build

How to run:
    1) Run Django: python manage.py runserver
    2) Run the test: python -m unittest test_player_display_text.py
"""
import json
import requests
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from time import sleep


class TestStringMethods(unittest.TestCase):
    """Tests contents of the nodes in front-end."""

    def setUp(self):
        """Setup the test"""
        # Web Browser Instance
        self.driver = webdriver.Safari()
        self.driver.get("http://127.0.0.1:8000/")

        # Setup game players
        player_list = self.driver.find_element_by_name('playerList')
        player_list.click()
        player_list.send_keys(Keys.COMMAND + "a")
        player_list.send_keys(Keys.DELETE)
        player_list.send_keys("ID1,ID2")

        # Choose difficulty
        difficulty_levels = Select(self.driver.find_element_by_name('level'))
        difficulty_levels.select_by_visible_text('Easy')

        # Start Game
        self.driver.find_element_by_name('start_game').click()

        # Let game load
        sleep(5)

        # Collect the displayed player information
        players_obj = self.driver.find_elements_by_name("player_name_display")
        player_points_obj = self.driver.find_elements_by_name("player_points_display")
        player_cards_obj = self.driver.find_elements_by_name("player_cards_display")
        deck_size_obj = self.driver.find_element_by_id("deck_size_display")

        # extract text
        self.players = list()
        self.points = list()
        self.cards = list()
        self.turn = ''
        self.deck_size = deck_size_obj.text.split(':')[1].strip()

        for index, instance in enumerate(players_obj):

            if '*' in instance.text:
                self.turn = instance.text.replace('*', '').strip()

            self.players.append(instance.text.replace('*', '').strip())
            self.points.append(player_points_obj[index].text.strip())
            self.cards.append(player_cards_obj[index].text.split('-'))

        # Get cookies
        cookies = self.driver.get_cookies()
        game_id = ""
        for cookie in cookies:
            if cookie['name'] == 'game_id':
                game_id = cookie['value']

        # Pull the expected game from API
        url = 'http://127.0.0.1:8000/game_board/api/board/' + game_id
        response = requests.get(url)
        board = json.loads(response.text)
        self.check_turn = board['turn']
        self.check_points = board['player_points']
        self.check_cards = board['cards']
        self.check_deck_size = len(board['deck'])

        # End the test. Closes the browser.
        self.driver.close()

    def test_turn(self):
        """Tests if the displayed turn is correct."""
        self.assertEqual(self.check_turn, self.turn)

    def test_points_players(self):
        """Tests if the displayed players and their points are correct."""

        for index, player in enumerate(self.players):
            self.assertEqual(self.check_points[player], int(self.points[index]))

    def test_deck_size(self):
        """Tests if the displayed deck size is correct."""
        self.assertEqual(self.check_deck_size, int(self.deck_size))

    def test_cards(self):
        """Tests if the displayed cards match the expected."""

        for index, cards in enumerate(self.cards):
            player = self.players[index]

            for cc in cards:
                cc = cc.strip()
                self.assertIn(cc, self.check_cards[player])
