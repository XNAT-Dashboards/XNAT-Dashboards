from saved_data_processing import get_info_DB
import json
from pymongo import MongoClient


# Code for fetching data from DB
try:
    with open('utils/db_config.json') as json_file:
        db_json = json.load(json_file)
except OSError:
    print("db_json not found")
    exit(1)

client = MongoClient(db_json['url'])
db = client[db_json['db']]
existing_user = db.users_data.find_one({'username': 'testUser'})

info_object = get_info_DB.GetInfo(
        'testUser', existing_user['info'], None)


def test_info():

    info = info_object.get_info()

    assert type(info) == dict   # Return type should be a dict
    assert len(info) == 16      # Currently 16 dicts to be returned
