"""
    Profile page API calls that allow interaction with
    the user's information such as log-in and sign-up.
    This API also provides calls for interaction with
    the information related to the user's profile such as
    game board sharing and saving.
"""
import uuid
import re
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from game_board.api import utils as game_utils
from profile_page.database import profile_page_db as db
from profile_page.api import mock as mock_db


# TODO: RYAN, Import your code

@api_view(['GET'])
def api_overview(request):
    '''
    Overview of the API calls exist.
    :param request:
    :return: Response, list of API URLs for the user profile.
    '''
    api_urls = {
        # Authentication API calls
        'Create a new user': '/register',
        'Log-in': '/login',
        'Log-out': '/logout',

        # User profile
        'Get all profile': '/profile',

        # Game Board API Calls for User Profile
        'Save Game Board': '/save_board',
        'Delete Game Board': '/delete_board',
        'Share': '/share',
        'Saved Game Boards': '/saved_boards/<str:user_id>/<str:token>',
        'Load Game Board': '/load_board'

    }
    return Response(api_urls)


@api_view(['POST'])
def profile(request):
    """
    POST request API call.
    Returns all of the user's profile information if the user is authenticated.
    Else, UNAUTHORIZED error is returned.
    :param request: POST request with fields 'user_id', 'token'.
    :return: success message, else error status.
    """
    # user_name == user_id
    required_fields = ['user_id', 'token']

    # Check if the post request contain the required fields
    if set(required_fields) != set(list(request.data.keys())):
        return Response({'error': str('Missing required fields!')}, status=status.HTTP_400_BAD_REQUEST)

    # POST Request content
    data = request.data

    # check for bad characters
    if check_special_characters(str(data['user_id'])) or check_special_characters(str(data['token'])):
        return Response({'error': str('Unaccepted character passed!')},
                        status=status.HTTP_400_BAD_REQUEST)

    # Here check if user_id matches the token with the database
    if not db.check_user(data['user_id'], data['token']):
        return Response({'error': str('UNAUTHORIZED')}, status=status.HTTP_401_UNAUTHORIZED)

    # Get the user profile data
    user_profile_data = db.read_one_user(data['user_id'])

    # Extract the game board information needed to list user's saved games
    saved_game_boards = user_profile_data['save_games']
    game_board_info = list()
    for game in saved_game_boards:
        temp = {
            'game_id': game['game_id'],
            'difficulty': game['difficulty'],
            'curr_data_structure': game['curr_data_structure']
        }
        game_board_info.append(temp)

    # Form the response data
    response_data = {
        'user_name': user_profile_data['user_id'],
        'badges': user_profile_data['badges'],
        'current_story_level': user_profile_data['current_story_level'],
        'friends': user_profile_data['friends'],
        'points': round(user_profile_data['points'], 2),
        'rank': user_profile_data['rank'],
        'saved_games': game_board_info
    }

    return Response({'user_profile': response_data})

@api_view(['POST'])
def add_friend(request):
    """
    POST request API call.
    Sends a friend request to the destination user if the source user is authenticated.
    Else, UNAUTHORIZED error is returned.
    source_user_id: user who is adding a friend.
    dest_user_id: friend who is being added.
    token: authentication token that allow access to the user's account.
    :param request: POST request with fields 'source_user_id', 'dest_user_id', 'token'
    :return: success message or error status.
    """
    required_fields = ['source_user_id', 'dest_user_id', 'token']

    # Check if the post request contain the required fields
    if set(required_fields) != set(list(request.data.keys())):
        return Response({'error': str('Missing required fields!')}, status=status.HTTP_400_BAD_REQUEST)

    # POST Request content
    data = request.data

    # Here check if user_id matches the token with the database
    if not db.check_user(data['source_user_id'], data['token']):
        return Response({'error': str('UNAUTHORIZED')}, status=status.HTTP_401_UNAUTHORIZED)

    # Send friend request
    if not mock_db.add_friend(data['source_user_id'], data['dest_user_id']):
        return Response({'error': str('Error when adding friend!')},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'status': 'success'})


@api_view(['POST'])
def accept_decline_friend(request):
    """
    POST request API call.
    Accepts the friend request if the source user is authenticated.
    Else, UNAUTHORIZED error is returned.
    source_user_id: user who recieved the friend request.
    dest_user_id: user who initiated friend request.
    accept: indicate acceptence or decline of the request.
    token: authentication token that allow access to the user's account.
    :param request: POST request with fields 'source_user_id', 'dest_user_id', 'accept', 'token'
    :return: success message or error status.
    """
    required_fields = ['source_user_id', 'dest_user_id', 'accept', 'token']

    # Check if the post request contain the required fields
    if set(required_fields) != set(list(request.data.keys())):
        return Response({'error': str('Missing required fields!')}, status=status.HTTP_400_BAD_REQUEST)

    # POST Request content
    data = request.data

    # Here check if user_id matches the token with the database
    if not db.check_user(data['source_user_id'], data['token']):
        return Response({'error': str('UNAUTHORIZED')}, status=status.HTTP_401_UNAUTHORIZED)

    # if friend request is being accepted
    if data['accept'] == "yes":
        if not mock_db.accept_friend(data['source_user_id'], data['dest_user_id']):
            return Response({'error': str('Error when accepting friend request!')},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # if friend request is not accepted
    elif data['accept'] == "no":
        if not mock_db.cancel_friend_request(data['source_user_id'], data['dest_user_id']):
            return Response({'error': str('Error when declining friend request!')},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # bad request
    else:
        return Response({'error': str('Invalid request. Use yes/no in accept field.')},
                        status=status.HTTP_400_BAD_REQUEST)

    return Response({'status': 'success'})


@api_view(['POST'])
def remove_friend(request):
    """
    POST request API call.
    Removes the friend from user's profile if the source user is authenticated.
    Else, UNAUTHORIZED error is returned.
    source_user_id: user who is deleting a friend.
    dest_user_id: friend that is being deleted.
    token: authentication token that allow access to the user's account.
    :param request: POST request with fields 'source_user_id', 'dest_user_id', 'token'
    :return: success message or error status.
    """
    required_fields = ['source_user_id', 'dest_user_id', 'token']

    # Check if the post request contain the required fields
    if set(required_fields) != set(list(request.data.keys())):
        return Response({'error': str('Missing required fields!')}, status=status.HTTP_400_BAD_REQUEST)

    # POST Request content
    data = request.data

    # Here check if user_id matches the token with the database
    if not db.check_user(data['source_user_id'], data['token']):
        return Response({'error': str('UNAUTHORIZED')}, status=status.HTTP_401_UNAUTHORIZED)

    # delete friend from user profile
    if not mock_db.remove_friend(data['source_user_id'], data['dest_user_id']):
        return Response({'error': str('Error when removing friend from the profile!')},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'status': 'success'})


@api_view(['POST'])
def register(request):
    """
    POST request API call.
    Registers a new user by creating a new account in the databse.
    Two passwords that are being passed must match.
    Username or e-mail should not exist already.
    user_name: User's unique name.
    password1: Password.
    password2: Password match.
    email: User's email.
    :param request: POST request with fields 'user_name', 'password1', 'password2', 'email'
    :return: user token for the authentcation if sucesfull, else error message.
    """
    # user_name == user_id
    required_fields = ['user_name', 'password1', 'password2', 'email']

    # Check if the post request contain the required fields
    if set(required_fields) != set(list(request.data.keys())):
        return Response({'error': str('Missing required fields!')}, status=status.HTTP_400_BAD_REQUEST)

    # POST Request content
    data = request.data

    # Check if passwords match
    if data['password1'] != data['password2']:
        return Response({'error': str('Passwords do not match!')}, status=status.HTTP_400_BAD_REQUEST)

    # Check minimum password length
    if len(str(data['password1'])) <= 8:
        return Response({'error': str('Password has to be longer than 8 characters!')}, status=status.HTTP_400_BAD_REQUEST)

    # check if user name is less than 3 characters
    if len(str(data['user_name'])) <= 5:
        return Response({'error': str('Username must be longer than 5 characters!')}, status=status.HTTP_400_BAD_REQUEST)

    # Check if user name does not start with bot
    if str(data['user_name'])[0:3].lower() == 'bot':
        return Response({'error': str('Username can not start with "bot"!')}, status=status.HTTP_400_BAD_REQUEST)

    # Check if username has space
    if str(data['user_name']).isspace() or str(data['password1']).isspace() or str(data['email']).isspace():
        return Response({'error': str('Username, password, and email can not have space!')}, status=status.HTTP_400_BAD_REQUEST)

    # check for valid e-mail
    if not bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", str(data['email']))):
        return Response({'error': str('Invalid e-mail!')},
                        status=status.HTTP_400_BAD_REQUEST)

    # check for not allowed characters
    if check_special_characters(str(data['user_name'])) or check_special_characters(str(data['password1'])):
        return Response({'error': str('Unaccepted character passed!')},
                        status=status.HTTP_400_BAD_REQUEST)

    # Here ask db to create a new user with its token
    token = str(uuid.uuid1())
    if not db.create_user(str(data['user_name']), str(data['password1']), str(data['email']), token):
        return Response({'error': str('Error when creating the account!')}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'status': 'success', 'token': token})

@api_view(['POST'])
def login(request):
    """
    POST request API call.
    Checks the database for matching username and password.
    If match is found, returns an authentication token.
    If match is not found, UNAUTHORIZED is returned.
    user_id: unique user identifier (same as username).
    password: user's password.
    :param request: POST request with fields 'user_id', 'password'.
    :return: user token for the authentcation if sucesfull, else error message.
    """
    # user_name == user_id
    required_fields = ['user_id', 'password']

    # Check if the post request contain the required fields
    if set(required_fields) != set(list(request.data.keys())):
        return Response({'error': str('Missing required fields!')}, status=status.HTTP_400_BAD_REQUEST)

    # POST Request content
    data = request.data

    # check for not allowed characters
    if check_special_characters(str(data['user_id'])) or check_special_characters(str(data['password'])):
        return Response({'error': str('Unaccepted character passed!')},
                        status=status.HTTP_400_BAD_REQUEST)

    # Here ask db if username and password works out
    # if db says nope, return error. else proceed.
    if not db.login(data['user_id'], data['password']):
        return Response({'error': str('UNAUTHORIZED')}, status=status.HTTP_401_UNAUTHORIZED)

    # Here let db know of the new token that user owns
    token = str(uuid.uuid1())
    if not db.update_token(data['user_id'], token):
        return Response({'error': str('Error when updating log-in token!')}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'status': 'success', 'token': token})


@api_view(['POST'])
def logout(request):
    """
    If the username has the given token, logout action is performed
    by removing user's token from the database.
    Else, UNAUTHORIZED error is returned.
    user_id: unique user identifier (same as username).
    token: authentication token that allow access to the user's account.
    :param request: POST request with fields 'user_id', 'token'.
    :return: success message, else error status.
    """
    # user_name == user_id
    required_fields = ['user_id', 'token']

    # Check if the post request contain the required fields
    if set(required_fields) != set(list(request.data.keys())):
        return Response({'error': str('Missing required fields!')}, status=status.HTTP_400_BAD_REQUEST)

    # POST Request content
    data = request.data

    # check for not allowed characters
    if check_special_characters(str(data['user_id'])) or check_special_characters(str(data['token'])):
        return Response({'error': str('Unaccepted character passed!')},
                        status=status.HTTP_400_BAD_REQUEST)

    # Here check if user_id matches the token with the database
    if not db.check_user(data['user_id'], data['token']):
        return Response({'error': str('UNAUTHORIZED')}, status=status.HTTP_401_UNAUTHORIZED)

    # Here let db know we are logging out by removing user's token
    if not db.remove_token(data['user_id']):
        return Response({'error': str('Error when logging out!')}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'status': 'success'})


@api_view(['POST'])
def delete(request):
    """
    If the username has the given token, user's account is deleted.
    Else, UNAUTHORIZED error is returned.
    user_id: unique user identifier (same as username).
    token: authentication token that allow access to the user's account.
    :param request: POST request with fields 'user_id', 'token'.
    :return: success message, else error status.
    """
    # user_name == user_id
    required_fields = ['user_id', 'token']

    # Check if the post request contain the required fields
    if set(required_fields) != set(list(request.data.keys())):
        return Response({'error': str('Missing required fields!')}, status=status.HTTP_400_BAD_REQUEST)

    # POST Request content
    data = request.data

    # check for not allowed characters
    if check_special_characters(str(data['user_id'])) or check_special_characters(str(data['token'])):
        return Response({'error': str('Unaccepted character passed!')},
                        status=status.HTTP_400_BAD_REQUEST)

    # Here check if user_id matches the token with the database
    if not db.check_user(data['user_id'], data['token']):
        return Response({'error': str('UNAUTHORIZED')}, status=status.HTTP_401_UNAUTHORIZED)

    # Here remove the user's account from the database
    if not db.remove_user(data['user_id']):
        return Response({'error': str('Error when removing the user account!')}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'status': 'success'})


@api_view(['POST'])
def save_board(request):
    """
    Saves the active game from the list of active games in the database
    to the user's profile. Game is only saved if the user is
    authenticated, i.e. if the user has the matching token, else
    UNAUTHORIZED error is returned.
    Game that is being saved must exist in the list of active games.
    user_id: unique user identifier (same as username).
    token: authentication token that allow access to the user's account.
    game_id: ID of the saved game.
    :param request: POST request with fields 'user_id', 'game_id', 'token'.
    :return: success message, or error status.
    """
    required_fields = ['user_id', 'game_id', 'token']

    # Check if the post request contain the required fields
    if set(required_fields) != set(list(request.data.keys())):
        return Response({'error': str('Missing required fields!')}, status=status.HTTP_400_BAD_REQUEST)

    # POST Request content
    data = request.data

    # check for not allowed characters
    if check_special_characters(str(data['user_id'])) or check_special_characters(str(data['game_id']))  \
            or check_special_characters(str(data['token'])):
        return Response({'error': str('Unaccepted character passed!')},
                        status=status.HTTP_400_BAD_REQUEST)

    # Here check if user_id matches the token with the database
    if not db.check_user(data['user_id'], data['token']):
        return Response({'error': str('UNAUTHORIZED')}, status=status.HTTP_401_UNAUTHORIZED)

    # Load the game board from the database
    response_status = game_utils.load_board_db(data['game_id'])
    if response_status['error']:
        return Response({'error': response_status['reason']},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    board = response_status['game_board']

    # Here append new game board to user's profile. Note that this board already have an ID.
    if not db.save_game(data['user_id'], board):
        return Response({'error': str('Error when saving the game!')}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'status': 'success'})


@api_view(['POST'])
def delete_board(request):
    """
    Removes the saved game board from user's profile.
    User must be authenticated, i.e. must have the matching token.
    Game board in the user's profile identified by game_id must exist.
    user_id: unique user identifier (same as username).
    token: authentication token that allow access to the user's account.
    game_id: ID of the saved game.
    :param request: POST request with fields 'user_id', 'game_id', 'token'.
    :return: success message, or error status.
    """
    required_fields = ['user_id', 'game_id', 'token']

    # Check if the post request contain the required fields
    if set(required_fields) != set(list(request.data.keys())):
        return Response({'error': str('Missing required fields!')}, status=status.HTTP_400_BAD_REQUEST)

    # POST Request content
    data = request.data

    # check for not allowed characters
    if check_special_characters(str(data['user_id'])) or check_special_characters(str(data['game_id']))  \
            or check_special_characters(str(data['token'])):
        return Response({'error': str('Unaccepted character passed!')},
                        status=status.HTTP_400_BAD_REQUEST)

    # Here check if user_id matches the token with the database
    if not db.check_user(data['user_id'], data['token']):
        return Response({'error': str('UNAUTHORIZED')}, status=status.HTTP_401_UNAUTHORIZED)

    # Here delete the game board from user's saved profile
    if not db.delete_game(data['user_id'], data['game_id']):
        return Response({'error': str('Error when deleting the game!')}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'status': 'success'})


@api_view(['POST'])
def share(request):
    """
    Shares the user's game boards with the destination user.
    User who is initiating the share action must be authenticated, i.e.
    the user must have the matching token. The game board
    identified by game_id must exist in user's profile.
    Destination user must have the accept shared games setting turned on.
    Share action is performed by creating a copy of the game board in the
    user's profile identified by dest_user_id.
    source_user_id: unique user identifier of user initiating share (same as username).
    dest_user_id: unique user identifier of user recieving the game (same as username).
    token: authentication token that allow access to the user's account.
    game_id: ID of the saved game.
    :param request: POST request with fields 'source_user_id', 'dest_user_id', 'game_id', 'token'
    :return: success message or error status.
    """
    required_fields = ['source_user_id', 'dest_user_id', 'game_id', 'token']

    # Check if the post request contain the required fields
    if set(required_fields) != set(list(request.data.keys())):
        return Response({'error': str('Missing required fields!')}, status=status.HTTP_400_BAD_REQUEST)

    # POST Request content
    data = request.data

    # check for not allowed characters
    if check_special_characters(str(data['source_user_id'])) or check_special_characters(str(data['dest_user_id']))  \
            or check_special_characters(str(data['game_id'])) or check_special_characters(str(data['token'])):
        return Response({'error': str('Unaccepted character passed!')},
                        status=status.HTTP_400_BAD_REQUEST)

    # Here check if user_id matches the token with the database
    if not db.check_user(data['source_user_id'], data['token']):
        return Response({'error': str('UNAUTHORIZED')}, status=status.HTTP_401_UNAUTHORIZED)

    # Here call db to copy saved game board from source_user_id to dest_user_id
    # This database call just copies the saved board into dest_user_id's saved game boards
    if not db.share_game_board(data['source_user_id'], data['dest_user_id'], data['game_id']):
        return Response({'error': str('Error when sharing the game!')}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'status': 'success'})


@api_view(['GET'])
def saved_boards(request, user_id, token):
    """
    GET request API call to aquire the saved games in the user's profile.
    user_id: unique user identifier (same as username).
    token: authentication token that allow access to the user's account.
    :param request: GET request
    :param user_id: username who is performing the action
    :param token: authentication token
    :return: dictionary of information for the saved games
    """

    # Here check if user_id matches the token with the database
    if not db.check_user(user_id, token):
        return Response({'error': str('UNAUTHORIZED')}, status=status.HTTP_401_UNAUTHORIZED)

    # Get list of game board IDs of user's saved game boards so that
    # user later can use these ids on other API calls
    saved_game_boards = db.list_user_games(user_id)

    # Extract the game board information needed to list user's saved games
    game_board_info = list()
    for game in saved_game_boards:
        temp = {
            'game_id': game['game_id'],
            'difficulty': game['difficulty'],
            'curr_data_structure': game['curr_data_structure']
        }
        game_board_info.append(temp)

    return Response({'saved_games': game_board_info})


@api_view(['POST'])
def load_board(request):
    """
    POST request API call to load in a saved game board.
    This API call activates the saved gave in the user's profile by
    moving the saved board to the list of active games.
    User must be authenticated, i.e. token must match with user's profile.
    Once the game loaded, i.e. moved to the active games, board can be
    interacted with using the Game Board API.
    User must have the claimed game board defined by the game_id.
    user_id: unique user identifier (same as username).
    token: authentication token that allow access to the user's account.
    game_id: ID of the saved game.
    :param request: POST request with fields 'user_id', 'game_id', 'token'
    :return: Game Board instance
    """
    required_fields = ['user_id', 'game_id', 'token']

    # Check if the post request contain the required fields
    if set(required_fields) != set(list(request.data.keys())):
        return Response({'error': str('Missing required fields!')}, status=status.HTTP_400_BAD_REQUEST)

    # POST Request content
    data = request.data

    if check_special_characters(str(data['user_id'])) or check_special_characters(str(data['game_id']))  \
            or check_special_characters(str(data['token'])):
        return Response({'error': str('Unaccepted character passed!')},
                        status=status.HTTP_400_BAD_REQUEST)

    # Here check if user_id matches the token with the database
    if not db.check_user(data['user_id'], data['token']):
        return Response({'error': str('UNAUTHORIZED')}, status=status.HTTP_401_UNAUTHORIZED)

    # Load the game from user's saved profile
    game_board = db.load_board(data['user_id'], data['game_id'])

    # indicate that this board is being loaded from the profile
    game_board['profile_load'] = True

    # Here I am just going to move this board to active games using the api we already have.
    # Note that board is still saved on user's profile, but we are just creating a new active game.
    response_status = game_utils.create_board_db(game_board)
    if response_status['error']:
        return Response({'error': response_status['reason']},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    active_game_id = response_status['game_id']

    # Here i am just going to return the game board itself from the active games
    # From this point front-end can continue using the Game Board API to interact with the game
    response_status = game_utils.load_board_db(active_game_id)
    if response_status['error']:
        return Response({'error': response_status['reason']},
                        status=status.HTTP_400_BAD_REQUEST)

    # hide the UID used by data structure backend from user
    del response_status['game_board']['graph']['uid']

    return Response(response_status['game_board'])

@api_view(['GET'])
def scheduled_tasks(request):
    """
    GET request API call.
    Starts the scheduled tasks
    :param request: GET request
    :return: success message, else error status.
    """

    # TODO: RYAN, here call schedule 1 (gameboard cleaner), don't forget to import it above
    # ryan_code.destroy_games()
    # IF ERROR EXAMPLE:
    #         return Response({'error': 'Did not work because_!'},
    #                         status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # TODO: RYAN, here call schedule 2 (scores sorter to assign ranking to each user),  don't forget to import it above
    # ryan_code2.set_rankings()

    # TODO: RYAN, no code here but need to setup the CI on github to have URL to this API call
    return Response({'Done'})

def check_special_characters(string):
    """Check if string has the target special character"""

    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]\'')
    return not (regex.search(string) == None)
