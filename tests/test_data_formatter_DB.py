from saved_data_processing import data_formatter_DB
from pymongo import MongoClient
import json


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

formatter_object_connected = data_formatter_DB.Formatter(
    'testUser', existing_user['info'])


def test_get_projects_details():

    project_details = formatter_object_connected.get_projects_details()

    assert type(project_details['Number of Projects']) == int
    assert type(project_details['Imaging Sessions']) == dict
    assert type(project_details['Projects Visibility']) == dict
    assert type(project_details['Sessions types/Project']) == dict


def test_get_subjects_details():

    subject_details = formatter_object_connected.get_subjects_details()

    assert type(subject_details['Number of Subjects']) == int
    assert type(subject_details['Age Range']) == dict
    assert type(subject_details['Gender']) == dict
    assert type(subject_details['Handedness']) == dict
    assert type(subject_details['Subjects/Project']) == dict


def test_get_experiments_details():

    experiment_details = formatter_object_connected.get_experiments_details()

    assert type(experiment_details['Number of Experiments']) == int
    assert type(experiment_details['Experiments/Subject']) == dict
    assert type(experiment_details['Experiments/Project']) == dict
    assert type(experiment_details['Experiment Types']) == dict


def test_get_scans_details():

    experiment_details = formatter_object_connected.get_scans_details()

    assert type(experiment_details['Number of Scans']) == int
    assert type(experiment_details['Scans/Subject']) == dict
    assert type(experiment_details['Scans/Project']) == dict
    assert type(experiment_details['Scans Quality']) == dict
    assert type(experiment_details['Scan Types']) == dict
    assert type(experiment_details['XSI Scan Types']) == dict
