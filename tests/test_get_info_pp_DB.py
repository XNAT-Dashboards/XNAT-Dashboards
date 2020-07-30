from saved_data_processing import get_info_DB


def create_mocker(
    mocker, username, info, role,
        project_visible=['p1', 'p2', 'p3', 'p4'],
        resources=None, resources_bbrc=None):

    mocker.patch(
        'saved_data_processing.data_formatter_DB.FormatterPP.__init__',
        return_value=None)

    info_object = get_info_DB.GetInfoPP(
        username, info, 'p2', role, project_visible, resources, resources_bbrc)

    return info_object


def test_info(mocker):

    info = {
        "projects": [{"id": "p3", "g1": {"x1": "y1", "x2": "y2"}}],
        "subjects": [{"project": "p3", "g1": {"x1": "y1", "x2": "y2"}}],
        "experiments": [{"project": "p1", "g1": {"x1": "y1", "x2": "y2"}}],
        "scans": [{"project": "p5", "g1": {"x1": "y1", "x2": "y2"}}],
        "Stats": {}}

    mocker.patch(
        'saved_data_processing.data_formatter_DB.'
        'FormatterPP.get_projects_details',
        return_value={'Number of Projects': 3})
    mocker.patch(
        'saved_data_processing.data_formatter_DB.'
        'FormatterPP.get_subjects_details',
        return_value={'Number of Subjects': 5})
    mocker.patch(
        'saved_data_processing.data_formatter_DB.'
        'FormatterPP.get_experiments_details',
        return_value={'Number of Experiments': 4})
    mocker.patch(
        'saved_data_processing.data_formatter_DB.'
        'FormatterPP.get_scans_details',
        return_value={'Number of Scans': 1})
    mocker.patch(
        'saved_data_processing.data_formatter_DB.'
        'FormatterPP.get_resources_details',
        return_value={})

    mocker.patch(
        'saved_data_processing.data_formatter_DB.'
        'FormatterPP.diff_dates',
        return_value={"count": {}})

    info_object = create_mocker(
        mocker, 'testUser', info, 'guest', {'guest': ['p1', 'p2', 'p3', 'p4']},
        resources={'resources': ['p1', 'res']},
        resources_bbrc={'resources': ['p3', 'res']})

    info = info_object.get_per_project_view()

    assert type(info) == dict   # Return type should be a dict
    assert len(info) == 2     # Currently 11 dicts to be returned
