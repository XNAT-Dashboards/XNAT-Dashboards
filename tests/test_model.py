from app.dashboards import model


def test_user_exists(mocker):

    mocker.patch(
        'pyxnat_interface.data_fetcher.Fetcher.get_projects_details',
        return_value=0)

    not_exist = model.user_exists('x', 'y', 'z', 'p')

    assert type(not_exist) == list

    mocker.patch(
        'pyxnat_interface.data_fetcher.Fetcher.get_projects_details',
        return_value=[3, 2])

    exist = model.user_exists('x', 'y', 'z', 'p')

    assert type(exist) == int


def test_user_role_exists(mocker):

    exists = model.user_role_config('testUser')
    assert type(exists) == dict
    exists = model.user_role_config('testUer')
    assert type(exists) is dict
    exists = model.user_role_config('noUser')
    assert exists is False


def test_model():

    user_data = model.load_users_data_pk('https://central.xnat.org')
    assert type(user_data)

    user_data = model.load_users_data_pk('ttps://central.org')
    assert user_data is None
