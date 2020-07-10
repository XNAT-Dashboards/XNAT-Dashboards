from pyxnat_api import get_info_pp

info_object = get_info_pp.GetInfo(
    user='testUser',
    password='testPassword',
    server='https://central.xnat.org',
    ssl=False,
    project_id='CENTRAL_OASIS_CS')


def test_info():

    info = info_object.get_pp_view('CENTRAL_OASIS_CS')

    assert type(info) == dict   # Return type should be a dict
    assert len(info) == 12     # Currently 12 dicts to be returned
