from xnat_dashboards.pyxnat_interface import data_fetcher


fetch_object_connected = data_fetcher.Fetcher(
    'xnat_dashboards/config/central.cfg')

fetch_object_conn_pwd_incorrect = data_fetcher.Fetcher(
    'xnat_dashboards/config/centralWP.cfg')

fetch_object_conn_uri_incorrect = data_fetcher.Fetcher(
    'xnat_dashboards/config/centralWURI.cfg')

fetch_object_conn_url_incorrect = data_fetcher.Fetcher(
    'xnat_dashboards/config/centralWURL.cfg')


def test_instance_details():

    details = fetch_object_connected.get_instance_details()

    assert type(details['projects']) == list

    assert fetch_object_conn_pwd_incorrect.get_instance_details() == 401
    assert fetch_object_conn_uri_incorrect.get_instance_details() == 500
    assert fetch_object_conn_url_incorrect.get_instance_details() == 1

    assert type(details['subjects']) == list

    assert type(details['experiments']) == list

    assert type(details['scans']) == list
