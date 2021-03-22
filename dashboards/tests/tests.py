from dashboards.data import filter as df
from dashboards.data import bbrc as dfb
from dashboards.data import graph as g
from dashboards.app import app
from dashboards import config
import os.path as op
import dashboards
import pyxnat
from dashboards import pickle as pk
import pickle

import tempfile
fh, fp = tempfile.mkstemp(suffix='.pickle')
print('Creating %s...' % fp)
config.PICKLE_PATH = fp

fp = op.join(op.dirname(dashboards.__file__), '..', 'config.json')
config.DASHBOARD_CONFIG_PATH = fp
fp = op.join(op.dirname(dashboards.__file__), '..', '.xnat.cfg')
x = pyxnat.Interface(config=fp)


def test_001_pickle_save():  # should be run first

    pk.save(x, config.PICKLE_PATH)
    with open(config.PICKLE_PATH, 'rb') as handle:
        data = pickle.load(handle)

    assert isinstance(data, dict)
    assert data['server'] == "https://devxnat.barcelonabeta.org"
    assert data['verify'] == 1
    assert isinstance(data, dict)
    assert isinstance(data['resources'], list)
    assert isinstance(data['longitudinal_data'], dict)


def test_019_reorder_graphs():
    p = pickle.load(open(config.PICKLE_PATH, 'rb'))
    df.filter_data(p, [])
    graphs = df.get_graphs(p)

    assert isinstance(graphs, dict)
    assert len(graphs) != 0


def test_020_reorder_graphs_PP():
    p = pickle.load(open(config.PICKLE_PATH, 'rb'))

    project = p['projects'][0]
    project_id = project['id']
    df.filter_data(p, project_id)
    graphs = df.get_graphs_per_project(p)
    assert isinstance(graphs, dict)
    assert len(graphs) != 0


# def test_022_reorder_graphs_bbrc():
#     p = pickle.load(open(config.PICKLE_PATH, 'rb'))
#
#     df.filter_data(p, '*')
#     assert isinstance(filtered, dict)
#     assert len(filtered) != 0


# def test_023_reorder_graphs_bbrc_PP():
#     p = pickle.load(open(config.PICKLE_PATH, 'rb'))
#     # bbrc_resources = p['extra_resources']
#
#     project = p['projects'][0]
#     project_id = project['id']
#     filtered = dfb.filter_data(p['resources'], project_id)
#
#     assert isinstance(filtered, dict)
#     assert len(filtered) != 0


def test_024_get_overview():
    p = pickle.load(open(config.PICKLE_PATH, 'rb'))

    role = 'admin'
    df.filter_data(p, p['projects'])
    data = df.get_graphs(p)
    stats = df.get_stats(p)

    overview = g.add_graph_fields(data, role)
    graph_list = g.split_by_2(overview)

    assert isinstance(graph_list, list)
    assert len(graph_list) != 0


def test_025_get_project_view():
    p = pickle.load(open(config.PICKLE_PATH, 'rb'))

    project = p['projects'][0]
    project_id = project['id']
    role = 'admin'
    df.filter_data(p, project_id)
    data_pp = df.get_graphs_per_project(p)
    resources = [e for e in p['resources'] if len(e) > 4]
    dfpp = dfb.filter_data_per_project(resources, project_id)
    data_pp.update(dfpp)
    stats = df.get_stats(p)
    project_details = df.get_projects_details_pp(p, project_id)
    data_pp.pop('test_grid')
    project_view = g.add_graph_fields(data_pp, role)
    graph_list = g.split_by_2(project_view)

    assert isinstance(graph_list, list)
    assert len(graph_list) != 0


def test_026_login():
    # Login route test
    respone_get = app.test_client().get('auth/login/')
    assert respone_get.status_code == 200


def test_027_logout():

    # Checks if we are getting redirected to login if using logout
    logout = app.test_client().get('dashboard/logout/',
                                   follow_redirects=True).status_code
    assert logout == 200


def test_028_stats():

    with app.test_client() as c:
        with c.session_transaction() as sess:
            sess['server'] = 'https://devxnat.barcelonabeta.org'
            sess['role'] = 'guest'
            sess['username'] = 'testUser'
            sess['projects'] = []
            sess['graphs'] = []

    response_get_stats = c.get('dashboard/overview/').status_code
    assert response_get_stats == 200
