"""
This script is a unit test that uses Selenium to verify
the content of the choices that displays on the homepage.
It checks that the cookies set with the choices the user selected
are correctly passed to game_board page.


To run this test, make the below changes first:
    1- Safari --> Allow Remote Automation
    2- Change the remote url variable to local in GameBoard.js
    3- npm run build

How to run:
    1) Run Django: python manage.py runserver
    2) Run the test: python -m unittest test_homepage.py
"""
import json
import unittest
from time import sleep
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By



class TestStringMethods(unittest.TestCase):
    """Tests contents of the choices on homepage in front-end."""

    def TestHomepage(self):
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

        # Choose DS game
        #DSgame_selection = Select(self.driver.find_element_by_name('DSgame'))
        #DSgame_selection .select_by_visible_text('LLIST')

        # Start Game
        self.driver.find_element_by_name('start_game').click()

        # Let game load
        sleep(5)

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

        # End tests, closes the browser
        self.driver.close()

