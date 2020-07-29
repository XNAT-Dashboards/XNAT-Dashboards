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

    db2.resources.remove({'server': 'https://central.xnat.org'})
    db2.users_data.remove({'server': 'https://central.xnat.org'})

    os.remove('pickles/users_data/general.pickle')
    os.remove('pickles/resources/general.pickle')
    os.remove('pickles/resources/generalbbrc.pickle')

    assert True
