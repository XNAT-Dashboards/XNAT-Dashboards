from xnat_dashboards.data_cleaning import data_formatter as df
import pickle
import xnat_dashboards
import os.path as op

pickle_path = op.join(op.dirname(xnat_dashboards.__file__), 'config', 'test_save.pickle')

def test_get_projects_details():

    with open(pickle_path, 'rb') as handle:
        data = pickle.load(handle)

    projects = data['info']['projects']
    project_details = df.Formatter().get_projects_details(projects)

    assert isinstance(project_details['Number of Projects'], int)
    assert isinstance(project_details['Projects Visibility'], dict)

    assert project_details['Number of Projects'] != 0
    assert len(project_details['Projects Visibility']) != 0



def test_get_subjects_details():

    with open(pickle_path, 'rb') as handle:
        data = pickle.load(handle)

    subjects = data['info']['subjects']
    subject_details = df.Formatter().get_subjects_details(subjects)

    assert isinstance(subject_details['Number of Subjects'], int)
    assert isinstance(subject_details['Age Range'], dict)
    assert isinstance(subject_details['Gender'], dict)
    assert isinstance(subject_details['Handedness'], dict)
    assert isinstance(subject_details['Subjects/Project'], dict)

    assert subject_details['Number of Subjects'] != 0
    assert len(subject_details['Age Range']) != 0
    assert len(subject_details['Gender']) != 0
    assert len(subject_details['Handedness']) != 0
    assert len(subject_details['Subjects/Project']) != 0


def test_get_experiments_details():

    with open(pickle_path, 'rb') as handle:
        data = pickle.load(handle)

    experiments = data['info']['experiments']
    experiments_details = df.Formatter().get_experiments_details(experiments)

    assert isinstance(experiments_details['Number of Experiments'], int)
    assert isinstance(experiments_details['Experiments/Project'], dict)
    assert isinstance(experiments_details['Experiment Types'], dict)

    assert experiments_details['Number of Experiments'] != 0
    assert len(experiments_details['Experiments/Project']) != 0
    assert len(experiments_details['Experiment Types']) != 0


def test_get_scans_details():

    with open(pickle_path, 'rb') as handle:
        data = pickle.load(handle)

    scans = data['info']['scans']
    scans_details = df.Formatter().get_scans_details(scans)

    assert isinstance(scans_details['Number of Scans'], int)
    assert isinstance(scans_details['Scans/Project'], dict)
    assert isinstance(scans_details['Scans Quality'], dict)
    assert isinstance(scans_details['Scan Types'], dict)
    assert isinstance(scans_details['XSI Scan Types'], dict)

    assert scans_details['Number of Scans'] != 0
    assert len(scans_details['Scans/Project']) != 0
    assert len(scans_details['Scans Quality']) != 0
    assert len(scans_details['Scan Types']) != 0
    assert len(scans_details['XSI Scan Types']) != 0


def test_get_resources_details():

    with open(pickle_path, 'rb') as handle:
        data = pickle.load(handle)

    resources = data['resources']
    resource_details = df.Formatter().get_resources_details(resources)

    assert isinstance(resource_details, dict)
    assert len(resource_details) != 0

