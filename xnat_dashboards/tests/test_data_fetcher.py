from xnat_dashboards import data_fetcher as df
from xnat_dashboards import pickle
import pyxnat
import os.path as op
import xnat_dashboards

fp = op.join(op.dirname(xnat_dashboards.__file__), '..', '.xnat.cfg')
x = pyxnat.Interface(config=fp)


def test_data_fetcher():

    details = df.get_instance_details(x)

    assert len(details['projects']) != 0
    assert len(details['subjects']) != 0
    assert len(details['experiments']) != 0
    assert len(details['scans']) != 0

    resources, bbrc_resources = df.get_resources(x)

    assert len(resources) != 0
    assert len(bbrc_resources) != 0

    longitudinal_data = df.longitudinal_data(details, resources)

    pickle.save(x, fp)
    with open(x.PICKLE_PATH, 'rb') as handle:
        data = pickle.load(handle)

    assert isinstance(data, dict)
    assert data['server'] == "https://dev-xnat.barcelonabeta.org"
    assert data['verify'] == 1
    assert data['info']['data']['projects'] == details['projects']
    assert data['info']['data']['subjects'] == details['subjects']
    assert data['info']['data']['experiments'] == details['experiments']
    assert data['info']['data']['scans'] == details['scans']
    assert data['resources'] == resources
    assert data['extra_resources'] == bbrc_resources
    assert data['longitudinal'] == longitudinal_data
