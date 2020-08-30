from xnat_dashboards.data_cleaning import graph_generator
from xnat_dashboards import config


config.DASHBOARD_CONFIG_PATH = 'xnat_dashboards/config/dashboard_config.json'
config.PICKLE_PATH = 'xnat_dashboards/config/general.pickle'


def create_mocker(
    mocker, username, data, role, graph_visibility, return_get_project_list,
        project_visible=None):

    mocker.patch(
        'xnat_dashboards.data_cleaning.data_filter.DataFilter.__init__',
        return_value=None)
    mocker.patch(
        'xnat_dashboards.data_cleaning.data_filter.DataFilter.'
        'get_project_list',
        return_value=return_get_project_list)
    mocker.patch(
        'xnat_dashboards.data_cleaning.data_filter.DataFilter.reorder_graphs',
        return_value=data['info'])

    graph_object = graph_generator.GraphGenerator(
        username, role, data, {role: ['p1', 'y']})

    return graph_object


def test_graph_preprocessor(mocker):

    data = {
        'info': {
            "Age Range": {"x1": "y1", "x2": "y2"},
            "Gender": {"x1": "y1", "x2": "y2"},
            "Handedness": {"x1": "y1", "x2": "y2"},
            "Experiments/Project": {"x1": "y1", "x2": "y2"}, "Stats": {}
            },
        'resources': {},
        'longitudinal_data': {}
    }

    graph_object = create_mocker(
        mocker, 'testUser', data, 'admin', ['*'],
        {'project_list': ['p1', 'p2'], 'project_list_ow_co_me': ['p3', 'p4']})
    assert isinstance(graph_object.add_graph_fields(data['info']), dict)

    graph_object = create_mocker(
        mocker, 'testUser', data, 'admin', ["*"],
        {'project_list': [], 'project_list_ow_co_me': []})

    assert isinstance(graph_object.add_graph_fields(data['info']), dict)

    graph_object = create_mocker(
        mocker, 'testUser', data, 'admin', ["*"],
        {'project_list': [], 'project_list_ow_co_me': []})

    assert graph_object.add_graph_fields([]) == []


def test_graph_generator(mocker):

    data = {
        'info': {
            "Age Range": {"x1": "y1", "x2": "y2"},
            "Gender": {"x1": "y1", "x2": "y2"},
            "Handedness": {"x1": "y1", "x2": "y2"},
            "Stats": {}},
        "Experiments/Project": {"x1": "y1", "x2": "y2"},
        "resources": {},
        'longitudinal_data': {}}

    graph_object = create_mocker(
        mocker, 'testUser', data, 'admin', ["*"],
        {'project_list': ['p1', 'p2'], 'project_list_ow_co_me': ['p3', 'p4']})

    assert isinstance(graph_object.get_overview(), list)
    assert isinstance(graph_object.get_overview()[0], list)
    assert isinstance(graph_object.get_overview()[1], dict)


def test_project_list_generator(mocker):

    data = {
        "info": {
            "Age Range": {"x1": "y1", "x2": "y2"},
            "Gender": {"x1": "y1", "x2": "y2"},
            "Handedness": {"x1": "y1", "x2": "y2"},
            "Stats": {}},
        "Experiments/Project": {"x1": "y1", "x2": "y2"},
        "resources": {},
        'longitudinal_data': {}}

    graph_object = create_mocker(
        mocker, 'testUser', data, 'admin', ['p1'],
        {'project_list': ['p1', 'p2'], 'project_list_ow_co_me': ['p3', 'p4']})

    project_list = graph_object.get_project_list()
    assert isinstance(project_list, list)
    assert isinstance(project_list[0], list)
    assert isinstance(project_list[1], list)

    graph_object = create_mocker(
        mocker, 'testUser', data, 'admin', ["*"],
        {'project_list': [], 'project_list_ow_co_me': []})

    assert graph_object.get_project_list() == [[[]], [[]]]

    graph_object = create_mocker(
        mocker, 'testUser', data, 'admin', ["*"],
        {'project_list': 1, 'project_list_ow_co_me': 1})
    assert graph_object.get_project_list() == 1


def test_graph_generator_longitudinal(mocker):

    gp = {
        "Projects": {}, "Subjects": {}, "Experiments": {},
        "Scans": {}, "Resources": {}}

    data = {
        "info": {
            "Age Range": {"x1": "y1", "x2": "y2"},
            "Gender": {"x1": "y1", "x2": "y2"},
            "Handedness": {"x1": "y1", "x2": "y2"},
            "Stats": {}},
        "Experiments/Project": {"x1": "y1", "x2": "y2"},
        "resources": {},
        'longitudinal_data': gp}

    graph_object = create_mocker(
        mocker, 'testUser', data, 'admin', ['p1'],
        {'project_list': ['p1', 'p2'], 'project_list_ow_co_me': ['p3', 'p4']})

    ld = graph_object.get_longitudinal_graphs()
    assert isinstance(ld, list)
