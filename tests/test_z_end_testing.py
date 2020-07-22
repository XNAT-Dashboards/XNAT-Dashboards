from pymongo import MongoClient
import sys
import os
import json
from os.path import dirname, abspath
sys.path.insert(0, dirname(dirname(abspath(__file__))))


def test_end_testing():

    with open('utils/db_config.json') as json_file:
        db_json = json.load(json_file)

    client = MongoClient(db_json['test_url'])
    db2 = client['test_xnat_dashboards']

    db2.users.remove({'role': 'guest'})
    db2.users_data.remove({'role': 'guest'})

    os.remove('pickles/users_data/guest.pickle')
    os.remove('pickles/resources/guest.pickle')
    os.remove('pickles/resources/guestbbrc.pickle')

    assert True
