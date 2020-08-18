from xnat_dashboards.app import app
from xnat_dashboards import path_creator
import os

path_creator.set_pickle_path(os.path.abspath(
    'xnat_dashboards/pickles/data/general.pickle'))
path_creator.set_dashboard_config_path(os.path.abspath(
    'xnat_dashboards/config/dashboard_config.json'))


def test_login_db():

    respone_get = app.test_client().get('auth/db/login/')
    assert respone_get.status_code == 200


def test_logout():

    # Checks if we are getting redirected to login through logout
    logout = app.test_client().get('dashboards/logout/',
                                   follow_redirects=True).status_code

    assert logout == 200


def test_home_redirect():
    response_post = app.test_client().get('/',
                                          follow_redirects=True).status_code
    # Checks if we are getting correct response that is 200
    # after redirecting
    response_post == 200


def test_dashboard_db(mocker):

    mocker.patch(
        'xnat_dashboards.saved_data_processing.'
        'graph_generator_DB.GraphGenerator.__init__',
        return_value=None)

    mocker.patch(
        'xnat_dashboards.saved_data_processing.graph_generator_DB.'
        'GraphGenerator.graph_generator',
        return_value=[[], []])

    mocker.patch(
        'xnat_dashboards.saved_data_processing.graph_generator_DB.'
        'GraphGenerator.project_list_generator',
        return_value=[[], []])

    mocker.patch(
        'xnat_dashboards.saved_data_processing.graph_generator_DB.'
        'GraphGeneratorPP.__init__',
        return_value=None)

    mocker.patch(
        'xnat_dashboards.saved_data_processing.graph_generator_DB.'
        'GraphGeneratorPP.graph_generator',
        return_value=None)

    mocker.patch(
        'xnat_dashboards.saved_data_processing.graph_generator_DB.'
        'GraphGenerator.graph_generator_longitudinal',
        return_value=[])

    data_post_login_dash_present = dict(username='testUser',
                                        password='testPassword',
                                        server='https://central.xnat.org',
                                        ssl=False,
                                        DB=True)

    response_post = app.test_client().post('auth/db/login/',
                                           data=data_post_login_dash_present,
                                           ).status_code

    data_post_login_dash_present_pk = dict(username='testUser',
                                           password='testPassword',
                                           server='https://central.xnat.org',
                                           ssl=False,
                                           DB=True)

    response_post_pk = app.test_client().post(
        'auth/db/login/',
        data=data_post_login_dash_present_pk).status_code

    assert response_post_pk == 302  # Redirects

    with app.test_client() as c:
        with c.session_transaction() as sess:
            sess['server'] = 'https://central.xnat.org'
            sess['role_exist'] = 'guest'
            sess['username'] = 'testUser'
            sess['project_visible'] = '*'

        response_get_pp = c.\
            get('dashboards/db/project/CENTRAL_OASIS_CS').status_code

        response_get_stats = c.\
            get('dashboards/db/stats/').status_code

    assert response_get_pp == 200

    assert response_post == 302  # Redirects to dashboards

    response_get = app.test_client().get('dashboards/db/stats/').status_code

    assert response_get == 302

    assert response_get_stats == 200
