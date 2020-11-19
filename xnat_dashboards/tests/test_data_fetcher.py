from xnat_dashboards import data_fetcher as df
import pyxnat
import os.path as op

_modulepath = op.dirname(op.abspath(__file__))
fp = op.join(op.dirname(op.dirname(__file__)), 'config/central.cfg')
x = pyxnat.Interface(config=fp)


def test_get_instance_details():

    details = df.get_instance_details(x)

    assert len(details['projects']) != 0
    assert len(details['subjects']) != 0
    assert len(details['experiments']) != 0
    assert len(details['scans']) != 0


def test_get_resources():

    resources, bbrc_resources = df.get_resources(x)
    print(bbrc_resources)

    assert len(resources) != 0
    assert len(bbrc_resources) != 0
