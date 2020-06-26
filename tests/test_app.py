from app import app


def test_login():
    response_get = app.test_client().get('auth/login/')
    # Checks if we are getting correct response that is 200
    assert response_get.status_code == 200


def test_dashboard():

    data_correct = dict(username='testUser',
                        password='testPassword',
                        server='https://central.xnat.org')
    # Checks if we are getting correct response that is 200
    response_post_correct = app.test_client().post(
                                    'dashboards/stats/',
                                    data=data_correct).status_code

    # Checks if we are redirecting if wrong password
    data_incorrect_1 = dict(username='testUser',
                            password='testPasswor',
                            server='https://central.xnat.org')
    response_post_incorrect_1 = app.test_client().post(
                                'dashboards/stats/', follow_redirects=True,
                                data=data_incorrect_1).status_code

    # Checks if we are redirecting if wrong url
    data_incorrect_2 = dict(username='testUser',
                            password='testPasswor',
                            server='https://central.xnat.org')
    response_post_incorrect_2 = app.test_client().post(
                                'dashboards/stats/', follow_redirects=True,
                                data=data_incorrect_2).status_code

    # Checks if we are getting redirected to login through logout
    logout = app.test_client().get('dashboards/logout/',
                                   follow_redirects=True).status_code

    assert response_post_correct == 200
    assert response_post_incorrect_1 == 200
    assert response_post_incorrect_2 == 200
    assert logout == 200


def test_home_redirect():
    response_post = app.test_client().get('/',
                                          follow_redirects=True).status_code
    # Checks if we are getting correct response that is 200
    # after redirecting
    response_post == 200
