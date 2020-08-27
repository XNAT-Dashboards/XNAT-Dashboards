from xnat_dashboards.pyxnat_interface import data_fetcher
import pyxnat

fetch_object_connected = data_fetcher.Fetcher(
    'xnat_dashboards/config/central.cfg')


def test_instance_details():

    details = fetch_object_connected.get_instance_details()

    assert isinstance(details['projects'], list)

    assert isinstance(details['subjects'], list)

    assert isinstance(details['experiments'], list)

    assert isinstance(details['scans'], list)

    obj = pyxnat.Interface(
        user="testUser",
        password="testPassrd",
        server="https://central.xnat.org",
        verify=True)
    obj.save_config('xnat_dashboards/config/t.cfg')

    fetch_object_conn_pwd_incorrect = data_fetcher.Fetcher(
        'xnat_dashboards/config/t.cfg')
    assert fetch_object_conn_pwd_incorrect.get_instance_details() == 401

    obj = pyxnat.Interface(
        user="testUser",
        password="testPassrd",
        server="https://central.xnat.org/",
        verify=True)
    obj.save_config('xnat_dashboards/config/t.cfg')
    fetch_object_conn_uri_incorrect = data_fetcher.Fetcher(
        'xnat_dashboards/config/t.cfg')

    obj = pyxnat.Interface(
        user="testUser",
        password="testPassrd",
        server="https://central.xna",
        verify=True)
    obj.save_config('xnat_dashboards/config/t.cfg')
    assert fetch_object_conn_uri_incorrect.get_instance_details() == 500

    fetch_object_conn_url_incorrect = data_fetcher.Fetcher(
        'xnat_dashboards/config/t.cfg')
    assert fetch_object_conn_url_incorrect.get_instance_details() == 1
