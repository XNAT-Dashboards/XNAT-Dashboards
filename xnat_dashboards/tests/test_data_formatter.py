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