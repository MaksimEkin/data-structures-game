from pymongo import MongoClient
import pprint
import os

DATABASE_URL1 = os.environ.get('DATABASE_URL1')


print("\nTesting DB connection")
#print(DATABASE_URL1)

client = MongoClient(DATABASE_URL1)

db = client.test_database
test_document = {"tester": "Ryan", "information": "My first DB test!", "list_test": ["Pandamic", "CMSC 447", "pymongo"]}
test_collection = db.test_collection
test_document_id = test_collection.insert_one(test_document).inserted_id

print("test_document_id =",test_document_id)

print()
returned_data = test_collection.find_one({"tester": "Ryan"})
pprint.pprint(returned_data)
print()
