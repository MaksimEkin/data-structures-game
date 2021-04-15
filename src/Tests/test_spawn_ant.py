"""
This script will be a simple test that tests the ant spawning actions render correctly.

To run this test, make the below changes first:
    1- Safari --> Allow Remote Automation
    2- Change the remote url variable to local in LListGameboard.js
    3- npm run build

How to run:
    1) Run Django: python manage.py runserver
    2) Run the test: python -m unittest test_spawn_ant.py
"""
import unittest
import requests
from selenium import webdriver 
from time import sleep

class TestStringMethods(unittest.TestCase):

    def setUp(self):
        """setup the test"""
        # Web browser instance
        self.driver = webdriver.Safari()
#       self.driver.get("http://127.0.0.1:8000/game_board/llist_api")
        self.driver.get("http://127.0.0.1:3000/game_board/llist_api")


    def test_spawn_elements(self):
        
        # get cookies, check that initial state of spawningAnt is false
        cookies = self.driver.get_cookies()
        spawning = ""
        for cookie in cookies:
            if cookie['name'] == 'spawningAnt':
                spawning = cookie['value']

        self.assertFalse(spawning)

        sleep(2)

        # click on queen ant and check that spawningAnt changes to true
        #queen_ant = self.driver.find_element_by_xpath("/div/span/button/img")
        queen_ant = self.driver.find_element_by_id('queenAnt')
        queen_ant.click()
        sleep(2)
        
        # when queen is clicked, spawningAnt is true, egg should appear on screen, find egg
        ant_egg = self.driver.find_element_by_id('egg')

        # This should work after frontend and backend are connected
        """
        cookies = self.driver.get_cookies()
        spawningAfterClick = ""
        for cookie in cookies:
            if cookie['name'] == 'spawningAnt':
                spawningAfterClick = cookie['value']

        sleep(2)
        self.assertTrue(spawningAfterClick)
        """
    
    



    def tearDown(self):
        self.driver.close()

if __name__ == '__main__':
    unittest.main()