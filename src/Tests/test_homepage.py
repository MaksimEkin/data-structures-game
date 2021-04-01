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


        self.driver.close()

    def test_node_contents(self):

        """Tests the node contents."""
        
        # check if all nodes exist
        for node in self.ids:
            self.assertIn(node, list(self.check.keys()))

        # check if point in the node match to what is expected
        for ii, node in enumerate(self.ids):
            self.assertEqual(self.check[node], self.points[ii])
