from pyxnat_connection import data_fetcher
import pytest

fetch_object_connected = data_fetcher.Fetcher(
                                            name='testUser',
                                            password='testPassword',
                                            server='https://central.xnat.org')


fetch_object_disconnected = data_fetcher.Fetcher(
                                            name='testUser',
                                            password='testPassword',
                                            server='https://central.xnat.org')

fetch_object_disconn_pwd_incorrect = data_fetcher.Fetcher(
                                            name='testUser',
                                            password='testPaword',
                                            server='https://central.xnat.org')

fetch_object_disconn_url_incorrect = data_fetcher.Fetcher(
                                            name='testUser',
                                            password='testPassword',
                                            server='https://central.xnat.org/')


def test_get_projects_details():

    project_details = fetch_object_connected.get_projects_details()

    assert type(project_details['Number of Projects']) == int
    assert type(project_details['Total MR PET CT Sessions']) == dict
    assert type(project_details['Projects Visibility']) == dict
    assert fetch_object_disconn_pwd_incorrect.get_projects_details() == 401
    assert fetch_object_disconn_url_incorrect.get_projects_details() == 500


def test_get_subjects_details():

    subject_details = fetch_object_connected.get_subjects_details()

    assert type(subject_details['Number of Subjects']) == int
    assert type(subject_details['Age Range']) == dict
    assert type(subject_details['Gender']) == dict
    assert type(subject_details['Handedness']) == dict
    assert type(subject_details['Subjects/Project']) == dict


def test_get_experiments_details():

    experiment_details = fetch_object_connected.get_experiments_details()

    assert type(experiment_details['Number of Experiments']) == int
    assert type(experiment_details['Experiments/Subject']) == dict
    assert type(experiment_details['Experiments/Project']) == dict
    assert type(experiment_details['Experiment Types']) == dict


def test_get_scans_details():

    experiment_details = fetch_object_connected.get_scans_details()

    assert type(experiment_details['Number of Scans']) == int
    assert type(experiment_details['Scans/Subject']) == dict
    assert type(experiment_details['Scans/Project']) == dict
    assert type(experiment_details['Scans Quality']) == dict
    assert type(experiment_details['Scan Types']) == dict
    assert type(experiment_details['XSI Scan Types']) == dict


def test_get_projects_details_specific():

    assert type(fetch_object_connected.get_projects_details_specific())\
           == list
    assert fetch_object_disconn_pwd_incorrect.get_projects_details_specific() == 401
    assert fetch_object_disconn_url_incorrect.get_projects_details_specific() == 500


@pytest.mark.disable_socket
def test_get_details_disconnected():

    fetch_object_disconnected = data_fetcher.Fetcher(name='testUser',
                                                 password='testPassword',
                                            server='https://central.xnat.org')

    # Network access removed using pytest_socket
    assert fetch_object_disconnected.get_projects_details() == 1

    assert fetch_object_disconnected.get_subjects_details() == 1

    assert fetch_object_disconnected.get_experiments_details() == 1

    assert fetch_object_disconnected.get_scans_details() == 1
