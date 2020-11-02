"""
python manage.py test home_page.database.test_db
"""

from django.test import TestCase
from home_page.database import home_page_db as mongo
from profile_page.database import profile_page_db as mongo2

class BColors:
    """ Testing colors for prints """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class DBRankings( TestCase ):
    """ Test for homepage rankings """

    def setUp( self ):
        """ The data needed for homepage tests  """

        self.user = {"user_id":"5f7d1b1d8fd2b816c48c148b","badges":[31,24,83],
        "current_story_level":9,"email":"ryanb777@umbc.edu",
        "friends":["Kulsoom2","Nick2","Maksim2","Naomi2"],
        "user_name":"ryan2","password_hash":"well,hello there",
        "points":9829999999974,"rank":"diamond",
        "save_games":["4(2(3)(no))(6(5))","4(2(3)(1))(6(5))","4(2(3)(1))(6(5))"]}

        mongo2.save_user( self.user )

    def test_get_player_rankings( self ):
        """ The rankings were retreived """

        players = mongo.get_rankings()
        found = False
        for player in players:
            if self.user["user_id"] == player["user_id"]:
                found = True

        self.assertEqual( found, True,
            msg=f'{BColors.FAIL}\t[-]\tPlayer with artificially high points was not first!\
            {BColors.ENDC}' )
        print( f"{BColors.OKGREEN}\t[+]\tPass homepage get rankings.{BColors.ENDC}" )

    def tearDown( self ):
        """ The data needed for homepage tests is removed -- no residual data """

        mongo2.remove_user(self.user["user_id"])
