"""
This script will be a simple test that verifies the gamepage
for the linked list game loads correctly.
There is nothing to test on the llist gameboard page currently 

To run this test, make the below changes first:
    1- Safari --> Allow Remote Automation
    2- Change the remote url variable to local in LListGameboard.js
    3- npm run build

How to run:
    1) Run Django: python manage.py runserver
    2) Run the test: python -m unittest test_llist_gameboard.py
"""
import unittest
from selenium import webdriver 
from time import sleep

class TestStringMethods(unittest.TestCase):

    def setUp(self):
        """setup the test"""
        # Web browser instance
        self.driver = webdriver.Safari()
        self.driver.get("http://127.0.0.1:8000/game_board/llist_api")
        


    def tearDown(self):
        self.driver.close()

if __name__ == '__main__':
    unittest.main()
    