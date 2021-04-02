"""
This script is a unit test that uses Selenium to verify
the content of the nodes in the graph.
More specifically, it checks the node IDs and their
corresponding node points with what is expected using
the Game Board API.

To run this test, make the below changes first:
    1- Safari --> Allow Remote Automation
    2- Change the remote url variable to local in GameBoard.js
    3- npm run build

How to run:
    1) Run Django: python manage.py runserver
    2) Run the test: python -m unittest test_node_text.py
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
    """Tests contents of the nodes in front-end."""

    def setUp(self):
        """Setup the test"""
        # Web Browser Instance
        self.driver = webdriver.Safari()
        


    def test_homepage_elements(self):

        driver= self.driver
        driver.get("http://127.0.0.1:8000/")

        # Setup game players
        player_list = driver.find_element_by_name('playerList')
        player_list.click()
        player_list.send_keys(Keys.COMMAND + "a")
        player_list.send_keys(Keys.DELETE)
        player_list.send_keys("ID1,ID2")

        self.assertEqual(player_list.get_attribute('value'), "ID1,ID2")

        # Choose difficulty
        difficulty_levels = Select(driver.find_element_by_name('level'))
        difficulty_levels.select_by_visible_text('Easy')
        selected_level = difficulty_levels.first_selected_option

        self.assertEqual(selected_level.text, 'Easy')

        # Choose ds game
        dsGame = Select(driver.find_element_by_name('gameDS'))
        dsGame.select_by_visible_text('Linked List Standard')
        selected_dsGame = dsGame.first_selected_option

        self.assertEqual(selected_dsGame.text, 'Linked List Standard')





    def tearDown(self):
        self.driver.close()

    

if __name__ == '__main__':
    unittest.main()