"""
Removes games older than a day from the mongo db
command to run: python game_board/database/purge_old_games.py
"""
from game_board_db import purge_old_games

if __name__ == '__main__':
    purge_old_games()
