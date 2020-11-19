from xnat_dashboards import data_fetcher as df
import pyxnat
import os.path as op

_moduledir = op.dirname(op.dirname(__file__))
fp = op.join(_moduledir, 'config', 'central.cfg')
x = pyxnat.Interface(config=fp)


def test_data_fetcher():

    details = df.get_instance_details(x)

    assert len(details['projects']) != 0
    assert len(details['subjects']) != 0
    assert len(details['experiments']) != 0
    assert len(details['scans']) != 0

    resources, bbrc_resources = df.get_resources(x)
    print(bbrc_resources)

    assert len(resources) != 0
    assert len(bbrc_resources) != 0

    df.longitudinal_data(details, resources)
