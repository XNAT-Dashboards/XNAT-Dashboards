from pyxnat_interface import data_fetcher_pp

fetch_object_connected = data_fetcher_pp.Fetcher(
    name='testUser',
    password='testPassword',
    server='https://central.xnat.org',
    ssl=False)

fetch_object_conn_pwd_incorrect = data_fetcher_pp.Fetcher(
    name='testUser',
    password='testPaword',
    server='https://central.xnat.org',
    ssl=False)

fetch_object_conn_uri_incorrect = data_fetcher_pp.Fetcher(
    name='testUser',
    password='testPassword',
    server='https://central.xnat.org/',
    ssl=False)

fetch_object_conn_url_incorrect = data_fetcher_pp.Fetcher(
    name='testUser',
    password='testPassword',
    server='https://centrat.org/',
    ssl=False)

p = 'CENTRAL_OASIS_CS'


def test_project_details():

    assert type(fetch_object_connected.get_project_details(p)) == list
    assert fetch_object_conn_pwd_incorrect.get_project_details(p) == 401
    assert fetch_object_conn_uri_incorrect.get_project_details(p) == 500
    assert fetch_object_conn_url_incorrect.get_project_details(p) == 1


def test_subject_details():

    assert type(fetch_object_connected.get_subjects_details(p)) == list
    assert fetch_object_conn_pwd_incorrect.get_subjects_details(p) == 401
    assert fetch_object_conn_uri_incorrect.get_subjects_details(p) == 500
    assert fetch_object_conn_url_incorrect.get_subjects_details(p) == 1


def test_experiments_details():

    assert type(fetch_object_connected.get_experiments_details(p)) == list
    assert fetch_object_conn_pwd_incorrect.get_experiments_details(p) == 401
    assert fetch_object_conn_uri_incorrect.get_experiments_details(p) == 500
    assert fetch_object_conn_url_incorrect.get_experiments_details(p) == 1


def test_scans_details():

    assert type(fetch_object_connected.get_scans_details(p)) == list
    assert fetch_object_conn_pwd_incorrect.get_scans_details(p) == 401
    assert fetch_object_conn_uri_incorrect.get_scans_details(p) == 500
    assert fetch_object_conn_url_incorrect.get_scans_details(p) == 1
