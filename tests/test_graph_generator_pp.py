from realtime_data_processing import graph_generator_pp
from utils import input_processor
import pathlib

graph_object = graph_generator_pp.GraphGenerator(
    "testUser",
    "testPassword",
    "https://central.xnat.org",
    ssl=False,
    project_id='CENTRAL_OASIS_CS')


def test_graph_preprocessor():

    assert type(graph_object.graph_pre_processor()) == dict


def test_graph_generator():

    assert type(graph_object.graph_generator()) == list
