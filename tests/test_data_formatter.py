from realtime_data_processing import data_formatter

formatter_object_connected = data_formatter.Formatter(
    name='testUser',
    password='testPassword',
    server='https://central.xnat.org',
    ssl=False)

formatter_object_conn_pwd_incorrect = data_formatter.Formatter(
    name='testUser',
    password='testPaword',
    server='https://central.xnat.org',
    ssl=False)

formatter_object_conn_uri_incorrect = data_formatter.Formatter(
    name='testUser',
    password='testPassword',
    server='https://central.xnat.org/',
    ssl=False)

formatter_object_conn_url_incorrect = data_formatter.Formatter(
    name='testUser',
    password='testPassword',
    server='https://centrat.org/',
    ssl=False)


def test_get_projects_details():

    project_details = formatter_object_connected.get_projects_details()

    assert type(project_details['Number of Projects']) == int
    assert type(project_details['Projects Visibility']) == dict
    assert formatter_object_conn_pwd_incorrect.get_projects_details() == 401
    assert formatter_object_conn_uri_incorrect.get_projects_details() == 500
    assert formatter_object_conn_url_incorrect.get_projects_details() == 1


def test_get_subjects_details():

    subject_details = formatter_object_connected.get_subjects_details()

    assert type(subject_details['Number of Subjects']) == int
    assert type(subject_details['Age Range']) == dict
    assert type(subject_details['Gender']) == dict
    assert type(subject_details['Handedness']) == dict
    assert type(subject_details['Subjects/Project']) == dict
    assert formatter_object_conn_pwd_incorrect.get_subjects_details() == 401
    assert formatter_object_conn_uri_incorrect.get_subjects_details() == 500
    assert formatter_object_conn_url_incorrect.get_subjects_details() == 1


def test_get_experiments_details():

    experiment_details = formatter_object_connected.get_experiments_details()

    assert type(experiment_details['Number of Experiments']) == int
    assert type(experiment_details['Experiments/Subject']) == dict
    assert type(experiment_details['Experiments/Project']) == dict
    assert type(experiment_details['Experiment Types']) == dict
    assert formatter_object_conn_pwd_incorrect.get_experiments_details() == 401
    assert formatter_object_conn_uri_incorrect.get_experiments_details() == 500
    assert formatter_object_conn_url_incorrect.get_experiments_details() == 1


def test_get_scans_details():

    experiment_details = formatter_object_connected.get_scans_details()

    assert type(experiment_details['Number of Scans']) == int
    assert type(experiment_details['Scans/Subject']) == dict
    assert type(experiment_details['Scans/Project']) == dict
    assert type(experiment_details['Scans Quality']) == dict
    assert type(experiment_details['Scan Types']) == dict
    assert type(experiment_details['XSI Scan Types']) == dict
    assert formatter_object_conn_pwd_incorrect.get_scans_details() == 401
    assert formatter_object_conn_uri_incorrect.get_scans_details() == 500
    assert formatter_object_conn_url_incorrect.get_scans_details() == 1
