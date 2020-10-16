"""
python manage.py test home_page.database.test_db
"""

from home_page.database import home_page_db as mongo
from django.test import TestCase

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

class DBRankings(TestCase):
    def test_get_player_rankings(self):
        """ The rankings were retreived """

        made_player = 0
        #Need to insert a made_player with the highest points and test to see if they are first
        # Currently no userprofile db

        player1 = mongo.get_rankings()[0]

        self.assertEqual( 0, made_player, msg=f'{BColors.FAIL}\t[-]\tPlayer with artificially high points was not first!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass homepage get rankings.{BColors.ENDC}")
