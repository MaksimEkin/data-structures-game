"""
python manage.py test profile_page.database.test_db
"""

from profile_page.database import profile_page_db as mongo
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

class DBCreate(TestCase):
    def setUp(self):
        self.user = {"user_id":"5f7d1b1d8fd2b816c48c148b","badges":[31,24,83],"current story level":9,"email":"ryanb777@umbc.edu","friends":["Kulsoom2","Nick2","Maksim2","Naomi2"],"user_name":"ryan2","password hash":"well,hello there","points":98274,"rank":"diamond","save games":["4(2(3)(no))(6(5))","4(2(3)(1))(6(5))","4(2(3)(1))(6(5))"]}
        self.fail_phrase = 'nah bro idk about it'
        mongo.remove_user(self.user["user_id"]) #Make sure the game is cleared out

    def test_create(self):
        """ The user document was created in the database """
        created_user = mongo.create_user( self.user )

        self.assertEqual( created_user, self.user["user_id"], msg=f'{BColors.FAIL}\t[-]\tUser was not created in the Database!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database save.{BColors.ENDC}")

    def test_duplicatecreate(self):
        """ The user document is a duplicate and should fail creation in the database """
        created_user = mongo.create_user( self.user )
        created_user = mongo.create_user( self.user )

        self.assertEqual( created_user, self.fail_phrase, msg=f'{BColors.FAIL}\t[-]\tGame was not created in the Database!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database save duplicate.{BColors.ENDC}")

    def tearDown(self):
        mongo.remove_user(self.user["user_id"])

class DBRead(TestCase):
    def setUp(self):
        self.user = {"user_id":"5f7d1b1d8fd2b816c48c148b","badges":[31,24,83],"current story level":9,"email":"ryanb777@umbc.edu","friends":["Kulsoom2","Nick2","Maksim2","Naomi2"],"user_name":"ryan2","password hash":"well,hello there","points":98274,"rank":"diamond","save games":["4(2(3)(no))(6(5))","4(2(3)(1))(6(5))","4(2(3)(1))(6(5))"]}
        self.fail_phrase = 'nah bro idk about it'
        mongo.create_user( self.user )

    def test_read_correct(self):
        """ The user document was read from the database """
        read_user = mongo.read_one_user( self.user["user_id"] )

        self.assertEqual( read_user["user_id"], self.user["user_id"], msg=f'{BColors.FAIL}\t[-]\tGame Id returned from read board does not equal expected!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database read.{BColors.ENDC}")

    def test_read_nonexist(self):
        """ The user document should not be read from the database """
        read_user = mongo.read_one_user( "This name should really not exist in the database, and if it does, YEESH!" )

        self.assertEqual( read_user, self.fail_phrase, msg=f'{BColors.FAIL}\t[-]\tIncorrect return for non-existant user!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database read nonexistant.{BColors.ENDC}")

    def test_read_user_name(self):
        """ The user's name was read from the database """
        read_user_name = mongo.read_user_name( self.user["user_id"] )

        self.assertEqual( read_user_name["user_name"], self.user["user_name"], msg=f'{BColors.FAIL}\t[-]\tUsername returned from read board does not equal expected!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database read-name.{BColors.ENDC}")

    def test_read_user_name_nonexist(self):
        """ The user-name document should not be read from the database """
        read_user = mongo.read_user_name( "This id should really not exist in the database, and if it does, YEESH!" )

        self.assertEqual( read_user, self.fail_phrase, msg=f'{BColors.FAIL}\t[-]\tIncorrect return for non-existant user id!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database read-name nonexistant.{BColors.ENDC}")

    def tearDown(self):
        mongo.remove_user(self.user["user_id"])

class DBUpdate(TestCase):
    def setUp(self):
        self.user = {"user_id":"5f7d1b1d8fd2b816c48c148b","badges":[31,24,83],"current story level":9,"email":"ryanb777@umbc.edu","friends":["Kulsoom2","Nick2","Maksim2","Naomi2"],"user_name":"ryan2","password hash":"well,hello there","points":98274,"rank":"diamond","save games":["4(2(3)(no))(6(5))","4(2(3)(1))(6(5))","4(2(3)(1))(6(5))"]}
        self.user2 = {"user_id":"5f7d1b1d8fd2b816c48c148b","badges":[989879879831,24,83],"current story level":9,"email":"ryanb777@umbc.edu","friends":["Kulsoom2","Nick2","Maksim2","Naomi2"],"user_name":"ryan2","password hash":"well,hello there","points":98274,"rank":"diamond","save games":["4(2(3)(no))(6(5))","4(2(3)(1))(6(5))","4(2(3)(1))(6(5))"]}
        self.fail_phrase = 'nah bro idk about it'
        mongo.create_user( self.user )

    def test_update_correct(self):
        """ The user document is updated in the database """
        updated_user = mongo.update_user( self.user["user_id"], self.user2 )

        self.assertEqual( updated_user["user_id"], self.user2["user_id"], msg=f'{BColors.FAIL}\t[-]\tUser Id returned from read user does not equal expected!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database update.{BColors.ENDC}")

    def test_update_nonexist(self):
        """ The user document should not be updated from the database """
        updated_user = mongo.update_user( "This name should really not exist in the database, and if it does, YEESH!", self.user )

        self.assertEqual( updated_user, self.fail_phrase, msg=f'{BColors.FAIL}\t[-]\tIncorrect return for non-existant user!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database update nonexistant.{BColors.ENDC}")

    def tearDown(self):
        mongo.remove_user(self.user2["user_id"])

class DBDelete(TestCase):
    def setUp(self):
        self.user = {"user_id":"5f7d1b1d8fd2b816c48c148b","badges":[31,24,83],"current story level":9,"email":"ryanb777@umbc.edu","friends":["Kulsoom2","Nick2","Maksim2","Naomi2"],"user_name":"ryan2","password hash":"well,hello there","points":98274,"rank":"diamond","save games":["4(2(3)(no))(6(5))","4(2(3)(1))(6(5))","4(2(3)(1))(6(5))"]}
        self.fail_phrase = 'nah bro idk about it'
        mongo.create_user( self.user )

    def test_delete_correct(self):
        """ The user document was deleted in the database """
        deleted_user = mongo.remove_user( self.user["user_id"] )

        self.assertEqual( deleted_user, 1, msg=f'{BColors.FAIL}\t[-]\tDatabase was not able to delete the user!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database delete.{BColors.ENDC}")

    def test_delete_nonexist(self):
        """ The user document should not be deleted from the database """
        deleted_user = mongo.remove_user( "This name should really not exist in the database, and if it does, it desrves to be deleted" )

        self.assertEqual( deleted_user, self.fail_phrase, msg=f'{BColors.FAIL}\t[-]\tIncorrect return for non-existant user!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database delete nonexistant.{BColors.ENDC}")

class DBList(TestCase):
    def setUp(self):
        self.user = {"user_id":"5f7d1b1d8fd2b816c48c148b","badges":[31,24,83],"current story level":9,"email":"ryanb777@umbc.edu","friends":["Kulsoom2","Nick2","Maksim2","Naomi2"],"user_name":"ryan2","password hash":"well,hello there","points":98274,"rank":"diamond","save games":["4(2(3)(no))(6(5))","4(2(3)(1))(6(5))","4(2(3)(1))(6(5))"]}
        self.fail_phrase = 'nah bro idk about it'
        mongo.create_user( self.user )

    def test_list_correct(self):
        """ The user document was added to the list and appears in the returned list """
        found = False
        game_cursor = mongo.list_users()
        for gameid in game_cursor:
            if self.user["user_id"] == gameid["user_id"]:
                found = True

        self.assertEqual( found, True, msg=f'{BColors.FAIL}\t[-]\tAdded user was not in the listed games!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass User-Profile database list.{BColors.ENDC}")

    def tearDown(self):
        mongo.remove_user(self.user["user_id"])
