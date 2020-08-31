from xnat_dashboards.data_cleaning import data_filter


def create_mocker(
    mocker, username, info, role,
        project_visible=['p1', 'p2', 'p3', 'p4'],
        resources=None):

    mocker.patch(
        'xnat_dashboards.data_cleaning.data_formatter.FormatterPP.__init__',
        return_value=None)

    filtered = data_filter.DataFilterPP(
        username, info, 'p2', role, project_visible, resources)

    return filtered


def test_info(mocker):

    info = {
        "projects": [{"id": "p3", "g1": {"x1": "y1", "x2": "y2"}}],
        "subjects": [{"project": "p3", "g1": {"x1": "y1", "x2": "y2"}}],
        "experiments": [{"project": "p1", "g1": {"x1": "y1", "x2": "y2"}}],
        "scans": [{"project": "p5", "g1": {"x1": "y1", "x2": "y2"}}],
        "Stats": {}}

    mocker.patch(
        'xnat_dashboards.data_cleaning.data_formatter.'
        'FormatterPP.get_projects_details',
        return_value={'Number of Projects': 3})
    mocker.patch(
        'xnat_dashboards.data_cleaning.data_formatter.'
        'FormatterPP.get_subjects_details',
        return_value={'Number of Subjects': 5})
    mocker.patch(
        'xnat_dashboards.data_cleaning.data_formatter.'
        'FormatterPP.get_experiments_details',
        return_value={'Number of Experiments': 4})
    mocker.patch(
        'xnat_dashboards.data_cleaning.data_formatter.'
        'FormatterPP.get_scans_details',
        return_value={'Number of Scans': 1})
    mocker.patch(
        'xnat_dashboards.data_cleaning.data_formatter.'
        'FormatterPP.get_resources_details',
        return_value={})

    filtered = create_mocker(
        mocker, 'testUser', info, 'guest', {'guest': ['p1', 'p2', 'p3', 'p4']},
        resources=['p1', 'res'])

    info = filtered.reorder_graphs_pp()

    assert isinstance(info, dict)   # Return type should be a dict
    assert len(info) == 2     # Currently 2 dicts to be returned
