from xnat_dashboards.data_cleaning import data_formatter as df
import pyxnat
import pickle
import os.path as op
import xnat_dashboards

fp = op.join(op.dirname(xnat_dashboards.__file__), '..', '.xnat.cfg')
x = pyxnat.Interface(config=fp)
pickle_path = 'xnat_dashboards/config/test.pickle'

def test_get_projects_details():

    with open(pickle_path, 'rb') as handle:
        data = pickle.load(handle)

    projects = data['info']['projects']
    project_details = df.Formatter().get_projects_details(projects)

    assert isinstance(project_details['Number of Projects'], int)
    assert isinstance(project_details['Projects Visibility'], dict)

    project_details_specific = df.Formatter.get_projects_details_specific(projects)

    assert isinstance(project_details_specific, dict)