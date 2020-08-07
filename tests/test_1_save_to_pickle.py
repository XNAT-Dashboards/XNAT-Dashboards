from save_endpoint import save_to_pickle
import pickle


def test_save_data_and_user(mocker):

    username = 'testUser'
    password = 'testPassword'
    server = 'https://central.xnat.org'
    ssl = False

    resource_return_value = {
        'date': '28', 'resources': [], 'resources_bbrc': []}
    data_return_value = {'info': 'data'}

    mocker.patch(
        'pyxnat_interface.data_fetcher.Fetcher.get_resources',
        return_value=resource_return_value)

    mocker.patch(
        'pyxnat_interface.data_fetcher.Fetcher.get_experiment_resources',
        return_value=resource_return_value)

    mocker.patch(
        'pyxnat_interface.data_fetcher.Fetcher.fetch_all',
        return_value=data_return_value)

    save_to_pickle.SaveToPk(
        username, password, server, ssl).save_to_PK()

    with open('pickles/data/general.pickle', 'rb') as handle:
        data = pickle.load(handle)

    assert type(data) == dict
    assert type(data['info']) == dict
    assert type(data['resources']) == dict
    assert type(data['resources_bbrc']) == dict
