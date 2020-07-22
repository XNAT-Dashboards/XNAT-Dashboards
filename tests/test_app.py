from app import app


def test_login():
    response_get = app.test_client().get('auth/login/')
    # Checks if we are getting correct response that is 200
    assert response_get.status_code == 200


def test_login_db():

    respone_get = app.test_client().get('auth/db/login/')
    assert respone_get.status_code == 200


def test_dashboard():

    data_correct = dict(username='testUser',
                        password='testPassword',
                        server='https://central.xnat.org',
                        ssl=False)
    # Checks if we are getting correct response that is 200
    response_post_correct = app.test_client().post(
        'dashboards/stats/',
        data=data_correct).status_code

    reponse_get_pp = app.test_client().\
        get('dashboards/project/CENTRAL_OASIS_CS').status_code

    response_get = app.test_client().get('dashboards/stats/').status_code

    # Checks if we are redirecting if wrong password
    data_incorrect_1 = dict(username='testUser',
                            password='testPasswor',
                            server='https://central.xnat.org',
                            ssl=False)
    response_post_incorrect_1 = app.test_client().post(
        'dashboards/stats/', follow_redirects=True,
        data=data_incorrect_1).status_code

    # Checks if we are redirecting if wrong url
    data_incorrect_2 = dict(username='testUser',
                            password='testPasswor',
                            server='https://central.xnat.org',
                            ssl=False)
    response_post_incorrect_2 = app.test_client().post(
        'dashboards/stats/', follow_redirects=True,
        data=data_incorrect_2).status_code

    # Checks if we are getting redirected to login through logout
    logout = app.test_client().get('dashboards/logout/',
                                   follow_redirects=True).status_code

    assert reponse_get_pp == 200
    assert response_post_correct == 200
    assert response_get == 200
    assert response_post_incorrect_1 == 200
    assert response_post_incorrect_2 == 200
    assert logout == 200


def test_home_redirect():
    response_post = app.test_client().get('/',
                                          follow_redirects=True).status_code
    # Checks if we are getting correct response that is 200
    # after redirecting
    response_post == 200


def test_dashboard_db(mocker):

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
