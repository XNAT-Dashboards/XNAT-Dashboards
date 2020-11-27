from xnat_dashboards.data_cleaning import data_formatter as df
import pickle

pickle_path = 'xnat_dashboards/config/test.pickle'

def test_get_projects_details():

    with open(pickle_path, 'rb') as handle:
        data = pickle.load(handle)

    projects = data['info']['projects']
    project_details = df.Formatter().get_projects_details(projects)

    assert isinstance(project_details['Number of Projects'], int)
    assert isinstance(project_details['Projects Visibility'], dict)
    assert len(project_details['Number of Projects'] != 0)
    assert len(project_details['Projects Visibility'] != 0)


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

    assert len(subject_details['Number of Subjects'] != 0)
    assert len(subject_details['Age Range'] != 0)
    assert len(subject_details['Gender'] != 0)
    assert len(subject_details['Handedness'] != 0)
    assert len(subject_details['Subjects/Project'] != 0)


def test_get_experiments_details():

    with open(pickle_path, 'rb') as handle:
        data = pickle.load(handle)

    experiments = data['info']['experiments']
    experiments_details = df.Formatter().get_experiments_details(experiments)

    assert isinstance(experiments_details['Number of Experiments'], int)
    assert isinstance(experiments_details['Experiments/Project'], dict)
    assert isinstance(experiments_details['Experiment Types'], dict)

    assert len(experiments_details['Number of Experiments'] != 0)
    assert len(experiments_details['Experiments/Project'] != 0)
    assert len(experiments_details['Experiment Types'] != 0)