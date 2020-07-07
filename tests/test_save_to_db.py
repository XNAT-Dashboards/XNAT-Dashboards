from pyxnat_db import save_to_db
import json
from pymongo import MongoClient


def test_save_data_and_user():

    username = 'testUser'
    password = 'testPassword'
    server = 'https://central.xnat.org'
    ssl = False
    test = True

    saving_object = save_to_db.SaveToDb(username,
                                        password,
                                        server,
                                        ssl,
                                        test)
    saving_object.save_data()

    try:
        with open('utils/db_config.json') as json_file:
            db_json = json.load(json_file)
    except OSError:
        print("db_json not found")
        exit(1)

    client = MongoClient(db_json['test_url'])
    db = client[db_json['test_db']]

    ex_user = db.users_data.find_one({'username': 'testUser'})

    assert type(ex_user['info']) == dict
    assert type(ex_user['project_list']['project_list']) == list
    assert type(ex_user['project_list']['project_list_ow_co_me']) == list

    # Save user

    saving_object.save_user(username, password, server, ssl)

    ex_user = db.users.find_one({'username': 'testUser'})

    assert ex_user['username'] == 'testUser'
    assert ex_user['password'] == 'testPassword'
    assert ex_user['server'] == 'https://central.xnat.org'
    assert ex_user['ssl'] is False
