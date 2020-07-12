from saved_data_processing import graph_generator_pp_DB
import json
import pathlib
from utils import input_processor
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

graph_object = graph_generator_pp_DB.GraphGenerator(
        'testUser', existing_user['info'], 'CENTRAL_OASIS_CS')


def test_graph_preprocessor():

    assert type(graph_object.graph_pre_processor()) == dict


def test_graph_generator():

    assert type(graph_object.graph_generator()) == list
