from xnat_dashboards.pyxnat_interface import data_fetcher
import os.path as op

_modulepath = op.dirname(op.abspath(__file__))
fp = op.join(op.dirname(op.dirname(__file__)), 'config/central.cfg')

def test_get_instance_details():

    # CENTRAL
    details = data_fetcher.Fetcher(fp).get_instance_details()

    # type
    assert isinstance(details['projects'], list)
    assert isinstance(details['subjects'], list)
    assert isinstance(details['experiments'], list)
    assert isinstance(details['scans'], list)

    # length
    assert len(details['projects']) != 0
    assert len(details['subjects']) != 0
    assert len(details['experiments']) != 0
    assert len(details['scans']) != 0


def test_get_resources():

    # CENTRAL
    details = data_fetcher.Fetcher(fp).get_instance_details()
    resources, bbrc_resources = data_fetcher.Fetcher(fp)\
        .get_resources(details['experiments'])
    print(bbrc_resources)
    # type
    assert isinstance(resources, list)
    assert isinstance(bbrc_resources, list)

    # length
    assert len(resources) != 0
    assert len(bbrc_resources) != 0

