from pyxnat_connection import data_fetcher

fetch_object = data_fetcher.Fetcher(name='testUser',
                                    password='testPassword',
                                    instance_url='https://central.xnat.org')


def test_get_project_details():

    assert type(fetch_object.get_projects_details())\
           == dict or fetch_object.get_projects_details()\
           == 1, "Correct"


def test_get_experiments_details():

    assert type(fetch_object.get_experiments_details())\
           == dict or fetch_object.get_experiments_details()\
           == 1, "Correct"


def test_get_scan_details():

    assert type(fetch_object.get_scans_details())\
           == dict or fetch_object.get_scans_details()\
           == 1, "Correct"
