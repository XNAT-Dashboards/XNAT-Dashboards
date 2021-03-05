from dashboards.data_cleaning import data_filter as dfi
from dashboards.bbrc import data_filter as dfib
from dashboards.data_cleaning import graph_generator as gg
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


# def test_002_get_projects_details():
#     p = pickle.load(open(config.PICKLE_PATH, 'rb'))
#
#     projects = p['projects']
#     project_details = dfo.Formatter().get_projects_details(projects)
#
#     assert isinstance(project_details['Number of Projects'], int)
#     assert isinstance(project_details['Projects'], dict)
#
#     assert project_details['Number of Projects'] != 0
#     assert len(project_details['Projects']) != 0


# def test_003_get_projects_details_PP():
#     p = pickle.load(open(config.PICKLE_PATH, 'rb'))
#
#     projects = p['projects']
#     project = p['projects'][0]
#     project_id = project['id']
#     project_details = dfo.FormatterPP(project_id).get_projects_details(projects)
#
#     assert isinstance(project_details['Owner(s)'], list)
#     assert isinstance(project_details['Collaborator(s)'], list)
#     assert isinstance(project_details['member(s)'], list)
#     assert isinstance(project_details['user(s)'], list)
#     assert isinstance(project_details['last_accessed(s)'], list)
#     assert isinstance(project_details['insert_user(s)'], str)
#     assert isinstance(project_details['insert_date'], str)
#     assert isinstance(project_details['access'], str)
#     assert isinstance(project_details['name'], str)
#     assert isinstance(project_details['last_workflow'], str)


# def test_004_get_projects_details_specific():
#     p = pickle.load(open(config.PICKLE_PATH, 'rb'))
#
#     projects = p['projects']
#     project_details_specific = dfo.Formatter().get_projects_details_specific(projects)
#
#     assert isinstance(project_details_specific, dict)
#     assert len(project_details_specific) != 0


# def test_005_get_subjects_details():
#     p = pickle.load(open(config.PICKLE_PATH, 'rb'))
#
#     subjects = p['subjects']
#     subject_details = dfo.Formatter().get_subjects_details(subjects)
#
#     assert isinstance(subject_details['Number of Subjects'], int)
#     assert isinstance(subject_details['Subjects'], dict)
#
#     assert subject_details['Number of Subjects'] != 0
#     assert len(subject_details['Subjects']) != 0


# def test_006_get_subjects_details_PP():
#     p = pickle.load(open(config.PICKLE_PATH, 'rb'))
#
#     subjects = p['subjects']
#     project = p['projects'][0]
#     project_id = project['id']
#     subject_details = dfo.FormatterPP(project_id).get_subjects_details(subjects)
#
#     assert isinstance(subject_details['Number of Subjects'], int)
#     assert subject_details['Number of Subjects'] != 0


# def test_007_get_experiments_details():
#     p = pickle.load(open(config.PICKLE_PATH, 'rb'))
#
#     experiments = p['experiments']
#     experiments_details = dfo.Formatter().get_experiments_details(experiments)
#
#     assert isinstance(experiments_details['Number of Experiments'], int)
#     assert isinstance(experiments_details['Total amount of sessions'], dict)
#
#     assert experiments_details['Number of Experiments'] != 0
#     assert len(experiments_details['Total amount of sessions']) != 0


# def test_008_get_experiments_details_PP():
#     p = pickle.load(open(config.PICKLE_PATH, 'rb'))
#
#     experiments = p['experiments']
#     project = p['projects'][0]
#     project_id = project['id']
#     experiments_details = dfo.FormatterPP(project_id).get_experiments_details(experiments)
#
#     assert isinstance(experiments_details['Number of Experiments'], int)
#     assert isinstance(experiments_details['Total amount of sessions'], dict)
#
#     assert experiments_details['Number of Experiments'] != 0
#     assert len(experiments_details['Total amount of sessions']) != 0


# def test_009_get_scans_details():
#     p = pickle.load(open(config.PICKLE_PATH, 'rb'))
#     # bbrc_resources = p['extra_resources']
#     resources, bbrc_resources = [], []
#     for e in p['resources']:
#         if len(e) == 4:
#             resources.append(e)
#         elif len(e) > 4:
#             bbrc_resources.append(e)
#
#     scans = p['scans']
#     scans_details = dfo.Formatter().get_scans_details(scans)
#
#     assert isinstance(scans_details['Number of Scans'], int)
#     assert isinstance(scans_details['Scan quality'], dict)
#     assert isinstance(scans_details['Scan Types'], dict)
#
#     assert scans_details['Number of Scans'] != 0
#     assert len(scans_details['Scan quality']) != 0
#     assert len(scans_details['Scan Types']) != 0


# def test_010_get_scans_details_PP():
#     p = pickle.load(open(config.PICKLE_PATH, 'rb'))
#
#     scans = p['scans']
#     project = p['projects'][0]
#     project_id = project['id']
#     scans_details = dfo.FormatterPP(project_id).get_scans_details(scans)
#
#     assert isinstance(scans_details['Number of Scans'], int)
#     assert isinstance(scans_details['Scan quality'], dict)
#     assert isinstance(scans_details['Scan Types'], dict)
#
#     assert scans_details['Number of Scans'] != 0
#     assert len(scans_details['Scan quality']) != 0
#     assert len(scans_details['Scan Types']) != 0

#
# def test_011_get_resources_details():
#     p = pickle.load(open(config.PICKLE_PATH, 'rb'))
#     # bbrc_resources = p['extra_resources']
#     resources, bbrc_resources = [], []
#     for e in p['resources']:
#         if len(e) == 4:
#             resources.append(e)
#         elif len(e) > 4:
#             bbrc_resources.append(e)
#
#     resource_details = dfo.Formatter().get_resources_details(resources)
#
#     assert isinstance(resource_details, dict)
#     assert len(resource_details) != 0


# def test_012_get_resources_details_PP():
#
#     p = pickle.load(open(config.PICKLE_PATH, 'rb'))
#     # bbrc_resources = p['extra_resources']
#     resources, bbrc_resources = [], []
#     for e in p['resources']:
#         if len(e) == 4:
#             resources.append(e)
#         elif len(e) > 4:
#             bbrc_resources.append(e)
#
#     project = p['projects'][0]
#     project_id = project['id']
#     resource_details = dfo.FormatterPP(project_id).get_resources_details(resources)
#
#     assert isinstance(resource_details, dict)
#     assert len(resource_details) != 0


def test_013_get_get_longitudinal_data():
    p = pickle.load(open(config.PICKLE_PATH, 'rb'))

    long_data = p['longitudinal_data']

    assert isinstance(long_data, dict)
    assert len(long_data) != 0


# def test_014_get_bbrc_resource_details():
#     p = pickle.load(open(config.PICKLE_PATH, 'rb'))
#     # bbrc_resources = p['extra_resources']
#     resources, bbrc_resources = [], []
#     for e in p['resources']:
#         if len(e) == 4:
#             resources.append(e)
#         elif len(e) > 4:
#             bbrc_resources.append(e)
#
#     resource_bbrc_details = dfo_bbrc.Formatter().get_resource_details(bbrc_resources)
#
#     assert isinstance(resource_bbrc_details, dict)
#     assert len(resource_bbrc_details) != 0


# def test_015_diff_dates():
#     p = pickle.load(open(config.PICKLE_PATH, 'rb'))
#     # bbrc_resources = p['extra_resources']
#     resources, bbrc_resources = [], []
#     for e in p['resources']:
#         if len(e) == 4:
#             resources.append(e)
#         elif len(e) > 4:
#             bbrc_resources.append(e)
#     #experiments = p['experiments']
#     project = p['projects'][0]
#     project_id = project['id']
#     dict_diff_dates = dfo_bbrc.Formatter().diff_dates(bbrc_resources, project_id)
#
#     assert isinstance(dict_diff_dates, dict)
#     assert len(dict_diff_dates) != 0


# def test_016_generate_test_grid_bbrc():
#
#     p = pickle.load(open(config.PICKLE_PATH, 'rb'))
#     # bbrc_resources = p['extra_resources']
#     resources, bbrc_resources = [], []
#     for e in p['resources']:
#         if len(e) == 4:
#             resources.append(e)
#         elif len(e) > 4:
#             bbrc_resources.append(e)
#
#     project = p['projects'][0]
#     project_id = project['id']
#     test_grid = dfo_bbrc.Formatter().generate_test_grid_bbrc(bbrc_resources, project_id)
#
#     assert isinstance(test_grid, list)
#     assert len(test_grid) != 0


# def test_017_get_project_list():
#     p = pickle.load(open(config.PICKLE_PATH, 'rb'))
#     # bbrc_resources = p['extra_resources']
#     resources, bbrc_resources = [], []
#     for e in p['resources']:
#         if len(e) == 4:
#             resources.append(e)
#         elif len(e) > 4:
#             bbrc_resources.append(e)
#
#     filtered = dfi.DataFilter('testUser', p, 'admin', [])
#     projects = filtered.get_projects_details_specific(filtered.data['projects'])
#
#     assert isinstance(projects, dict)
#     assert isinstance(projects['project_list'], list)


def test_019_reorder_graphs():
    p = pickle.load(open(config.PICKLE_PATH, 'rb'))
    # bbrc_resources = p['extra_resources']
    resources = [e for e in p['resources'] if len(e) == 4]
    bbrc_resources = [e for e in p['resources'] if len(e) > 4]

    filtered = dfi.DataFilter(p, [])
    ordered_graphs = filtered.reorder_graphs()

    assert isinstance(ordered_graphs, dict)
    assert len(ordered_graphs) != 0


def test_020_reorder_graphs_PP():
    p = pickle.load(open(config.PICKLE_PATH, 'rb'))

    project = p['projects'][0]
    project_id = project['id']
    filtered = dfi.DataFilterPP()
    ordered_graphs = filtered.reorder_graphs_pp(p, project_id)
    assert isinstance(ordered_graphs, dict)
    assert len(ordered_graphs) != 0


def test_022_reorder_graphs_bbrc():
    p = pickle.load(open(config.PICKLE_PATH, 'rb'))

    filtered = dfib.BBRCDataFilter(p['resources'], [])
    ordered_graphs = filtered.reorder_graphs()

    assert isinstance(ordered_graphs, dict)
    assert len(ordered_graphs) != 0


def test_023_reorder_graphs_bbrc_PP():
    p = pickle.load(open(config.PICKLE_PATH, 'rb'))
    # bbrc_resources = p['extra_resources']

    experiments = p['experiments']
    project = p['projects'][0]
    project_id = project['id']
    role = 'admin'
    filtered = dfib.DataFilterPP(p['resources'], experiments, project_id,
                                 {role: [project_id]})
    ordered_graphs = filtered.reorder_graphs_pp()
    assert isinstance(ordered_graphs, dict)
    assert len(ordered_graphs) != 0


def test_024_get_overview():
    p = pickle.load(open(config.PICKLE_PATH, 'rb'))

    role = 'admin'
    filtered = dfi.DataFilter(p, p['projects'])
    graph_object = gg.GraphGenerator(filtered, p)

    graph_list = graph_object.get_overview(role)

    assert isinstance(graph_list, list)
    assert len(graph_list) != 0


def test_025_get_project_view():
    p = pickle.load(open(config.PICKLE_PATH, 'rb'))

    project = p['projects'][0]
    project_id = project['id']
    role = 'admin'
    g = gg.GraphGeneratorPP(project_id, role, p, {role: [project_id]})

    graph_list = g.get_project_view()

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

    response_get_stats = c.get('dashboard/overview/').status_code
    assert response_get_stats == 200
