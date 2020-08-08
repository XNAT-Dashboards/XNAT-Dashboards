from app import app


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
        'saved_data_processing.graph_generator_DB.GraphGenerator.__init__',
        return_value=None)

    mocker.patch(
        'saved_data_processing.graph_generator_DB.'
        'GraphGenerator.graph_generator',
        return_value=[[], []])

    mocker.patch(
        'saved_data_processing.graph_generator_DB.'
        'GraphGenerator.project_list_generator',
        return_value=[[], []])

    mocker.patch(
        'saved_data_processing.graph_generator_DB.'
        'GraphGeneratorPP.__init__',
        return_value=None)

    mocker.patch(
        'saved_data_processing.graph_generator_DB.'
        'GraphGeneratorPP.graph_generator',
        return_value=None)

    mocker.patch(
        'saved_data_processing.graph_generator_DB.'
        'GraphGenerator.graph_generator_longitudinal',
        return_value=[])

    data_post_login_dash_present = dict(username='testUser',
                                        password='testPassword',
                                        server='https://central.xnat.org',
                                        ssl=False,
                                        DB=True)

    response_post = app.test_client().post('dashboards/db/stats/',
                                           data=data_post_login_dash_present,
                                           ).status_code

    data_post_login_dash_present_pk = dict(username='testUser',
                                           password='testPassword',
                                           server='https://central.xnat.org',
                                           ssl=False,
                                           DB=True)

    response_post_pk = app.test_client().post(
        'dashboards/db/stats/',
        data=data_post_login_dash_present_pk).status_code

    assert response_post_pk == 200

    response_get_pp = app.test_client().\
        get('dashboards/db/project/CENTRAL_OASIS_CS').status_code

    assert response_get_pp == 200

    assert response_post == 200

    response_get = app.test_client().get('dashboards/db/stats/').status_code

    assert response_get == 200
