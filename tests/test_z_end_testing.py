import sys
import os
from os.path import dirname, abspath
sys.path.insert(0, dirname(dirname(abspath(__file__))))


def test_end_testing():

    os.remove('pickles/users_data/general.pickle')
    os.remove('pickles/resources/general.pickle')
    os.remove('pickles/resources/generalbbrc.pickle')

    assert True
