from xnat_dashboards.data_cleaning import graph_generator
from xnat_dashboards import path_creator

path_creator.set_dashboard_config_path(
    'xnat_dashboards/config/dashboard_config.json')


def create_mocker(
        mocker, username, data, project_id, role,
        graph_visibility,
        project_visible=None):

    mocker.patch(
        'xnat_dashboards.data_cleaning.data_filter.DataFilterPP.__init__',
        return_value=None)
    mocker.patch(
        'xnat_dashboards.data_cleaning.data_filter.DataFilterPP.'
        'get_per_project_view',
        return_value=data['info'])

    graph_object = graph_generator.GraphGeneratorPP(
        username, project_id, role, data, {role: ['p1', 'y']})

    return graph_object


def test_graph_generator(mocker):

    data = {
        'info': {
            "Age Range": {"x1": "y1", "x2": "y2"},
            "Gender": {"x1": "y1", "x2": "y2"},
            "Handedness": {"x1": "y1", "x2": "y2"},
            "Stats": {},
            "Project details": {}},
        "Experiments/Project": {"x1": "y1", "x2": "y2"}, 'test_grid': [],
        'resources': {}}

    graph_object = create_mocker(
        mocker, 'testUser', data, 'p2', 'guest', ['p1'])

    assert type(graph_object.graph_generator()) == list
    assert type(graph_object.graph_generator()[0]) == list
    assert type(graph_object.graph_generator()[1]) == dict
    assert type(graph_object.graph_generator()[2]) == dict

