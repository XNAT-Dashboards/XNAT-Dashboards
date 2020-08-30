from xnat_dashboards.app.dashboards import model as model_dash
from xnat_dashboards.app.authentication import model as model_auth
from xnat_dashboards import config


config.DASHBOARD_CONFIG_PATH = 'xnat_dashboards/config/dashboard_config.json'


# Auth model function
def test_user_exists(mocker):

    # User doesn't exist

    not_exist = model_auth.user_exists(
        'x', 'y', 'https://central.xnat.org', 'p')

    assert isinstance(not_exist, list)

    exist = model_auth.user_exists(
        'testUser', 'testPassword', 'https://central.xnat.org', 1)

    assert isinstance(exist, int)


def test_login_urls(mocker):

    # Normal url flow
    url = model_auth.login_urls()
    assert len(url) == 1


def test_user_role_exists(mocker):

    # User exist role exist
    exists = model_auth.user_role_config('testUser')
    assert type(exists) == dict

    # User role exist but login as guest
    exists = model_auth.user_role_config('testUer')
    assert type(exists) is dict

    # User role forbidden
    exists = model_auth.user_role_config('noUser')
    assert exists is False


def test_model():

    user_data = model_dash.load_users_data('https://central.xnat.org')
    assert type(user_data)

    user_data = model_dash.load_users_data('ttps://central.org')
    assert user_data is None


def test_load_user_data():

    # Normal flow
    url = 'https://central.xnat.org'
    config.PICKLE_PATH = 'xnat_dashboards/config/general.pickle'
    data = model_dash.load_users_data(url)

    assert isinstance(data, dict)

    # server url and pickle server url mismatch
    url_2 = 'https://wron url'
    data = model_dash.load_users_data(url_2)

    assert data is None

    # Pickle file not found
    config.PICKLE_PATH = 'xnat_dashboards/config/cetral.pic'
    data = model_dash.load_users_data(url)

    assert data is None
