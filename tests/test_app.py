from app import app


def test_login():
    response_get = app.test_client().get('auth/login/')
    # Checks if we are getting correct response that is 200
    assert response_get.status_code == 200


def test_dashboard():
    data = dict(username='testUser',
                password='testPassword',
                server='https://central.xnat.org')
    # Checks if we are getting correct response that is 200
    response_post = app.test_client().post('dashboards/stats/',
                                           data=data).status_code
    assert response_post == 200


def test_home_redirect():
    response_post = app.test_client().get('/',
                                          follow_redirects=True).status_code
    # Checks if we are getting correct response that is 200
    # after redirecting
    response_post == 200
