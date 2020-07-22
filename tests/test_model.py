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

    exists = model.user_role_exist('testUser')
    assert exists == 'guest'
    exists = model.user_role_exist('testUer')
    assert exists is False


def test_model():

    res_bbrc = model.load_resources_bbrc_pk('guest')
    assert type(res_bbrc) == dict

    res = model.load_resources_pk('guest')
    assert type(res) == dict

    user_data = model.load_users_data_pk('guest')
    assert type(user_data)

    res_bbrc = model.load_resources_bbrc_pk('superusr')
    assert res_bbrc is None

    res = model.load_resources_pk('super')
    assert res is None

    user_data = model.load_users_data_pk('superyser')
    assert user_data is None
