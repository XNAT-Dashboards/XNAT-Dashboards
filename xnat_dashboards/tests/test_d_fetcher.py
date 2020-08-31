from xnat_dashboards.pyxnat_interface import data_fetcher
import pyxnat

fetch_object_connected = data_fetcher.Fetcher(
    'xnat_dashboards/config/central.cfg')


def test_instance_details():

    # Normal flow
    details = fetch_object_connected.get_instance_details()

    assert isinstance(details['projects'], list)
    assert isinstance(details['subjects'], list)
    assert isinstance(details['experiments'], list)
    assert isinstance(details['scans'], list)

    # Wrong password
    obj = pyxnat.Interface(
        user="testUser",
        password="testPassrd",
        server="https://central.xnat.org",
        verify=True)
    obj.save_config('xnat_dashboards/config/wrong_pass.cfg')

    fetch_object_conn_pwd_incorrect = data_fetcher.Fetcher(
        'xnat_dashboards/config/wrong_pass.cfg')
    assert fetch_object_conn_pwd_incorrect.get_instance_details() == 401

    # Wrong URI
    obj = pyxnat.Interface(
        user="testUser",
        password="testPassword",
        server="https://central.xnat.org/",
        verify=True)
    obj.save_config('xnat_dashboards/config/wrong_uri.cfg')
    fetch_object_conn_uri_incorrect = data_fetcher.Fetcher(
        'xnat_dashboards/config/wrong_uri.cfg')

    assert fetch_object_conn_uri_incorrect.get_instance_details() == 500

    # Wrong URL
    obj = pyxnat.Interface(
        user="testUser",
        password="testPassword",
        server="https://central.xna",
        verify=True)
    obj.save_config('xnat_dashboards/config/wrong_url.cfg')
    fetch_object_conn_url_incorrect = data_fetcher.Fetcher(
        'xnat_dashboards/config/wrong_url.cfg')
    assert fetch_object_conn_url_incorrect.get_instance_details() == 1


def test_get_resources(mocker):

    # Normal resource flow
    res = fetch_object_connected.get_resources(
        [{
            'ID': 'OAS1_0007_MR1_APARC_LH',
            'project': 'CENTRAL_OASIS_CS'}])
    assert len(res) == 1  # No resource found

    # Wrong data
    res = fetch_object_connected.get_resources(
        [{
            'ID': 'OS2_0002_MR',
            'project': 'CENTRAL_OASIS_LON'}])

    assert len(res) == 1  # No resource found
