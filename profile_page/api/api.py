from rest_framework.decorators import api_view
from rest_framework.response import Response
# Status codes documentation: https://www.django-rest-framework.org/api-guide/status-codes/
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from game_board.database import game_board_db as db
from game_board.api import utils
import uuid
import json

# @permission_classes([IsAuthenticated])
# from rest_framework.authtoken.models import Token

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

    # TODO: Here ask db if this username or e-mail already exist
    # db.user_or_email_exist(user_name, email)
    # if DB says yes, return error, else proceed

    # TODO: Here ask db to create a new user with its token
    token = str(uuid.uuid1())
    # db.create_user(user_name, password1, email, token)

    return Response({'status': 'User Successfully Created!', 'token':token})


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

    # TODO: Here ask db if username and password works out
    # db.login(user_id, password)
    # if db says nope, return error. else proceed.

    # TODO: Here let db know of the new token that user owns
    token = str(uuid.uuid1())
    # db.update_token(user_id, token)

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

    # TODO: Here check if user_id matches the token with the database
    # db.check_user(user_id, token)

    # TODO: Here let db know we are logging out by removing user's token
    # db.remove_token(user_id)

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

    # TODO: Here check if user_id matches the token with the database
    # db.check_user(user_id, token)

    # Load the game board from the database
    response_status = utils.load_board_db(data['game_id'])
    if response_status['error']:
        return Response({'error': response_status['reason']},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    board = response_status['game_board']

    # TODO: Here append new game board to user's profile. Note that this board already have an ID.
    # db.save_game(user_id, board)
    # possibly return ('No space left to save')

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

    # TODO: Here check if user_id matches the token with the database
    # db.check_user(user_id, token)

    # TODO: Here delete the game board from user's saved profile
    # db.delete_game(user_id, board)
    # possibly return ('Game not found')

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

    # TODO: Here check if source_user_id matches the token with the database
    # db.check_user(source_user_id, token)

    # TODO: Here check if dest_user_id is accepting shared content
    # db.check_user_share_setting(dest_user_id)

    # TODO: Here call db to copy saved game board from source_user_id to dest_user_id
    # db.share_game_board(source_user_id, dest_user_id, game_id)
    # Note that this could also be multiple db calls where first you give me a game board and allow me to
    # call db.save_game(dest_user_id, board)

    return Response({'status': 'Content is Successfully Shared!'})



@api_view(['GET'])
def saved_boards(request, user_id, token):
    """

    :param request:
    :return:
    """

    # TODO: Here check user_id is authenticated with token on db
    # db.check_user(user_id, token)

    try:
        # TODO: Make sure DB returns list of game board IDs here
        saved_game_board_ids =  json.loads(json_util.dumps(db.list_user_games(user_id)))

    except Exception as e:
        return Response({'error': str('Error in the Database!')}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

    # TODO: Here check if user_id matches the token with the database
    # db.check_user(user_id, token)

    # TODO: Load the game from user's saved profile
    # game_board = db.load_board(user_id, game_id)

    # TODO: here I am just going to move this board to active games using the api we already have.
    # Note that board is still saved on user's profile, but we are just creating a new active game.
    # User can just keep creating new active games from the saved board.
    # So we possibly as of now don't need to update stuff in user's saved board
    # But we can use the update stuff once we have more functionality going.

    # TODO: here i am just going to return the game board from the active games
    # From this point front-end can continue using the Game Board API to interact with the game
    pass


