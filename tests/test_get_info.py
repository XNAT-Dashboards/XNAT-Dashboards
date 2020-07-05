from pyxnat_api import get_info

info_object = get_info.GetInfo(user='testUser',
                               password='testPassword',
                               server='https://central.xnat.org',
                               ssl=False)


def test_info():

    info = info_object.get_info()

    assert type(info) == dict   # Return type should be a dict
    assert len(info) == 19      # Currently 19 dicts to be returned
