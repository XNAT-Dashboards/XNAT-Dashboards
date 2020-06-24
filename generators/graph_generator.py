import sys
from os.path import dirname, abspath
sys.path.insert(0, dirname(dirname(abspath(__file__))))
from pyxnat_connection import get_info
import json


class GraphGenerator:

    data = {}

    def __init__(self, user, password, server):
        self.data = get_info.GetInfo(user,
                                     password,
                                     server).get_info()

    def graph_type_generator(self):

        '''
        This method create the graph type that will be needed by plotly
        This method creates a json file which have the graphy type with
        corresponding graph title
        '''

        data = self.data
        dict_output = {}

        for json_dict in data:
            dict_output[json_dict] =\
                input("Enter the graph type for graph name "
                      + json_dict + ": ")

        graph_type = json.dumps(dict_output)
        f = open("utils/graph_type.json", "w")
        f.write(graph_type)
        f.close()

    def graph_pre_processor(self):

        '''
        Add graph type and id for html using the graph_type.json file
        returns a dictionary which will have id and graph type for the
        html file
        '''

        try:
            with open('utils/graph_type.json') as json_file:
                graph_type = json.load(json_file)
        except OSError:
            print("graph_type.json file not found\n please"
                  + " generate by running graph_generator.py first")
            exit(1)

        counter_id = 0

        if(type(self.data) != dict):
            return self.data

        final_json_dict = self.data

        for final_json in final_json_dict:
            final_json_dict[final_json]['id'] = counter_id
            counter_id = counter_id + 1
            final_json_dict[final_json]['graph_type'] = graph_type[final_json]

        return final_json_dict

    def graph_generator(self):

        '''
        Returns a 2d array with each row having 2 columns which will
        be used in the html
        '''

        length_check = 0
        array_2d = []
        array_1d = []
        counter = 0

        graph_data = self.graph_pre_processor()
        if(type(graph_data) == int):
            return graph_data

        for final_json in graph_data:
            array_1d.append({final_json: graph_data[final_json]})
            counter = counter + 1
            if(counter == 2 or length_check == len(graph_data)-1):
                counter = 0
                array_2d.append(array_1d)
                array_1d = []

            length_check = length_check+1

        return array_2d


if __name__ == "__main__":
    '''
    This will run and create the graph_type.json file
    '''
    graph_object = GraphGenerator('testUser',
                                  'testPassword',
                                  'https://central.xnat.org')
    graph_object.graph_type_generator()
