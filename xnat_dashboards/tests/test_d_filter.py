from xnat_dashboards.data_cleaning import data_filter


def create_mocker(
    mocker, username, info, role,
        project_visible=[], resources=None):

    mocker.patch(
        'xnat_dashboards.data_cleaning.data_formatter.Formatter.__init__',
        return_value=None)

    info_object = data_filter.DataFilter(
        username, info, role, [], resources)

    return info_object


def test_info(mocker):

    info = {
        "projects": [{"id": "p3", "g1": {"x1": "y1", "x2": "y2"}}],
        "subjects": [{"project": "p3", "g1": {"x1": "y1", "x2": "y2"}}],
        "experiments": [{"project": "p1", "g1": {"x1": "y1", "x2": "y2"}}],
        "scans": [{"project": "p5", "g1": {"x1": "y1", "x2": "y2"}}],
        "Stats": {}}

    mocker.patch(
        'xnat_dashboards.data_cleaning.data_formatter.'
        'Formatter.get_projects_details',
        return_value={'Number of Projects': 3})
    mocker.patch(
        'xnat_dashboards.data_cleaning.data_formatter.'
        'Formatter.get_subjects_details',
        return_value={'Number of Subjects': 5})
    mocker.patch(
        'xnat_dashboards.data_cleaning.data_formatter.'
        'Formatter.get_experiments_details',
        return_value={'Number of Experiments': 4})
    mocker.patch(
        'xnat_dashboards.data_cleaning.data_formatter.'
        'Formatter.get_scans_details',
        return_value={'Number of Scans': 1})
    mocker.patch(
        'xnat_dashboards.data_cleaning.data_formatter.'
        'Formatter.get_resources_details',
        return_value={})

    info_object = create_mocker(
        mocker, 'testUser', info, 'guest',
        resources=['p1', 'res'])

    assert isinstance(info_object.get_info(), dict)  # Dict
    assert len(info) == 5     # Currently 15 dicts to be returned


def test_get_project_list(mocker):

    info = {
        "projects": [{"id": "p3", "g1": {"x1": "y1", "x2": "y2"}}],
        "subjects": [{"project": "p3", "g1": {"x1": "y1", "x2": "y2"}}],
        "experiments": [{"project": "p1", "g1": {"x1": "y1", "x2": "y2"}}],
        "scans": [{"project": "p5", "g1": {"x1": "y1", "x2": "y2"}}],
        "Stats": {}}

    mocker.patch(
        'xnat_dashboards.data_cleaning.data_formatter.'
        'Formatter.get_projects_details_specific',
        return_value=[
            'p1', 'p2', 'p3', 'p4', 'p1', 'p2',
            'p3', 'p4', 'p1', 'p2', 'p3', 'p4'])

    info_object = create_mocker(
        mocker, 'testUser', info, 'guest',
        resources=['p1', 'res'])

    assert isinstance(info_object.get_project_list(), list)
