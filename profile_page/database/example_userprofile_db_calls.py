from profile_page_db import *

# Example Usage
if __name__ == '__main__':
    board = {"game_id": "60afce36-085a-11eb-b6ab-acde48001122","graph": {"nodes": "node4(node2(node3)(node1))(node6(node5))","node_points": {"node1": 1,"node2": 2,"node3": 3,"node4": 4,"node5": 5,"node6": 6},"gold_node": "node5","balanced": True},"player_ids": ["id2","id3","id4","id5"],"player_names": ["naomi","kulsoom","nick","ryan"],"player_points": {"id2": 2,"id3": 2,"id4": 3,"id5": 10},"turn": "id2","cards": {"id2": ["card1","card2","card3"],"id3": ["card1","card2","card3"],"id4":["card1","card2","card3"],"id5": ["card1","card2","card3"]},"gold_node": False,"difficulty": "Medium","num_players": 4,"online": True,"curr_data_structure": "AVL","selected_data_structures": ["AVL","Stack"],"timed_game": False,"seconds_until_next_ds": 60,"time_created": "07/10/2020 00:05:47","end_game": False}
    board2 = {"game_id": "60afce36-085a-11eb-b6ab-acde48001122","graph": {"nodes": "DID ITnode4(node2(node3)(node1))(node6(node5))","node_points": {"node1": 1,"node2": 2,"node3": 3,"node4": 4,"node5": 5,"node6": 6},"gold_node": "node5","balanced": True},"player_ids": ["changed player","id3","id4","id5"],"player_names": ["naomi","kulsoom","nick","ryan"],"player_points": {"id2": 2,"id3": 2,"id4": 3,"id5": 10},"turn": "id2","cards": {"id2": ["card1","card2","card3"],"id3": ["card1","card2","card3"],"id4":["card1","card2","card3"],"id5": ["card1","card2","card3"]},"gold_node": False,"difficulty": "Medium","num_players": 4,"online": True,"curr_data_structure": "AVL","selected_data_structures": ["AVL","Stack"],"timed_game": False,"seconds_until_next_ds": 60,"time_created": "07/10/2020 00:05:47","end_game": False}

    new_graph = {"nodes": "DID IT WRETITREE ???5))"}
    user = {"user_id":"5f7d1b1d8fd2b816c48c148b","badges":[31,24,83],"current_story_level":9,"email":"ryanb777@umbc.edu","friends":["Kulsoom2","Nick2","Maksim2","Naomi2"],"user_name":"ryan2","password_hash":"well,hello there","points":98274,"rank":"diamond","save_games":[board,"4(2(3)(1))(6(5))","4(2(3)(1))(6(5))"]}
    remove_user(user)
    create_user(user)
    #print(update_user_game(user["user_id"], board["game_id"], board2))
    
    #print(find_user_game(user["user_id"], board["game_id"], board2))
    #print(list_user_games(user["user_id"]))
   # print(find_user_game_graph(user["user_id"], board["game_id"], new_graph))

    updated_user = update_user_game( user["user_id"], "This name should really not exist in the database, and if it does, YEESH!", board2)

    print(updated_user)
