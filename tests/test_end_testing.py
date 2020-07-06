from pymongo import MongoClient
import sys
import json
from os.path import dirname, abspath
sys.path.insert(0, dirname(dirname(abspath(__file__))))    


def test_end_testing():
    try:
        with open('utils/db_config.json') as json_file:
            db_json = json.load(json_file)
    except OSError:
        print("db_json not found")
        exit(1)
    print(db_json['url'])

    client = MongoClient(db_json['url'])
    db = client['xnat_dashboards']

    db.users.remove({'username': 'testUser'})
    db.users_data.remove({'username': 'testUser'})

    client = MongoClient(db_json['test_url'])
    db2 = client['xnat_dashboards']

    db2.users.remove({'username': 'testUser'})
    db2.users_data.remove({'username': 'testUser'})

    assert True
