from xnat_dashboards.save_endpoint import save_to_pickle
from xnat_dashboards import path_creator
import pickle


def test_save_data_and_user(mocker):

    path = 'central.cfg'

    resource_return_value = {
        'date': '28', 'resources': [], 'resources_bbrc': []}
    data_return_value = {
        'info': 'data',
        'projects': [], 'subjects': [],
        'experiments': [], 'scans': []}

    mocker.patch(
        'xnat_dashboards.pyxnat_interface.data_fetcher.Fetcher.get_resources',
        return_value=resource_return_value)

    mocker.patch(
        'xnat_dashboards.pyxnat_interface.data_fetcher.Fetcher'
        '.get_experiment_resources',
        return_value=resource_return_value)

    mocker.patch(
        'xnat_dashboards.pyxnat_interface.data_fetcher.Fetcher.fetch_all',
        return_value=data_return_value)

    save_to_pickle.SaveToPk(path).save_to_PK()

    with open(path_creator.get_pickle_path(), 'rb') as handle:
        data = pickle.load(handle)

    assert type(data) == dict
    assert type(data['info']) == dict
    assert type(data['resources']) == dict
    assert type(data['resources_bbrc']) == dict
