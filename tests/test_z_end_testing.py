import sys
import os
from os.path import dirname, abspath
sys.path.insert(0, dirname(dirname(abspath(__file__))))


def test_end_testing():

    os.remove('pickles/data/general.pickle')

    assert True
