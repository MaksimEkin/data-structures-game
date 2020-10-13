from game_board_db import *

# Example Usage
if __name__ == '__main__':
    for ranked in get_rankings():
        pprint.pprint(ranked)
