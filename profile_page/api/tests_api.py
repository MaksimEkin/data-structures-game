"""
Run: python manage.py test profile_page.api.tests_api
Reference: https://www.django-rest-framework.org/api-guide/testing/
"""
from time import sleep
import uuid
from django.test import TestCase
from game_board.database import game_board_db as game_db
from profile_page.database import profile_page_db as profile_db

class BColors:
    """ "Colors for printing"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class APIOverview(TestCase):
    """Tests calls related to the overview of the API."""

    def test_index_loads_properly(self):
        """The index page loads properly"""
        sleep(1)

        response = self.client.get('')
        self.assertEqual(response.status_code, 200, msg=f'{BColors.FAIL}\t[-]\tResponse was not 200!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass return code api_overview.{BColors.ENDC}")


class Register(TestCase):
    """Tests the API calls that is related to user registration."""

    def setUp(self):
        """Create an account."""
        sleep(1)

        # temporary user name
        self.user_info = str(uuid.uuid1()).split('-')[0]

        post_data = {'user_name':  self.user_info,
                     'password1': 'smith1',
                     'password2': 'smith1',
                     'email':  self.user_info}
        response = self.client.post('/profile_page/api/register', post_data)
        self.assertEqual(response.status_code, 200,
                          msg=f'{BColors.FAIL}\t[-]\tFailed creating an account!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass creating a user.{BColors.ENDC}")

        # Authentication token
        self.token = response.data['token']


    def tearDown(self):
        """Removes the testing user from the database."""
        profile_db.remove_user(self.user_info)


    def test_invalid_api_request(self):
        """Invalid API request fields"""

        post_data = {'user_name': 'john55',
                     'password1': 'smith',
                     'password2': 'smith',
                     'wrong_field': 'test'}
        response = self.client.post('/profile_page/api/register', post_data).data
        self.assertEqual(response['error'], 'Missing required fields!',
                         msg=f'{BColors.FAIL}\t[-]\tAccepted invalid POST request!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass not allowing invalid POST request.{BColors.ENDC}")

    def test_non_matching_password(self):
        """Attempts to register with non-matching password."""

        post_data = {'user_name': 'john55',
                     'password1': 'smith1',
                     'password2': 'smith2',
                     'email': 'test'}

        response = self.client.post('/profile_page/api/register', post_data).data
        self.assertEqual(response['error'], 'Passwords does not match!',
                         msg=f'{BColors.FAIL}\t[-]\tAccepted non-matching password!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass not allowing non-matching password.{BColors.ENDC}")


    def test_duplicate_user(self):
        """Attempts to register an existing user."""

        post_data = {'user_name':  self.user_info,
                     'password1': 'smith1',
                     'password2': 'smith1',
                     'email':  self.user_info + 'a'}

        response = self.client.post('/profile_page/api/register', post_data).data
        self.assertEqual(response['error'], 'Error when creating the account!',
                         msg=f'{BColors.FAIL}\t[-]\tAccepted existing user!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass not allowing existing username.{BColors.ENDC}")

    def test_duplicate_email(self):
        """Attempts to register an existing email."""

        post_data = {'user_name':  self.user_info + 'a',
                     'password1': 'smith1',
                     'password2': 'smith1',
                     'email':  self.user_info}

        response = self.client.post('/profile_page/api/register', post_data).data
        self.assertEqual(response['error'], 'Error when creating the account!',
                         msg=f'{BColors.FAIL}\t[-]\tAccepted existing email!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass not allowing existing email.{BColors.ENDC}")


class Login(TestCase):
    """Tests the API calls that is related to user login."""

    def setUp(self):
        """Create an account."""
        sleep(1)

        # temporary user name
        self.user_info = str(uuid.uuid1()).split('-')[0]

        post_data = {'user_name': self.user_info,
                     'password1': 'pineapple',
                     'password2': 'pineapple',
                     'email': self.user_info}
        response = self.client.post('/profile_page/api/register', post_data)
        self.assertEqual(response.status_code, 200,
                          msg=f'{BColors.FAIL}\t[-]\tFailed creating an account!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass creating a user.{BColors.ENDC}")

        # Authentication token
        self.token = response.data['token']

    def tearDown(self):
        """Removes the testing user from the database."""
        profile_db.remove_user(self.user_info)

    def test_invalid_username(self):
        """Tests logging in with invalid username."""

        post_data = {'user_id': self.user_info + 'a',
                     'password': 'pineapple'}

        response = self.client.post('/profile_page/api/login', post_data)
        self.assertEqual(response.status_code, 401,
                         msg=f'{BColors.FAIL}\t[-]\tLogged in with wrong username!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass not allowing incorrect username.{BColors.ENDC}")

    def test_invalid_password(self):
        """Tests logging in with invalid password."""

        post_data = {'user_id': self.user_info,
                     'password': 'many_pineapple'}

        response = self.client.post('/profile_page/api/login', post_data)
        self.assertEqual(response.status_code, 401,
                         msg=f'{BColors.FAIL}\t[-]\tLogged in with wrong password!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass not allowing incorrect password.{BColors.ENDC}")

    def test_login(self):
        """Tests user login by checking the token."""

        # login
        post_data = {'user_id': self.user_info,
                     'password': 'pineapple'}

        response = self.client.post('/profile_page/api/login', post_data)
        self.assertEqual(response.status_code, 200,
                         msg=f'{BColors.FAIL}\t[-]\tFailed to log-in!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass logging in.{BColors.ENDC}")

        # expected authentication token
        token = response.data['token']

        # check if user has the correct token
        self.assertEqual(profile_db.check_user(self.user_info, token), True,
                          msg=f'{BColors.FAIL}\t[-]\tUser has wrong token after log-in!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tUser has the correct token after log-in.{BColors.ENDC}")


class Logout(TestCase):
    """Tests the API calls that is related to user logout."""

    def setUp(self):
        """Create an account."""
        sleep(1)

        # temporary user name
        self.user_info = str(uuid.uuid1()).split('-')[0]

        post_data = {'user_name': self.user_info,
                     'password1': 'pineapple',
                     'password2': 'pineapple',
                     'email': self.user_info}
        response = self.client.post('/profile_page/api/register', post_data)
        self.assertEqual(response.status_code, 200,
                          msg=f'{BColors.FAIL}\t[-]\tFailed creating an account!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass creating a user.{BColors.ENDC}")

        # Authentication token
        self.token = response.data['token']

    def tearDown(self):
        """Removes the testing user from the database."""
        profile_db.remove_user(self.user_info)

    def test_logout(self):
        """Tests user logout by checking token."""

        # logout
        post_data = {'user_id': self.user_info,
                    'token': self.token}

        response = self.client.post('/profile_page/api/logout', post_data)
        self.assertEqual(response.status_code, 200,
                         msg=f'{BColors.FAIL}\t[-]\tFailed logging out!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass logging out.{BColors.ENDC}")

        # check if user doesn't have the token after logout
        self.assertEqual(profile_db.check_user(self.user_info, self.token), False,
                         msg=f'{BColors.FAIL}\t[-]\tUser still have the token after log-out!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tUser does not have the token after log-out.{BColors.ENDC}")


class Delete(TestCase):
    """Tests the API calls that is related to deleting user account."""

    def setUp(self):
        """Create an account."""
        sleep(1)

        # temporary user name
        self.user_info = str(uuid.uuid1()).split('-')[0]

        post_data = {'user_name': self.user_info,
                     'password1': 'pineapple',
                     'password2': 'pineapple',
                     'email': self.user_info}
        response = self.client.post('/profile_page/api/register', post_data)
        self.assertEqual(response.status_code, 200,
                          msg=f'{BColors.FAIL}\t[-]\tFailed creating an account!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass creating a user.{BColors.ENDC}")

        # Authentication token
        self.token = response.data['token']

    def test_delete(self):
        """Tests account deleting by checking if it is still in the database."""

        # delete account
        post_data = {'user_id': self.user_info,
                     'token': self.token}

        response = self.client.post('/profile_page/api/delete', post_data)
        self.assertEqual(response.status_code, 200,
                         msg=f'{BColors.FAIL}\t[-]\tFailed deleting the account!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass deleting the account.{BColors.ENDC}")

        # check if user the user does not exist after it got deleted
        self.assertEqual(profile_db.read_one_user(self.user_info), False,
                         msg=f'{BColors.FAIL}\t[-]\tUser still exist after the account deleted!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tUser is no longer in the database after got removed.{BColors.ENDC}")


class SaveBoard(TestCase):
    """Tests the API calls that is related to saving a game board."""

    def setUp(self):
        """Create an account and active game."""
        sleep(1)

        # temporary user name
        self.user_info = str(uuid.uuid1()).split('-')[0]

        post_data = {'user_name': self.user_info,
                     'password1': 'pineapple',
                     'password2': 'pineapple',
                     'email': self.user_info}
        response = self.client.post('/profile_page/api/register', post_data)
        self.assertEqual(response.status_code, 200,
                          msg=f'{BColors.FAIL}\t[-]\tFailed creating an account!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass creating a user.{BColors.ENDC}")

        # Authentication token
        self.token = response.data['token']

        # create a new game
        self.game_id = self.client.get('/game_board/api/start_game/Easy/ID1,ID2,ID3/AVL').data['game_id']
        self.board = self.client.get('/game_board/api/board/' + str(self.game_id)).data

    def tearDown(self):
        """Removes the testing user and game board from the database."""

        # remove user
        profile_db.remove_user(self.user_info)
        # remove the created game
        game_db.remove_game(self.game_id)

    def test_unauthorized_save(self):
        """Attempts to save a game from an unauthorized account."""

        post_data = {'user_id': self.user_info,
                     'game_id': self.game_id,
                     'token': self.token + 'a'}
        response = self.client.post('/profile_page/api/save_board', post_data)
        self.assertEqual(response.status_code, 401,
                          msg=f'{BColors.FAIL}\t[-]\tSaved game from unauthorized account!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass not allowing unauthorized account saving game.{BColors.ENDC}")

    def test_nonexisting_save(self):
        """Attempts to save a game that does not exist."""

        post_data = {'user_id': self.user_info,
                     'game_id': self.game_id +'a',
                     'token': self.token}
        response = self.client.post('/profile_page/api/save_board', post_data)
        self.assertEqual(response.status_code, 500,
                          msg=f'{BColors.FAIL}\t[-]\tSaved a game that does not exist!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass not saving a game that does not exist.{BColors.ENDC}")

    def test_board_save(self):
        """Attempts to save a game."""

        # save the game board
        post_data = {'user_id': self.user_info,
                     'game_id': self.game_id,
                     'token': self.token}
        response = self.client.post('/profile_page/api/save_board', post_data)
        self.assertEqual(response.status_code, 200,
                          msg=f'{BColors.FAIL}\t[-]\tFailed saving a game!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass saving a game.{BColors.ENDC}")

        # check if the saved game is in the list of saved games
        saved_games = self.client.get('/profile_page/api/saved_boards/' + str(self.user_info) + '/' \
                                      + str(self.token)).data['saved_games']
        game_ids = list()
        for board in saved_games:
            game_ids.append(board['game_id'])

        self.assertIn(self.game_id, game_ids,
                      msg=f'{BColors.FAIL}\t[-]\tGame ID was not in the saved games!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tFound the saved game ID in the user's profile.{BColors.ENDC}")


class Share(TestCase):
    """Tests the API calls that is related to sharing the game board."""

    def setUp(self):
        """Create two accounts, game, and save the game to the first account."""
        sleep(1)

        # temporary user names
        self.user_1_info = str(uuid.uuid1()).split('-')[0]
        self.user_2_info = str(uuid.uuid1()).split('-')[0]

        # Create the user 1
        post_data_1 = {'user_name': self.user_1_info,
                     'password1': 'pineapple',
                     'password2': 'pineapple',
                     'email': self.user_1_info}
        response_1 = self.client.post('/profile_page/api/register', post_data_1)
        self.assertEqual(response_1.status_code, 200,
                          msg=f'{BColors.FAIL}\t[-]\tFailed creating an account!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass creating a user.{BColors.ENDC}")

        # Create user 2
        post_data_2 = {'user_name': self.user_2_info,
                     'password1': 'pineapple',
                     'password2': 'pineapple',
                     'email': self.user_2_info}
        response_2 = self.client.post('/profile_page/api/register', post_data_2)
        self.assertEqual(response_2.status_code, 200,
                          msg=f'{BColors.FAIL}\t[-]\tFailed creating an account!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass creating a user.{BColors.ENDC}")

        # Authentication tokens
        self.token_user_1 = response_1.data['token']
        self.token_user_2 = response_2.data['token']

        # create a new game
        self.game_id = self.client.get('/game_board/api/start_game/Easy/ID1,ID2,ID3/AVL').data['game_id']

        # Save the game to user 1's profile
        post_data_save = {'user_id': self.user_1_info,
                          'game_id': self.game_id,
                          'token': self.token_user_1}
        response_save = self.client.post('/profile_page/api/save_board', post_data_save)
        self.assertEqual(response_save.status_code, 200,
                          msg=f'{BColors.FAIL}\t[-]\tFailed saving a game!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass saving a game.{BColors.ENDC}")

    def tearDown(self):
        """Removes the testing user and game board from the database."""

        # remove the users
        profile_db.remove_user(self.user_1_info)
        profile_db.remove_user(self.user_2_info)
        # remove the created game
        game_db.remove_game(self.game_id)

    def test_unauthorized_share(self):
        """Attempts to share a game from an unauthorized account."""

        post_data = {'source_user_id': self.user_1_info,
                     'dest_user_id': self.user_2_info,
                     'game_id': self.game_id,
                     'token': self.token_user_1 + 'a'}
        response = self.client.post('/profile_page/api/share', post_data)
        self.assertEqual(response.status_code, 401,
                          msg=f'{BColors.FAIL}\t[-]\tShared game from unauthorized account!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass not allowing unauthorized account sharing game.{BColors.ENDC}")

    def test_nonexisting_board_share(self):
        """Attempts to share a game that does notexist."""

        post_data = {'source_user_id': self.user_1_info,
                     'dest_user_id': self.user_2_info,
                     'game_id': self.game_id + 'a',
                     'token': self.token_user_1}
        response = self.client.post('/profile_page/api/share', post_data)
        self.assertEqual(response.status_code, 500,
                          msg=f'{BColors.FAIL}\t[-]\tShared game from that does not exist!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass not sharing a game that does not exist.{BColors.ENDC}")

    def test_nonexisting_destination_user_share(self):
        """Attempts to share a game with a user that does not exist."""

        post_data = {'source_user_id': self.user_1_info,
                     'dest_user_id': self.user_2_info + 'a',
                     'game_id': self.game_id,
                     'token': self.token_user_1}
        response = self.client.post('/profile_page/api/share', post_data)
        self.assertEqual(response.status_code, 500,
                          msg=f'{BColors.FAIL}\t[-]\tShared game with a user that does not exist!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass not sharing a game with a user that does not exist.{BColors.ENDC}")

    def test_share(self):
        """Attempts to share a game with another user."""

        # Share the game
        post_data = {'source_user_id': self.user_1_info,
                     'dest_user_id': self.user_2_info,
                     'game_id': self.game_id,
                     'token': self.token_user_1}
        response = self.client.post('/profile_page/api/share', post_data)
        self.assertEqual(response.status_code, 200,
                          msg=f'{BColors.FAIL}\t[-]\tFailed to share a game with a user!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass sharing the game.{BColors.ENDC}")

        # Check the destination user if the game was shared
        saved_games = self.client.get('/profile_page/api/saved_boards/' + str(self.user_2_info) + '/' \
                                      + str(self.token_user_2)).data['saved_games']
        game_ids = list()
        for board in saved_games:
            game_ids.append(board['game_id'])

        self.assertIn(self.game_id, game_ids,
                      msg=f'{BColors.FAIL}\t[-]\tGame ID was not in the saved games of destination user!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tFound the saved game ID in the destination user's profile.{BColors.ENDC}")


class DeleteBoard(TestCase):
    """Tests the API calls that is related to deleting the saved game board."""

    def setUp(self):
        """Create an account and active game. Then save the game to the user's profile."""
        sleep(1)

        # temporary user name
        self.user_info = str(uuid.uuid1()).split('-')[0]

        # Create the user
        post_data = {'user_name': self.user_info,
                     'password1': 'pineapple',
                     'password2': 'pineapple',
                     'email': self.user_info}
        response_1 = self.client.post('/profile_page/api/register', post_data)
        self.assertEqual(response_1.status_code, 200,
                          msg=f'{BColors.FAIL}\t[-]\tFailed creating an account!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass creating a user.{BColors.ENDC}")

        # Authentication token
        self.token = response_1.data['token']

        # create a new game
        self.game_id = self.client.get('/game_board/api/start_game/Easy/ID1,ID2,ID3/AVL').data['game_id']

        # Save the game to user 's profile
        post_data_save = {'user_id': self.user_info,
                          'game_id': self.game_id,
                          'token': self.token}
        response_save = self.client.post('/profile_page/api/save_board', post_data_save)
        self.assertEqual(response_save.status_code, 200,
                          msg=f'{BColors.FAIL}\t[-]\tFailed saving a game!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass saving a game.{BColors.ENDC}")

    def tearDown(self):
        """Removes the testing user and game board from the database."""

        # remove the user
        profile_db.remove_user(self.user_info)
        # remove the created game
        game_db.remove_game(self.game_id)

    def test_unauthorized_delete(self):
        """Attempts to delete a game from an unauthorized account."""

        post_data = {'user_id': self.user_info,
                     'game_id': self.game_id,
                     'token': self.token + 'a'}
        response = self.client.post('/profile_page/api/delete_board', post_data)
        self.assertEqual(response.status_code, 401,
                          msg=f'{BColors.FAIL}\t[-]\tDeleted game from unauthorized account!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass not allowing unauthorized account delete game.{BColors.ENDC}")

    def test_delete(self):
        """Attempts to delete a saved game from an account."""

        post_data = {'user_id': self.user_info,
                     'game_id': self.game_id,
                     'token': self.token}
        response = self.client.post('/profile_page/api/delete_board', post_data)
        self.assertEqual(response.status_code, 200,
                          msg=f'{BColors.FAIL}\t[-]\tFailed deleting the game from user profile!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass deleting the saved game.{BColors.ENDC}")

class SavedBoards(TestCase):
    """Tests the API calls that is related to listing the saved games."""

    def setUp(self):
        """Create an account and 2 active games. Then save the games to the user's profile."""
        sleep(1)

        # temporary user name
        self.user_info = str(uuid.uuid1()).split('-')[0]

        # Create the user
        post_data = {'user_name': self.user_info,
                     'password1': 'pineapple',
                     'password2': 'pineapple',
                     'email': self.user_info}
        response_1 = self.client.post('/profile_page/api/register', post_data)
        self.assertEqual(response_1.status_code, 200,
                          msg=f'{BColors.FAIL}\t[-]\tFailed creating an account!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass creating a user.{BColors.ENDC}")

        # Authentication token
        self.token = response_1.data['token']

        # create 2 new games
        self.game_id_1 = self.client.get('/game_board/api/start_game/Easy/ID1,ID2,ID3/AVL').data['game_id']
        self.game_id_2 = self.client.get('/game_board/api/start_game/Hard/ID1,ID2,ID3/AVL').data['game_id']

        # Save the games to user 's profile
        # save game 1
        post_data_save_1 = {'user_id': self.user_info,
                          'game_id': self.game_id_1,
                          'token': self.token}
        response_save_1 = self.client.post('/profile_page/api/save_board', post_data_save_1)
        self.assertEqual(response_save_1.status_code, 200,
                          msg=f'{BColors.FAIL}\t[-]\tFailed saving a game!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass saving a game.{BColors.ENDC}")

        # save game 2
        post_data_save_2 = {'user_id': self.user_info,
                          'game_id': self.game_id_2,
                          'token': self.token}
        response_save_2 = self.client.post('/profile_page/api/save_board', post_data_save_2)
        self.assertEqual(response_save_2.status_code, 200,
                          msg=f'{BColors.FAIL}\t[-]\tFailed saving a game!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass saving a game.{BColors.ENDC}")

    def tearDown(self):
        """Removes the testing user and game board from the database."""

        # remove the user
        profile_db.remove_user(self.user_info)
        # remove the created games
        game_db.remove_game(self.game_id_1)
        game_db.remove_game(self.game_id_2)

    def test_unauthorized_list(self):
        """Attempts to list the saved games from an unauthorized account."""

        response = self.client.get('/profile_page/api/saved_boards/' + str(self.user_info) + '/' \
                                      + str(self.token + 'a'))
        self.assertEqual(response.status_code, 401,
                          msg=f'{BColors.FAIL}\t[-]\tListed the saved games from unauthorized account!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass not allowing listing games from unauthorized account.{BColors.ENDC}")

    def test_list(self):
        """Attempts to list the saved games."""

        # get the list of saved game board in the user's profile
        response = self.client.get('/profile_page/api/saved_boards/' + str(self.user_info) + '/' \
                                      + str(self.token))
        self.assertEqual(response.status_code, 200,
                          msg=f'{BColors.FAIL}\t[-]\tFailed listing the saved games!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass listing the saved games.{BColors.ENDC}")

        # check if both of the saved game boards are in the user's profile
        game_ids = list()
        for board in response.data['saved_games']:
            game_ids.append(board['game_id'])

        self.assertEqual(set([self.game_id_1, self.game_id_2]), set(game_ids),
                      msg=f'{BColors.FAIL}\t[-]\tGame ID was not in the saved games of destination user!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tBoth game IDs were in the user's profile.{BColors.ENDC}")


class LoadBoard(TestCase):
    """Tests the API calls that is related to loading saved games."""

    def setUp(self):
        """Create an account and active game. Then save the games to the user's profile."""
        sleep(1)

        # temporary user name
        self.user_info = str(uuid.uuid1()).split('-')[0]

        # Create the user
        post_data = {'user_name': self.user_info,
                     'password1': 'pineapple',
                     'password2': 'pineapple',
                     'email': self.user_info}
        response_1 = self.client.post('/profile_page/api/register', post_data)
        self.assertEqual(response_1.status_code, 200,
                          msg=f'{BColors.FAIL}\t[-]\tFailed creating an account!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass creating a user.{BColors.ENDC}")

        # Authentication token
        self.token = response_1.data['token']

        # create a new game
        self.game_id = self.client.get('/game_board/api/start_game/Easy/ID1,ID2,ID3/AVL').data['game_id']

        # Save the game to user 's profile
        post_data_save = {'user_id': self.user_info,
                          'game_id': self.game_id,
                          'token': self.token}
        response_save = self.client.post('/profile_page/api/save_board', post_data_save)
        self.assertEqual(response_save.status_code, 200,
                          msg=f'{BColors.FAIL}\t[-]\tFailed saving a game!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass saving a game.{BColors.ENDC}")

        # remove the active games since we can't have the duplicate active games
        game_db.remove_game(self.game_id)

    def tearDown(self):
        """Removes the testing user and game board from the database."""

        # remove the user
        profile_db.remove_user(self.user_info)
        # remove the created games
        game_db.remove_game(self.game_id)

    def test_unauthorized_load(self):
        """Attempts to list the load games from an unauthorized account."""

        post_data = {'user_id': self.user_info,
                     'game_id': self.game_id,
                     'token': self.token + 'a'}
        response = self.client.post('/profile_page/api/load_board', post_data)
        self.assertEqual(response.status_code, 401,
                          msg=f'{BColors.FAIL}\t[-]\tLoaded game from unauthorized account!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass not allowing unauthorized account loading game.{BColors.ENDC}")

    def test_load_board(self):
        """Attempts to list the load games from an unauthorized account."""

        # load the game board
        post_data = {'user_id': self.user_info,
                     'game_id': self.game_id,
                     'token': self.token}
        response = self.client.post('/profile_page/api/load_board', post_data)

        self.assertEqual(response.status_code, 200,
                          msg=f'{BColors.FAIL}\t[-]\tFailed loading a game!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass loading a saved game board.{BColors.ENDC}")

        # check if it is the same game
        self.assertEqual(response.data['game_id'], self.game_id,
                          msg=f'{BColors.FAIL}\t[-]\tLoaded game does not match!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass loading the same game.{BColors.ENDC}")

        # check if the loaded game is now in the active games
        active_game = self.client.get('/game_board/api/board/' + str(self.game_id))
        self.assertEqual(active_game.status_code, 200,
                          msg=f'{BColors.FAIL}\t[-]\tLoaded game is not in the active games!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass loading the in to the active games.{BColors.ENDC}")
