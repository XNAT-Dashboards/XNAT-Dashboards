from dashboards.data import filter as f
from dashboards.data import bbrc
from dashboards.data import graph as g
from dashboards.app import app
from dashboards import config
import os.path as op
import dashboards
import pyxnat
from dashboards import pickle as pk
import pickle
import logging as log

import tempfile
fh, fp = tempfile.mkstemp(suffix='.pickle')
log.info('Creating %s...' % fp)
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


def test_002_pickle_project_data():

    c = pyxnat.Interface(server='https://www.nitrc.org/ir', anonymous=True)
    projects = pk.get_projects(c)

    p = projects.pop()
    keys = sorted(['insert_date', 'insert_user', 'id', 'name', 'name_csv',
                   'description', 'description_csv', 'secondary_id', 'keywords',
                   'pi', 'project_invs', 'project_access', 'project_users',
                   'project_owners', 'project_members', 'project_collabs',
                   'project_last_workflow', 'project_last_access', 'project_fav',
                   'proj_mr_count', 'proj_ct_count', 'proj_pet_count',
                   'proj_ut_count'])
    assert(sorted(p.keys()) == keys)


def test_003_pickle_subject_data():

    c = pyxnat.Interface(server='https://www.nitrc.org/ir', anonymous=True)
    subjects = pk.get_subjects(c)

    s = subjects.pop()
    keys = sorted(['gender', 'handedness', 'project', 'ID', 'URI', 'age'])
    assert(sorted(s.keys()) == keys)


def test_004_pickle_experiment_data():

    c = pyxnat.Interface(server='https://www.nitrc.org/ir', anonymous=True)
    experiments = pk.get_experiments(c)

    e = experiments.pop()
    keys = sorted(['xnat:subjectassessordata/id', 'subject_ID', 'ID',
                   'project', 'date', 'xsiType', 'URI'])
    assert(sorted(e.keys()) == keys)


def test_005_pickle_scan_data():

    c = pyxnat.Interface(server='https://www.nitrc.org/ir', anonymous=True)
    scans = pk.get_scans(c)

    s = scans.pop()
    keys = sorted(['session_ID', 'xnat:imagesessiondata/subject_id', 'ID',
                   'project', 'xsiType', 'xnat:imagescandata/id', 'URI',
                   'xnat:imagescandata/quality', 'xnat:imagescandata/type'])
    assert(sorted(s.keys()) == keys)


def test_006_pickle_resource_data():

    c = pyxnat.Interface(server='https://www.nitrc.org/ir', anonymous=True)
    resources = pk.get_resources(c)

    r = resources.pop()
    assert(len(r) == 4)


def test_007_pickle_bbrc_resource_data():

    bbrc_resources = pk.get_bbrc_resources(x)
    bbrc_resources = [r for r in bbrc_resources if isinstance(r[2], dict)]
    r = bbrc_resources.pop()
    assert(len(r) == 5)
    assert(r[1] == r[2]['experiment_id'])


def test_008_pickle_bbrc_test_data():

    r = x.select.experiment('BBRCDEV_E00375').resource('BBRC_VALIDATOR')
    results, validators = pk.get_bbrc_tests(r, 'ArchivingValidator')

    assert(results['HasUsableT1'] == {'has_passed': True, 'data': ['301']})
    assert(len(validators) == len(list(r.files()))/2)


def test_019_reorder_graphs():
    p = pickle.load(open(config.PICKLE_PATH, 'rb'))
    p = f.filter_data(p, '*')

    project = p['projects'][0]
    project_id = project['id']
    p = f.filter_data(p, project_id)


def test_024_get_overview():
    p = pickle.load(open(config.PICKLE_PATH, 'rb'))

    projects = [e['id'] for e in p['projects']]
    p = f.filter_data(p, projects)

    import dashboards.pickle
    dashboards.pickle.get_stats(p)


def test_025_get_project_view():
    p = pickle.load(open(config.PICKLE_PATH, 'rb'))

    project = p['projects'][0]
    project_id = project['id']
    p = f.filter_data(p, project_id)
    project_details = pk.get_project_details(p)

    br = [e for e in p['resources'] if len(e) > 4]

    import pandas as pd
    columns = ['Project', 'Session', 'archiving_validator', 'BBRC_Validators',
               'Insert date']
    data = pd.DataFrame(br, columns=columns).set_index('Session')

    dd = bbrc.diff_dates(data)

    if br[0][3] != 0:  # archiving_validator
        test_grid = bbrc.build_test_grid(p)

    graphs = [g.ProjectGraph, g.SubjectGraph, g.PerProjectSessionGraph,
              g.SessionGraph, g.SessionsPerSubjectGraph, g.ScanQualityGraph,
              g.ResourcePerTypeGraph, g.ResourcesPerSessionGraph,
              g.UsableT1SessionGraph, g.ResourcesOverTimeGraph,
              g.ValidatorGraph,
              g.ConsistentAcquisitionDateGraph,
              g.ScanTypeGraph, g.ScansPerSessionGraph,
              g.VersionGraph,
              g.DateDifferenceGraph]
    # Collect graphs and select them based on access rights
    graphs = [v() for v in graphs]
    graphs = [e.get_chart(i, p) for i, e in enumerate(graphs)]


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
            sess['projects'] = ['*']
            sess['graphs'] = []

    response_get_stats = c.get('dashboard/overview/').status_code
    assert response_get_stats == 200
