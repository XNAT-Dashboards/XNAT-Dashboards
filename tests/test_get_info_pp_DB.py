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

info_object = get_info_DB.GetInfoPP(
    'testUser', existing_user['info'], 'CENTRAL_OASIS_CS', None)


def test_info():

    info = info_object.get_per_project_view()

    assert type(info) == dict   # Return type should be a dict
    assert len(info) == 12     # Currently 12 dicts to be returned
