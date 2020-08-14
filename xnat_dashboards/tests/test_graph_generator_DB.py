from xnat_dashboards.saved_data_processing import graph_generator_DB


def create_mocker(
    mocker, username, info, role, graph_visibility, return_get_project_list,
        project_visible=None, resources=None, resources_bbrc=None):

    mocker.patch(
        'xnat_dashboards.saved_data_processing.get_info_DB.GetInfo.__init__',
        return_value=None)
    mocker.patch(
        'xnat_dashboards.saved_data_processing.get_info_DB.GetInfo.get_project_list',
        return_value=return_get_project_list)
    mocker.patch(
        'xnat_dashboards.saved_data_processing.get_info_DB.GetInfo.get_info',
        return_value=info)

    graph_object = graph_generator_DB.GraphGenerator(
        username, info, role, {role: ['p1', 'y']})

    return graph_object


def test_graph_preprocessor(mocker):

    info = {
        "Age Range": {"x1": "y1", "x2": "y2"},
        "Gender": {"x1": "y1", "x2": "y2"},
        "Handedness": {"x1": "y1", "x2": "y2"},
        "Experiments/Project": {"x1": "y1", "x2": "y2"}, "Stats": {}}

    graph_object = create_mocker(
        mocker, 'testUser', info, 'guest', ['*'],
        {'project_list': ['p1', 'p2'], 'project_list_ow_co_me': ['p3', 'p4']})
    assert type(graph_object.graph_pre_processor(info)) == dict

    graph_object = create_mocker(
        mocker, 'testUser', info, 'guest', ["*"],
        {'project_list': [], 'project_list_ow_co_me': []})

    assert type(graph_object.graph_pre_processor(info)) == dict

    graph_object = create_mocker(
        mocker, 'testUser', 1, 'guest', ["*"],
        {'project_list': [], 'project_list_ow_co_me': []})

    assert graph_object.graph_pre_processor([]) == []


def test_graph_generator(mocker):

    info = {
        "Age Range": {"x1": "y1", "x2": "y2"},
        "Gender": {"x1": "y1", "x2": "y2"},
        "Handedness": {"x1": "y1", "x2": "y2"},
        "Experiments/Project": {"x1": "y1", "x2": "y2"}, "Stats": {}}

    graph_object = create_mocker(
        mocker, 'testUser', info, 'guest', ["*"],
        {'project_list': ['p1', 'p2'], 'project_list_ow_co_me': ['p3', 'p4']})

    assert type(graph_object.graph_generator()) == list
    assert type(graph_object.graph_generator()[0]) == list
    assert type(graph_object.graph_generator()[1]) == dict

    graph_object = create_mocker(
        mocker, 'testUser', 1, 'guest', ["*"],
        {'project_list': [], 'project_list_ow_co_me': []})

    assert graph_object.graph_generator() == 1


def test_project_list_generator(mocker):

    info = {
        "Age Range": {"x1": "y1", "x2": "y2"},
        "Gender": {"x1": "y1", "x2": "y2"},
        "Handedness": {"x1": "y1", "x2": "y2"},
        "Experiments/Project": {"x1": "y1", "x2": "y2"}, "Stats": {}}

    graph_object = create_mocker(
        mocker, 'testUser', info, 'guest', ['p1'],
        {'project_list': ['p1', 'p2'], 'project_list_ow_co_me': ['p3', 'p4']})

    project_list = graph_object.project_list_generator()
    assert type(project_list) == list
    assert type(project_list[0]) == list
    assert type(project_list[1]) == list

    graph_object = create_mocker(
        mocker, 'testUser', info, 'guest', ["*"],
        {'project_list': [], 'project_list_ow_co_me': []})

    assert graph_object.project_list_generator() == [[[]], [[]]]

    graph_object = create_mocker(
        mocker, 'testUser', info, 'guest', ["*"],
        {'project_list': 1, 'project_list_ow_co_me': 1})
    assert graph_object.project_list_generator() == 1
