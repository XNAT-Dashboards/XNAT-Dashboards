from xnat_dashboards.app import app
from xnat_dashboards import config
import os

config.PICKLE_PATH = os.path.abspath('xnat_dashboards/config/general.pickle')
config.DASHBOARD_CONFIG_PATH = os.path.abspath(
    'xnat_dashboards/config/dashboard_config.json')


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
        'xnat_dashboards.data_cleaning.'
        'graph_generator.GraphGenerator.__init__',
        return_value=None)

    mocker.patch(
        'xnat_dashboards.data_cleaning.graph_generator.'
        'GraphGenerator.graph_generator',
        return_value=[[], []])

    mocker.patch(
        'xnat_dashboards.data_cleaning.graph_generator.'
        'GraphGenerator.project_list_generator',
        return_value=[[], []])

    mocker.patch(
        'xnat_dashboards.data_cleaning.graph_generator.'
        'GraphGeneratorPP.__init__',
        return_value=None)

    mocker.patch(
        'xnat_dashboards.data_cleaning.graph_generator.'
        'GraphGeneratorPP.graph_generator',
        return_value=None)

    mocker.patch(
        'xnat_dashboards.data_cleaning.graph_generator.'
        'GraphGenerator.graph_generator_longitudinal',
        return_value=[])

    data_post_login_dash_present = dict(username='testUser',
                                        password='testPassword',
                                        server='CENTRAL XNAT',
                                        server_url='https://central.xnat.org',
                                        ssl=False,
                                        DB=True)

    response_post = app.test_client().post('auth/db/login/',
                                           data=data_post_login_dash_present,
                                           ).status_code

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
