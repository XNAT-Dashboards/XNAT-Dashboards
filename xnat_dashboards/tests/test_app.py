from xnat_dashboards.app import app
from xnat_dashboards import config
import os

config.PICKLE_PATH = os.path.abspath('xnat_dashboards/config/general.pickle')
config.DASHBOARD_CONFIG_PATH = os.path.abspath(
    'xnat_dashboards/config/dashboard_config.json')


def test_login(mocker):

    # Auth get methods

    # Login route test
    respone_get = app.test_client().get('auth/login/')
    assert respone_get.status_code == 200

    # If session error is not -1
    with app.test_client() as c:
        with c.session_transaction() as sess:
            sess['error'] = 'Error'

        respone_get = c.get('auth/login/')
        assert respone_get.status_code == 200

    # Auth post methods

    # Normal flow of user login

    mocker.patch(
        'xnat_dashboards.app.authentication.model.user_exists',
        return_value=34)

    data_post_login_dash_present = dict(username='testUser',
                                        password='testPassword',
                                        server='CENTRAL XNAT',
                                        server_url='https://central.xnat.org',
                                        ssl=False,
                                        DB=True)

    response_post = app.test_client().post('auth/login/',
                                           data=data_post_login_dash_present,
                                           ).status_code
    assert response_post == 302  # Redirects to dashboards

    # If user role is assigned forbidden

    data_post_login_dash_present = dict(username='tUser',
                                        password='tPassword',
                                        server='CENTRAL XNAT',
                                        server_url='https://central.xnat.org',
                                        ssl=False,
                                        DB=True)

    response_post = app.test_client().post('auth/login/',
                                           data=data_post_login_dash_present,
                                           ).status_code
    assert response_post == 302  # Redirects to login

    # Wrong username or password
    mocker.patch(
        'xnat_dashboards.app.authentication.model.user_exists',
        return_value=[])
    data_post_login_dash_present = dict(username='tUse',
                                        password='tPassword',
                                        server='CENTRAL XNAT',
                                        server_url='https://central.xnat.org',
                                        ssl=False,
                                        DB=True)

    response_post = app.test_client().post('auth/login/',
                                           data=data_post_login_dash_present,
                                           ).status_code
    assert response_post == 302  # Redirects to login

    # Role not assigned then guest is assigned

    mocker.patch(
        'xnat_dashboards.app.authentication.model.user_exists',
        return_value=34)
    data_post_login_dash_present = dict(username='userNew',
                                        password='tPassword',
                                        server='CENTRAL XNAT',
                                        server_url='https://central.xnat.org',
                                        ssl=False,
                                        DB=True)

    response_post = app.test_client().post('auth/login/',
                                           data=data_post_login_dash_present,
                                           ).status_code

    assert response_post == 302


def test_logout(mocker):

    # Checks if we are getting redirected to login if using logout
    logout = app.test_client().get('dashboard/logout/',
                                   follow_redirects=True).status_code

    assert logout == 200

    # Flow if user is logged in and then log out

    with app.test_client() as c:
        with c.session_transaction() as sess:

            sess['username'] = 'name'
            sess['role_exist'] = 'exist'
            sess['project_visible'] = 'project_visible'
            sess['server'] = 'server'

        logout_v2 = c.get(
            'dashboard/logout/', follow_redirects=True).status_code

    assert logout_v2 == 200


def test_home_redirect():
    response_post = app.test_client().get('/',
                                          follow_redirects=True).status_code
    # Checks if we are getting correct response that is 200
    # after redirecting
    response_post == 200


def test_dashboard(mocker):

    mocker.patch(
        'xnat_dashboards.data_cleaning.'
        'graph_generator.GraphGenerator.__init__',
        return_value=None)

    # If data returned is empty for overview
    mocker.patch(
        'xnat_dashboards.data_cleaning.graph_generator.'
        'GraphGenerator.get_overview',
        return_value=[[], []])

    mocker.patch(
        'xnat_dashboards.data_cleaning.graph_generator.'
        'GraphGenerator.get_project_list',
        return_value=[[], []])

    mocker.patch(
        'xnat_dashboards.data_cleaning.graph_generator.'
        'GraphGeneratorPP.__init__',
        return_value=None)

    # If data returned is empty for per project view
    mocker.patch(
        'xnat_dashboards.data_cleaning.graph_generator.'
        'GraphGeneratorPP.get_project_view',
        return_value=[[], [], [], []])

    mocker.patch(
        'xnat_dashboards.data_cleaning.graph_generator.'
        'GraphGenerator.get_longitudinal_graphs',
        return_value=[])

    with app.test_client() as c:
        with c.session_transaction() as sess:
            sess['server'] = 'https://central.xnat.org'
            sess['role_exist'] = 'guest'
            sess['username'] = 'testUser'
            sess['project_visible'] = '*'

        # Get request for per project dashboard
        response_get_pp = c.\
            get('dashboard/project/CENTRAL_OASIS_CS').status_code
        assert response_get_pp == 200

        # Get request for overview dashboard having session details
        response_get_stats = c.\
            get('dashboard/stats/').status_code
        assert response_get_stats == 200

    # Get request for overview dashboard with no session details
    response_get = app.test_client().get('dashboard/stats/').status_code
    assert response_get == 302

    # If None is returned from graph generator per project view
    mocker.patch(
        'xnat_dashboards.data_cleaning.graph_generator.'
        'GraphGeneratorPP.get_project_view',
        return_value=None)

    with app.test_client() as c:
        with c.session_transaction() as sess:
            sess['server'] = 'https://central.xnat.org'
            sess['role_exist'] = 'guest'
            sess['username'] = 'testUser'
            sess['project_visible'] = '*'

        # Get request for per project dashboard
        response_get_pp = c.\
            get('dashboard/project/CENTRAL_OASIS_CS').status_code
        assert response_get_pp == 200
