"""
This script is a unit test that uses Selenium to verify
the content of the visual in Gameboard that displays
whose turn it is and how many points that user have.

To run this test, make the below changes first:
    1- Safari --> Allow Remote Automation
    2- Change the remote url variable to local in GameBoard.js

How to run:
    1) Run Django: python manage.py runserver
    2) Run the test: python -m unittest test_turn_text.py
"""
import json
import unittest
from time import sleep
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


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

        # Collect turn and points displayed in frontend
        self.turn = self.driver.find_element_by_class_name("turn_display").text
        self.points = int(self.driver.find_element_by_class_name("turn_points_display").text)

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
        self.check_points = board['player_points'][self.check_turn]

        # End the test. Closes the browser.
        self.driver.close()

    def test_turn(self):
        """Tests if the displayed turn is correct."""
        self.assertEqual(self.check_turn, self.turn)

    def test_points(self):
        """Tests if the displayed points is correct."""
        self.assertEqual(self.check_points, self.points)
