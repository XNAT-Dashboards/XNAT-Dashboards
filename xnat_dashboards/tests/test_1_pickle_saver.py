from xnat_dashboards.pyxnat_interface import pickle_saver
from xnat_dashboards import config
import pyxnat
import pickle

config.PICKLE_PATH = 'xnat_dashboards/config/general.pickle'
config.DASHBOARD_CONFIG_PATH = 'xnat_dashboards/config/dashboard_config.json'


def test_save(mocker):

    # Check code for normal flow
    return_value = {
        'server': 'https://central.xnat.org',
        'info': 'data',
        'projects': [], 'subjects': [],
        'experiments': [], 'scans': []}

    mocker.patch(
        'xnat_dashboards.pyxnat_interface.data_fetcher.Fetcher.get_resources',
        return_value=[])

    mocker.patch(
        'xnat_dashboards.bbrc.data_fetcher.Fetcher'
        '.get_resource',
        return_value=[])

    mocker.patch(
        'xnat_dashboards.pyxnat_interface.data_fetcher.Fetcher'
        '.get_instance_details',
        return_value=return_value)

    pickle_saver.PickleSaver('xnat_dashboards/config/central.cfg').save()

    with open(config.PICKLE_PATH, 'rb') as handle:
        data = pickle.load(handle)

    assert isinstance(data, dict)
    assert isinstance(data['info'], dict)
    assert isinstance(data['resources'], list)
    assert data['extra_resources'] is None

    # Code flow if server url mismatches from the already created file
    # Create a cfg file with different url
    obj = pyxnat.Interface(
        user="testUser",
        password="testPassrd",
        server="https://central.xna",
        verify=True)
    obj.save_config('xnat_dashboards/config/wrong_url.cfg')

    assert pickle_saver.PickleSaver(
        'xnat_dashboards/config/wrong_url.cfg').save() == 1


# Code if BBRC resources are present
def test_save_bbrc(mocker):

    resources = [
        ['p1', 's2', True, 'BBRC_VALIDATOR', 'Test', True, 'Date'],
        ['p1', 's2', True, 'BBRC_VALIDATOR', 'Test', False, None],
        ['p1', 's2', True, 'BBRC_VALIDATOR', 'Test', True, 'Date'],
        ['p1', 's2', False, 0, 'Test', False, None],
        ['p1', 's2', True, 'BBRC_VALIDATOR', 'Test', False, None]]

    data = {
        'server': 'https://central.xnat.org',
        'info': 'data',
        'projects': [{'id': 'p1'}, {'id': 'p2'}],
        'subjects': [{'ID': 's1'}, {'ID': 's2'}],
        'experiments': [], 'scans': []}

    mocker.patch(
        'xnat_dashboards.pyxnat_interface.data_fetcher.Fetcher.get_resources',
        return_value=resources)

    mocker.patch(
        'xnat_dashboards.bbrc.data_fetcher.Fetcher'
        '.get_resource',
        return_value=resources)

    mocker.patch(
        'xnat_dashboards.pyxnat_interface.data_fetcher.Fetcher'
        '.get_instance_details',
        return_value=data)

    config.PICKLE_PATH = 'xnat_dashboards/config/test_extra_resources.pickle'
    pickle_saver.PickleSaver('xnat_dashboards/config/central.cfg').save()

    with open(config.PICKLE_PATH, 'rb') as handle:
        data = pickle.load(handle)

    assert isinstance(data, dict)
    assert isinstance(data['info'], dict)
    assert isinstance(data['resources'], list)
    assert isinstance(data['extra_resources'], list)


def test_longitudinal_data(mocker):

    resources = [
        ['p1', 's2', True, 'BBRC_VALIDATOR', 'Test', True, 'Date'],
        ['p1', 's2', True, 'BBRC_VALIDATOR', 'Test', False, None],
        ['p1', 's2', True, 'BBRC_VALIDATOR', 'Test', True, 'Date'],
        ['p1', 's2', False, 0, 'Test', False, None],
        ['p1', 's2', True, 'BBRC_VALIDATOR', 'Test', False, None]]

    data = {
        'server': 'https://central.xnat.org',
        'info': 'data',
        'projects': [{'id': 'p1'}, {'id': 'p2'}],
        'subjects': [{'ID': 's1'}, {'ID': 's2'}],
        'experiments': [], 'scans': []}

    mocker.patch(
        'xnat_dashboards.pyxnat_interface.'
        'pickle_saver.PickleSaver.__init__',
        return_value=None)

    l_d = pickle_saver.PickleSaver('xnat_dashboards/config/central.cfg')\
        .longitudinal_data_processing(
            data, {}, resources)

    assert len(l_d) == 5
