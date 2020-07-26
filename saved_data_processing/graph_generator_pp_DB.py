import sys
from os.path import dirname, abspath
import json
sys.path.insert(0, dirname(dirname(abspath(__file__))))
from saved_data_processing import get_info_DB


class GraphGenerator:

    data = None
    project_id = ''

    def __init__(
            self,
            username,
            info, project_id, role, graph_visibility=None, skip_project=None,
            resources=None, resources_bbrc=None):

        info = get_info_DB.GetInfoPP(
            username, info, project_id, role, skip_project,
            resources, resources_bbrc)
        self.role = role
        self.data = info.get_per_project_view()
        self.graph_visibility = graph_visibility[role]

    def graph_pre_processor(self):

        '''
        Add graph type and id for html using the graph_type.json file
        returns a dictionary which will have id and graph type for the
        html file
        '''

        try:
            with open('utils/graph_config.json') as json_file:
                graph_config = json.load(json_file)
                graph_type = graph_config['graph type']
                graph_descriptor = graph_config['graph descriptor']
        except OSError:
            print(OSError.with_traceback())
            print("graph_type.json file not found run graph_generator")

        counter_id = 0
        final_json_dict = self.data

        if type(final_json_dict) != dict:

            return final_json_dict

        for final_json in final_json_dict:
            if final_json == 'Stats' or\
                final_json == 'Project details' or\
                    final_json not in self.graph_visibility:
                continue

            final_json_dict[final_json]['id'] = counter_id
            counter_id = counter_id + 1
            final_json_dict[final_json]['graph_type'] = graph_type[final_json]
            final_json_dict[final_json]['graph descriptor'] =\
                graph_descriptor[final_json]

        '''
        Returns a nested dict with id and graph type added
        {
            Graph1_name : { x_axis_values, y_axis_values, id, graph_type},
            Graph2_name : { x_axis_values, y_axis_values, id, graph_type},
            Graph3_name : { x_axis_values, y_axis_values, id, graph_type},
            Graph4_name : { x_axis_values, y_axis_values, id, graph_type},
        }
        '''
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

        if type(graph_data) == int or graph_data is None:
            return graph_data

        for final_json in graph_data:
            if final_json == 'Stats' or\
                final_json == 'Project details' or\
                    final_json not in self.graph_visibility:

                length_check = length_check + 1
                continue

            array_1d.append({final_json: graph_data[final_json]})
            counter = counter + 1
            if counter == 2 or length_check == len(graph_data) - 1:
                counter = 0
                array_2d.append(array_1d)
                array_1d = []

            length_check = length_check + 1

        '''
            Returns a nested list with dict inside
            [
                array_2d[
                    [project1_info, project2_info]
                    [project3_info, project4_info]
                ]
                graph_data['Stats']{
                    Projects: count
                    Experiment: count
                    Scans: count
                    Subjects: count
                }
            ]
        '''

        return [array_2d, graph_data['Stats'], graph_data['Project details']]
