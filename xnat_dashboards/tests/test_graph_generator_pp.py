from xnat_dashboards.data_cleaning import graph_generator
from xnat_dashboards import config

config.DASHBOARD_CONFIG_PATH = 'xnat_dashboards/config/dashboard_config.json'


def create_mocker(
        mocker, username, data, project_id, role,
        graph_visibility,
        project_visible=None):

    mocker.patch(
        'xnat_dashboards.data_cleaning.data_filter.DataFilterPP.__init__',
        return_value=None)
    mocker.patch(
        'xnat_dashboards.data_cleaning.data_filter.DataFilterPP.'
        'reorder_graphs_pp',
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
        mocker, 'testUser', data, 'p2', 'admin', ['p1'])

    assert isinstance(graph_object.get_project_view(), list)
    assert isinstance(graph_object.get_project_view()[0], list)
    assert isinstance(graph_object.get_project_view()[1], dict)
    assert isinstance(graph_object.get_project_view()[2], dict)

