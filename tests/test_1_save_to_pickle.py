from save_endpoint import save_to_pickle
import pickle


def test_save_data_and_user(mocker):

    username = 'testUser'
    password = 'testPassword'
    server = 'https://central.xnat.org'
    ssl = False

    saving_object = save_to_pickle.SaveToPk(
        username, password, server, ssl)

    resource_return_value = {'date': '28', 'resources': 'test'}
    data_return_value = {'info': 'data'}

    mocker.patch(
        'pyxnat_interface.data_fetcher.FetcherLong.get_resources',
        return_value=resource_return_value)

    mocker.patch(
        'pyxnat_interface.data_fetcher.FetcherLong.get_experiment_resources',
        return_value=resource_return_value)

    mocker.patch(
        'pyxnat_interface.data_fetcher.Fetcher.fetch_all',
        return_value=data_return_value)

    saving_object = save_to_pickle.SaveToPk(
        username, password, server, ssl)

    saving_object.save_resources()

    with open('pickles/resources/general.pickle', 'rb') as handle:
        res = pickle.load(handle)

    assert type(res) == dict

    saving_object.save_data()

    with open('pickles/users_data/general.pickle', 'rb') as handle:
        user_data = pickle.load(handle)

    assert type(user_data) == dict
