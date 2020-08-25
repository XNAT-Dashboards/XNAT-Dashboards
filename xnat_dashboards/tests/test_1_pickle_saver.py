from xnat_dashboards.pyxnat_interface import pickle_saver
from xnat_dashboards import config
import pickle

config.PICKLE_PATH = 'xnat_dashboards/config/general.pickle'
config.DASHBOARD_CONFIG_PATH = 'xnat_dashboards/config/dashboard_config.json'


def test_save_and_user(mocker):

    resource_return_value = {
        'date': '28', 'resources': [], 'resources_bbrc': []}
    return_value = {
        'info': 'data',
        'projects': [], 'subjects': [],
        'experiments': [], 'scans': []}

    mocker.patch(
        'xnat_dashboards.pyxnat_interface.data_fetcher.Fetcher.get_resources',
        return_value=resource_return_value)

    mocker.patch(
        'xnat_dashboards.bbrc.data_fetcher.Fetcher'
        '.get_resource',
        return_value=resource_return_value)

    mocker.patch(
        'xnat_dashboards.pyxnat_interface.data_fetcher.Fetcher'
        '.get_instance_details',
        return_value=return_value)

    pickle_saver.PickleSaver('xnat_dashboards/config/central.cfg').save()

    with open(path_creator.get_pickle_path(), 'rb') as handle:
        data = pickle.load(handle)

    assert type(data) == dict
    assert type(data['info']) == dict
    assert type(data['resources']) == dict
    assert type(data['extra_resources']) == dict
