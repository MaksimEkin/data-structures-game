from game_board.mock import MockDB

"""
This is the mock of the user profile database function calls.
"""


def user_or_email_exist(user_name, email):
    return False


def create_user(user_name, password1, email, token):
    return True


def login(user_id, password):
    return True


def update_token(user_id, token):
    return True


def check_user(user_id, token):
    return True


def remove_token(user_id):
    return True


def save_game(user_id, board):
    return True


def delete_game(user_id, game_id):
    return True


def check_user_share_setting(dest_user_id):
    return True


def share_game_board(source_user_id, dest_user_id, game_id):
    return True


def list_user_games(user_id):
    return ['id1', 'id2']


def load_board(user_id, game_id):
    return MockDB.read_game(game_id)