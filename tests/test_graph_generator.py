from generators import graph_generator
from utils import input_processor
import pathlib

graph_object = graph_generator.GraphGenerator("testUser",
                                              "testPassword",
                                              "https://central.xnat.org")


def test_graph_type_generator():

    input_processor.set_keyboard_input(['bar', 'bar', 'bar', 'bar',
                                        'bar', 'bar', 'bar', 'bar',
                                        'bar', 'bar', 'bar', 'bar',
                                        'bar', 'bar', 'bar'])
    graph_object.graph_type_generator()

    assert pathlib.Path('utils/graph_type.json').exists


def test_graph_preprocessor():

    assert type(graph_object.graph_pre_processor()) == dict


def test_graph_generator():

    assert type(graph_object.graph_generator()) == list


def test_project_list_generator():

    project_list = graph_object.project_list_generator()
    assert type(project_list) == list
    assert type(project_list[0]) == list
    assert type(project_list[1]) == list
