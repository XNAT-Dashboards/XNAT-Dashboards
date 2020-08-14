from xnat_dashboards.saved_data_processing import graph_generator_DB


def create_mocker(
        mocker, username, info, project_id, role,
        graph_visibility,
        project_visible=None, resources=None, resources_bbrc=None):

    mocker.patch(
        'xnat_dashboards.saved_data_processing.get_info_DB.GetInfoPP.__init__',
        return_value=None)
    mocker.patch(
        'xnat_dashboards.saved_data_processing.get_info_DB.GetInfoPP.get_per_project_view',
        return_value=info)

    graph_object = graph_generator_DB.GraphGeneratorPP(
        username, info, project_id, role, {role: ['p1', 'y']})

    return graph_object


def test_graph_generator(mocker):

    info = {
        "Age Range": {"x1": "y1", "x2": "y2"},
        "Gender": {"x1": "y1", "x2": "y2"},
        "Handedness": {"x1": "y1", "x2": "y2"},
        "Experiments/Project": {"x1": "y1", "x2": "y2"}, "Stats": {},
        "Project details": {}, 'test_grid': []}

    graph_object = create_mocker(
        mocker, 'testUser', info, 'p2', 'guest', ['p1'])

    assert type(graph_object.graph_generator()) == list
    assert type(graph_object.graph_generator()[0]) == list
    assert type(graph_object.graph_generator()[1]) == dict
    assert type(graph_object.graph_generator()[2]) == dict

    graph_object = create_mocker(
        mocker, 'testUser', 1, 'p2', 'guest', ['p1'])

    assert graph_object.graph_generator() == 1
