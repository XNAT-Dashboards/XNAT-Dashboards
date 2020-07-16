from saved_data_processing import graph_generator_DB
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

graph_object = graph_generator_DB.GraphGenerator(
    'testUser', existing_user['info'])


def test_graph_type_generator():

    input_processor.set_keyboard_input(['bar', 'bar', 'bar', 'bar',
                                        'bar', 'bar', 'bar', 'bar',
                                        'bar', 'bar', 'bar', 'bar',
                                        'bar', 'bar', 'bar', 'bar',
                                        'bar', 'bar', 'bar'])
    graph_object.graph_type_generator()

    assert pathlib.Path('utils/graph_type.json').exists


def test_graph_preprocessor():

    assert type(graph_object.graph_pre_processor()) == dict


def test_graph_generator():

    assert type(graph_object.graph_generator()) == list


def test_project_list_generator():

    project_list = graph_object.project_list_generator()
    assert type(project_list) == list
    assert type(project_list[0]) == list
    assert type(project_list[1]) == list
