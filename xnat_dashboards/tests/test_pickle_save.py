from xnat_dashboards import pickle as pk
import pyxnat
import pickle
import os.path as op
import xnat_dashboards

pickle_path = 'xnat_dashboards/config/test.pickle'
fp = op.join(op.dirname(xnat_dashboards.__file__), '..', '.xnat.cfg')
x = pyxnat.Interface(config=fp)

def test_pickle_save():

    pk.save(x, pickle_path)
    with open(pickle_path, 'rb') as handle:
        data = pickle.load(handle)

    assert isinstance(data, dict)
    assert data['server'] == "https://devxnat.barcelonabeta.org"
    assert data['verify'] == 1
    assert isinstance(data['info'], dict)
    assert isinstance(data['resources'], list)
    assert isinstance(data['extra_resources'], list)