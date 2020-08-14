from xnat_dashboards.pyxnat_interface import data_fetcher

fetch_object_connected = data_fetcher.Fetcher(
    name='testUser',
    password='testPassword',
    server='https://central.xnat.org',
    ssl=False)

fetch_object_conn_pwd_incorrect = data_fetcher.Fetcher(
    name='testUser',
    password='testPaword',
    server='https://central.xnat.org',
    ssl=False)

fetch_object_conn_uri_incorrect = data_fetcher.Fetcher(
    name='testUser',
    password='testPassword',
    server='https://central.xnat.org/',
    ssl=False)

fetch_object_conn_url_incorrect = data_fetcher.Fetcher(
    name='testUser',
    password='testPassword',
    server='https://centrat.org/',
    ssl=False)


def test_project_details():

    assert type(fetch_object_connected.get_projects_details()) == list
    assert fetch_object_conn_pwd_incorrect.get_projects_details() == 401
    assert fetch_object_conn_uri_incorrect.get_projects_details() == 500
    assert fetch_object_conn_url_incorrect.get_projects_details() == 1


def test_subject_details():

    assert type(fetch_object_connected.get_subjects_details()) == list
    assert fetch_object_conn_pwd_incorrect.get_subjects_details() == 401
    assert fetch_object_conn_uri_incorrect.get_subjects_details() == 500
    assert fetch_object_conn_url_incorrect.get_subjects_details() == 1


def test_experiments_details():

    assert type(fetch_object_connected.get_experiments_details()) == list
    assert fetch_object_conn_pwd_incorrect.get_experiments_details() == 401
    assert fetch_object_conn_uri_incorrect.get_experiments_details() == 500
    assert fetch_object_conn_url_incorrect.get_experiments_details() == 1


def test_scans_details():

    assert type(fetch_object_connected.get_scans_details()) == list
    assert fetch_object_conn_pwd_incorrect.get_scans_details() == 401
    assert fetch_object_conn_uri_incorrect.get_scans_details() == 500
    assert fetch_object_conn_url_incorrect.get_scans_details() == 1
