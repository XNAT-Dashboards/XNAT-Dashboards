from realtime_data_processing import graph_generator

graph_object = graph_generator.GraphGenerator("testUser",
                                              "testPassword",
                                              "https://central.xnat.org",
                                              ssl=False)

def test_graph_preprocessor():

    assert type(graph_object.graph_pre_processor()) == dict


def test_graph_generator():

    assert type(graph_object.graph_generator()) == list


def test_project_list_generator():

    project_list = graph_object.project_list_generator()
    assert type(project_list) == list
    assert type(project_list[0]) == list
    assert type(project_list[1]) == list
