from save_endpoint import save_to_db
import json
from pymongo import MongoClient


def test_save_data_and_user(mocker):

    username = 'testUser'
    password = 'testPassword'
    server = 'https://central.xnat.org'
    ssl = False
    role = 'guest'
    test = True

    saving_object = save_to_db.SaveToDb(username,
                                        password,
                                        server,
                                        ssl,
                                        role,
                                        test)

    resource_return_value = {'date': '28', 'resources': 'test'}
    data_return_value = {'info': 'data'}

    mocker.patch(
        'pyxnat_interface.data_fetcher.FetcherLong.get_resources',
        return_value=resource_return_value)

    mocker.patch(
        'pyxnat_interface.data_fetcher.FetcherLong.get_experiment_resources',
        return_value=resource_return_value)

    mocker.patch(
        'pyxnat_interface.data_fetcher.Fetcher.fetch_all',
        return_value=data_return_value)

    saving_object.save_data()

    try:
        with open('utils/db_config.json') as json_file:
            db_json = json.load(json_file)
    except OSError:
        print("db_json not found")
        exit(1)

    client = MongoClient(db_json['test_url'])
    db = client[db_json['test_db']]

    existing_user = db.users_data.find_one({'role': 'guest'})

    assert type(existing_user['info']) == dict

    saving_object.save_resources()

    res = db.resources.find_one({'role': 'guest'})

    assert type(res) == dict

    res_bbrc = db.resources.find_one({'role': 'guest'})

    assert type(res_bbrc) == dict
