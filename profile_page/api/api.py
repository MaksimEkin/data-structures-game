"""
    Profile page API calls that allow interaction with
    the user's information such as log-in and sign-up.
    This API also provides calls for interaction with
    the information related to the user's profile such as
    game board sharing and saving.
"""
import uuid
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from game_board.api import utils as game_utils
from profile_page.database import profile_page_db as db


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


@api_view(['GET'])
def profile(request):
    """
    TODO: This API call is not implemented yet.

    :param request:
    :return:
    """
    Response({'status': 'TODO'})


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
        return Response({'error': str('Passwords does not match!')}, status=status.HTTP_400_BAD_REQUEST)

    # Here ask db to create a new user with its token
    token = str(uuid.uuid1())
    if not db.create_user(data['user_name'], data['password1'], data['email'], token):
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

    # Here ask db if username and password works out
    # if db says nope, return error. else proceed.
    if not db.login(data['user_id'], data['password']):
        return Response({'error': str('UNAUTHORIZED')}, status=status.HTTP_401_UNAUTHORIZED)

    # Here let db know of the new token that user owns
    token = str(uuid.uuid1())
    if not db.update_token(data['user_id'], token):
        return Response({'error': str('Error when updating logging in!')}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'status': 'success', 'token': token})


@api_view(['POST'])
def logout(request):
    """
    If the username has the given token, logout action is performed
    by removing user's token from the database.
    Else, UNAUTHORIZED error is returned.

    user_id: unique user identifier (same as username).
    token: authentication token that allow access to the user's account.

    :param self: POST request with fields 'user_id', 'token'.
    :return: success message, else error status.
    """
    # user_name == user_id
    required_fields = ['user_id', 'token']

    # Check if the post request contain the required fields
    if set(required_fields) != set(list(request.data.keys())):
        return Response({'error': str('Missing required fields!')}, status=status.HTTP_400_BAD_REQUEST)

    # POST Request content
    data = request.data

    # Here check if user_id matches the token with the database
    if not db.check_user(data['user_id'], data['token']):
        return Response({'error': str('UNAUTHORIZED')}, status=status.HTTP_401_UNAUTHORIZED)

    # Here let db know we are logging out by removing user's token
    if not db.remove_token(data['user_id']):
        return Response({'error': str('Error when logging out!')}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

    # Here check if user_id matches the token with the database
    if not db.check_user(data['user_id'], data['token']):
        return Response({'error': str('UNAUTHORIZED')}, status=status.HTTP_401_UNAUTHORIZED)

    # Load the game from user's saved profile
    game_board = db.load_board(data['user_id'], data['game_id'])

    # Here I am just going to move this board to active games using the api we already have.
    # Note that board is still saved on user's profile, but we are just creating a new active game.
    response_status = game_utils.create_board_db(game_board)
    print(response_status)
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