from pyxnat_connection import data_fetcher
import pytest

fetch_object_connected = data_fetcher.Fetcher(name='testUser',
                                            password='testPassword',
                                    instance_url='https://central.xnat.org')


fetch_object_disconnected = data_fetcher.Fetcher(name='testUser',
                                                 password='testPassword',
                                    instance_url='https://central.xnat.org')


def test_get_projects_details():

    project_details = fetch_object_connected.get_projects_details()

    assert type(project_details['number_of_projects']) == int
    assert type(project_details['project_mr_ct_pet']) == dict


def test_get_subjects_details():

    subject_details = fetch_object_connected.get_subjects_details()

    assert type(subject_details['number_of_subjects']) == int
    assert type(subject_details['age_range']) == dict
    assert type(subject_details['gender']) == dict
    assert type(subject_details['handedness']) == dict
    assert type(subject_details['subjects_per_project']) == dict


def test_get_experiments_details():

    experiment_details = fetch_object_connected.get_experiments_details()

    assert type(experiment_details['number_of_experiments']) == int
    assert type(experiment_details['experiments_per_subject']) == dict
    assert type(experiment_details['experiments_per_project']) == dict
    assert type(experiment_details['experiment_types']) == dict


def test_get_scans_details():

    experiment_details = fetch_object_connected.get_scans_details()

    assert type(experiment_details['number_of_scans']) == int
    assert type(experiment_details['scans_per_subject']) == dict
    assert type(experiment_details['scans_per_project']) == dict
    assert type(experiment_details['scans_per_experiment']) == dict
    assert type(experiment_details['scans_quality']) == dict
    assert type(experiment_details['scan_types']) == dict
    assert type(experiment_details['xsi_scan_types']) == dict


@pytest.mark.disable_socket
def test_get_details_disconnected():

    # Network access removed using pytest_socket
    assert fetch_object_disconnected.get_projects_details() == 1

    assert fetch_object_disconnected.get_subjects_details() == 1

    assert fetch_object_disconnected.get_experiments_details() == 1

    assert fetch_object_disconnected.get_scans_details() == 1
