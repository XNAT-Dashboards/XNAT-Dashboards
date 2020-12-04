from dashboards import data_fetcher as df
import pyxnat
import os.path as op
import dashboards

fp = op.join(op.dirname(dashboards.__file__), '..', '.xnat.cfg')
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