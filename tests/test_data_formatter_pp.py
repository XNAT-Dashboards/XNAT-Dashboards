from pyxnat_api import data_formatter_pp


formatter_object_connected = data_formatter_pp.Formatter(
    username='testUser',
    password='testPassword',
    server='https://central.xnat.org',
    ssl=False,
    project_id='CENTRAL_OASIS_CS')

formatter_object_conn_pwd_incorrect = data_formatter_pp.Formatter(
    username='testUser',
    password='testPaword',
    server='https://central.xnat.org',
    ssl=False,
    project_id='CENTRAL_OASIS_CS')

formatter_object_conn_uri_incorrect = data_formatter_pp.Formatter(
    username='testUser',
    password='testPassword',
    server='https://central.xnat.org/',
    ssl=False,
    project_id='CENTRAL_OASIS_CS')

formatter_object_conn_url_incorrect = data_formatter_pp.Formatter(
    username='testUser',
    password='testPassword',
    server='https://centrat.org/',
    ssl=False,
    project_id='CENTRAL_OASIS_CS')


def test_get_projects_details():

    project_details = formatter_object_connected.get_projects_details()

    assert type(project_details['Imaging Sessions']) == dict
    assert type(project_details['Total Sessions']) == int
    assert type(project_details['user(s)']) == list
    assert type(project_details['member(s)']) == list
    assert type(project_details['Collaborator(s)']) == list
    assert type(project_details['Owner(s)']) == list
    assert type(project_details['last_accessed(s)']) == list
    assert type(project_details['insert_user(s)']) == str
    assert type(project_details['insert_date']) == str
    assert type(project_details['access']) == str
    assert type(project_details['name']) == str
    assert type(project_details['last_workflow']) == str
    assert formatter_object_conn_pwd_incorrect.get_projects_details() == 401
    assert formatter_object_conn_uri_incorrect.get_projects_details() == 500
    assert formatter_object_conn_url_incorrect.get_projects_details() == 1


def test_get_subjects_details():

    subject_details = formatter_object_connected.get_subjects_details()

    assert type(subject_details['Number of Subjects']) == int
    assert type(subject_details['Age Range']) == dict
    assert type(subject_details['Gender']) == dict
    assert type(subject_details['Handedness']) == dict
    assert formatter_object_conn_pwd_incorrect.get_subjects_details() == 401
    assert formatter_object_conn_uri_incorrect.get_subjects_details() == 500
    assert formatter_object_conn_url_incorrect.get_subjects_details() == 1


def test_get_experiments_details():

    experiment_details = formatter_object_connected.get_experiments_details()

    assert type(experiment_details['Number of Experiments']) == int
    assert type(experiment_details['Experiments/Subject']) == dict
    assert type(experiment_details['Experiment Types']) == dict
    assert formatter_object_conn_pwd_incorrect.get_experiments_details() == 401
    assert formatter_object_conn_uri_incorrect.get_experiments_details() == 500
    assert formatter_object_conn_url_incorrect.get_experiments_details() == 1


def test_get_scans_details():

    experiment_details = formatter_object_connected.get_scans_details()

    assert type(experiment_details['Number of Scans']) == int
    assert type(experiment_details['Scans/Subject']) == dict
    assert type(experiment_details['Scans Quality']) == dict
    assert type(experiment_details['Scan Types']) == dict
    assert type(experiment_details['XSI Scan Types']) == dict
    assert formatter_object_conn_pwd_incorrect.get_scans_details() == 401
    assert formatter_object_conn_uri_incorrect.get_scans_details() == 500
    assert formatter_object_conn_url_incorrect.get_scans_details() == 1
