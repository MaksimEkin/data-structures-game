from game_board_db import purge_old_games

if __name__ == '__main__':
    """
    Removes games older than a day from the mongo db
    """

    purge_old_games()
