from xnat_dashboards.saved_data_processing import get_info_DB


def create_mocker(
    mocker, username, info, role,
        project_visible=[], resources=None, resources_bbrc=None):

    mocker.patch(
        'xnat_dashboards.saved_data_processing.data_formatter_DB.Formatter.__init__',
        return_value=None)

    info_object = get_info_DB.GetInfo(
        username, info, role, [], resources, resources_bbrc)

    return info_object


def test_info(mocker):

    info = {
        "projects": [{"id": "p3", "g1": {"x1": "y1", "x2": "y2"}}],
        "subjects": [{"project": "p3", "g1": {"x1": "y1", "x2": "y2"}}],
        "experiments": [{"project": "p1", "g1": {"x1": "y1", "x2": "y2"}}],
        "scans": [{"project": "p5", "g1": {"x1": "y1", "x2": "y2"}}],
        "Stats": {}}

    mocker.patch(
        'xnat_dashboards.saved_data_processing.data_formatter_DB.'
        'Formatter.get_projects_details',
        return_value={'Number of Projects': 3})
    mocker.patch(
        'xnat_dashboards.saved_data_processing.data_formatter_DB.'
        'Formatter.get_subjects_details',
        return_value={'Number of Subjects': 5})
    mocker.patch(
        'xnat_dashboards.saved_data_processing.data_formatter_DB.'
        'Formatter.get_experiments_details',
        return_value={'Number of Experiments': 4})
    mocker.patch(
        'xnat_dashboards.saved_data_processing.data_formatter_DB.'
        'Formatter.get_scans_details',
        return_value={'Number of Scans': 1})
    mocker.patch(
        'xnat_dashboards.saved_data_processing.data_formatter_DB.'
        'Formatter.get_resources_details',
        return_value={})

    info_object = create_mocker(
        mocker, 'testUser', info, 'guest',
        resources=['p1', 'res'],
        resources_bbrc=['p3', 'res'])

    assert type(info_object.get_info()) == dict  # Return type should be a dict
    assert len(info) == 5     # Currently 15 dicts to be returned


def test_get_project_list(mocker):

    info = {
        "projects": [{"id": "p3", "g1": {"x1": "y1", "x2": "y2"}}],
        "subjects": [{"project": "p3", "g1": {"x1": "y1", "x2": "y2"}}],
        "experiments": [{"project": "p1", "g1": {"x1": "y1", "x2": "y2"}}],
        "scans": [{"project": "p5", "g1": {"x1": "y1", "x2": "y2"}}],
        "Stats": {}}

    mocker.patch(
        'xnat_dashboards.saved_data_processing.data_formatter_DB.'
        'Formatter.get_projects_details_specific',
        return_value=[
            'p1', 'p2', 'p3', 'p4', 'p1', 'p2',
            'p3', 'p4', 'p1', 'p2', 'p3', 'p4'])

    info_object = create_mocker(
        mocker, 'testUser', info, 'guest',
        resources=['p1', 'res'],
        resources_bbrc=['p3', 'res'])

    assert type(info_object.get_project_list()) == list
