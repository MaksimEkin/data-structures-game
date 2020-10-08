from pymongo import MongoClient
import os

def create_user(user_data):
    user_email = user_data['email']

    DATABASE_URL1 = os.environ.get('DATABASE_URL1' )
    client = MongoClient(DATABASE_URL1)

    User_collection = client.InitialDB.User_profile
    returned_data = User_collection.find_one({"email": user_email})
    if returned_data is None:
        return User_collection.insert_one(user_data)
    else:
        return 'nah bro idk about it'

'''
# Example Usage
if __name__ == '__main__':
    user = {'badges': [31, 24, 83],
     'current story level': 9,
     'email': 'ryanb777@umbc.edu',
     'friends': ['Kulsoom2', 'Nick2', 'Maksim2', 'Naomi2'],
     'id': 34456,
     'name': 'ryan2',
     'password hash': 'well,hello there',
     'points': 98274,
     'rank': 'diamond',
     'save games': ['4(2(3)(no))(6(5))', '4(2(3)(1))(6(5))', '4(2(3)(1))(6(5))']}

    print(create_user(user))
'''
