from rest_framework.decorators import api_view
from rest_framework.response import Response
# Status codes documentation: https://www.django-rest-framework.org/api-guide/status-codes/
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

import uuid
import json

from game_board.api import utils as game_utils
from game_board.database import game_board_db as game_db

# from profile_page.database import profile_page_db as db
from . import mock_db as db

@api_view(['GET'])
def api_overview(request):
    '''
    Overview of the API calls exist.

    :param request:
    :return: Response, list of API URLs.
    '''
    api_urls = {
        'Create a new user': '/register',
        'Log-in': '/login',
        'Log-out': '/logout',

        'Save Game Board': '/save_board',
        'Delete Game Board': '/delete_board',
        'Share': '/share',
        'Saved Game Boards': '/saved_boards/<str:user_id>/<str:token>',
        'Load Game Board': '/load_board'

    }
    return Response(api_urls)


@api_view(['POST'])
def register(request):
    """
    POST Request with Username, Password, and E-mail
    Returns token

    :param self:
    :return:
    """
    # user_name == user_id
    REQUIRED_FIELDS = ['user_name', 'password1', 'password2', 'email']

    # Check if the post request contain the required fields
    if REQUIRED_FIELDS != list(request.data.keys()):
        return Response({'error': str('Missing required fields!')}, status=status.HTTP_400_BAD_REQUEST)

    # POST Request content
    data = request.data

    # Check if passwords match
    if data['password1'] != data['password2']:
        return Response({'error': str('Passwords does not match!')}, status=status.HTTP_400_BAD_REQUEST)

    # Here ask db if this username or e-mail already exist
    # if DB says yes, return error, else proceed
    if db.user_or_email_exist(data['user_name'], data['email']):
        return Response({'error': str('User or e-mail already exist!')}, status=status.HTTP_406_NOT_ACCEPTABLE)

    # Here ask db to create a new user with its token
    token = str(uuid.uuid1())
    if not db.create_user(data['user_name'], data['password1'], data['email'], token):
        return Response({'error': str('Error when creating the account!')}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'status': 'User Successfully Created!', 'token': token})


@api_view(['POST'])
def login(request):
    """
    POST request with Username and Password
    Returns token

    :param self:
    :return:
    """
    # user_name == user_id
    REQUIRED_FIELDS = ['user_id', 'password']

    # Check if the post request contain the required fields
    if REQUIRED_FIELDS != list(request.data.keys()):
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

    return Response({'status': 'User Successfully Logged-in!', 'token': token})


@api_view(['POST'])
def logout(request):
    """
    :param self:
    :return:
    """
    # user_name == user_id
    REQUIRED_FIELDS = ['user_id', 'token']

    # Check if the post request contain the required fields
    if REQUIRED_FIELDS != list(request.data.keys()):
        return Response({'error': str('Missing required fields!')}, status=status.HTTP_400_BAD_REQUEST)

    # POST Request content
    data = request.data

    # Here check if user_id matches the token with the database
    if not db.check_user(data['user_id'], data['token']):
        return Response({'error': str('UNAUTHORIZED')}, status=status.HTTP_401_UNAUTHORIZED)

    # Here let db know we are logging out by removing user's token
    # db.remove_token(user_id)
    if not db.remove_token(data['token']):
        return Response({'error': str('Error when logging out!')}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'status': 'User Successfully Logged-out!'})


@api_view(['POST'])
def save_board(request):
    """
    :param self:
    :return:
    """
    REQUIRED_FIELDS = ['user_id', 'game_id', 'token']

    # Check if the post request contain the required fields
    if REQUIRED_FIELDS != list(request.data.keys()):
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

    return Response({'status':'Game is Successfully Saved!'})


@api_view(['POST'])
def delete_board(request):
    """
    :param self:
    :return:
    """
    REQUIRED_FIELDS = ['user_id', 'game_id', 'token']

    # Check if the post request contain the required fields
    if REQUIRED_FIELDS != list(request.data.keys()):
        return Response({'error': str('Missing required fields!')}, status=status.HTTP_400_BAD_REQUEST)

    # POST Request content
    data = request.data

    # Here check if user_id matches the token with the database
    if not db.check_user(data['user_id'], data['token']):
        return Response({'error': str('UNAUTHORIZED')}, status=status.HTTP_401_UNAUTHORIZED)

    # Here delete the game board from user's saved profile
    if not db.delete_game(data['user_id'], data['game_id']):
        return Response({'error': str('Error when deleting the game!')}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'status': 'Game is Successfully Deleted!'})


@api_view(['POST'])
def share(request):
    """
    :param self:
    :return:
    """
    REQUIRED_FIELDS = ['source_user_id', 'dest_user_id', 'game_id', 'token']

    # Check if the post request contain the required fields
    if REQUIRED_FIELDS != list(request.data.keys()):
        return Response({'error': str('Missing required fields!')}, status=status.HTTP_400_BAD_REQUEST)

    # POST Request content
    data = request.data

    # Here check if user_id matches the token with the database
    if not db.check_user(data['source_user_id'], data['token']):
        return Response({'error': str('UNAUTHORIZED')}, status=status.HTTP_401_UNAUTHORIZED)

    # Here check if dest_user_id is accepting shared content
    if not db.check_user_share_setting(data['dest_user_id']):
        return Response({'error': str('NOT ALLOWED')}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # Here call db to copy saved game board from source_user_id to dest_user_id
    # This database call just copies the saved board into dest_user_id's saved game boards
    if not db.share_game_board(data['source_user_id'], data['dest_user_id'], data['game_id']):
        return Response({'error': str('Error when sharing the game!')}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Note that this could also be multiple db calls where first you give me a game board and allow me to
    # call db.save_game(dest_user_id, board)

    return Response({'status': 'Content is Successfully Shared!'})


@api_view(['GET'])
def saved_boards(request, user_id, token):
    """

    :param request:
    :return:
    """

    # Here check if user_id matches the token with the database
    if not db.check_user(user_id, token):
        return Response({'error': str('UNAUTHORIZED')}, status=status.HTTP_401_UNAUTHORIZED)

    # Get list of game board IDs of user's saved game boards so that
    # user later can use these ids on other API calls
    # saved_game_board_ids = json.loads(json_util.dumps(db.list_user_games(user_id)))
    saved_game_board_ids = db.list_user_games(user_id)

    return Response({'saved_games': saved_game_board_ids})


@api_view(['POST'])
def load_board(request):
    """
    :param self:
    :return:
    """
    REQUIRED_FIELDS = ['user_id', 'game_id', 'token']

    # Check if the post request contain the required fields
    if REQUIRED_FIELDS != list(request.data.keys()):
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
    # User can just keep creating new active games from the saved board.
    # So we possibly as of now don't need to update stuff in user's saved board
    # But we can use the update stuff once we have more functionality going.
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
