import json
from xnat_dashboards.saved_data_processing import get_info_DB
from xnat_dashboards import path_creator


class GraphGenerator:

    data = {}
    project_list = []
    project_list_ow_co_me = []

    def __init__(
            self, username, info, l_data, role,
            project_visible=None, resources=None, resources_bbrc=None):

        self.info = get_info_DB.GetInfo(
            username, info,
            role, project_visible, resources, resources_bbrc)

        projects_data_dict = self.info.get_project_list()

        self.counter_id = 0
        self.role = role
        self.l_data = l_data
        self.data = self.info.get_info()
        self.project_list = projects_data_dict['project_list']
        self.project_list_ow_co_me =\
            projects_data_dict['project_list_ow_co_me']

    def graph_pre_processor(self, data):

        '''
        Add graph type and id for html using the graph_type.json file
        returns a dictionary which will have id and graph type for the
        html file
        '''

        with open(path_creator.get_dashboard_config_path()) as json_file:
            self.graph_config = json.load(json_file)['graph_config']

        if type(data) != dict:
            return data

        final_json_dict = data

        for final_json in final_json_dict:
            if final_json == 'Stats' or\
                final_json == 'test_grid' or\
                final_json == 'Project details' or\
                self.role\
                    not in self.graph_config[final_json]['visibility']:
                continue

            final_json_dict[final_json]['id'] = self.counter_id
            self.counter_id = self.counter_id + 1

            final_json_dict[final_json]['graph_type'] =\
                self.graph_config[final_json]['type']
            final_json_dict[final_json]['graph descriptor'] =\
                self.graph_config[final_json]['description']
            final_json_dict[final_json]['color'] =\
                self.graph_config[final_json]['color']

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

        graph_data = self.graph_pre_processor(self.data)

        if type(graph_data) == int:
            return graph_data

        for final_json in graph_data:
            if final_json == 'Stats' or\
                self.role\
                    not in self.graph_config[final_json]['visibility']:
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

        return [array_2d, graph_data['Stats']]

    def project_list_generator(self):
        '''
        Returns a the names of project based in a 2dArray
        To be processed by frontend

        ow_co_me means owned_collob_member all variables
        with this suffix represent the project list for
        owned collaborated or member list
        '''
        length_check = 0
        length_check_ow_co_me = 0
        array_2d = []
        array_1d = []
        array_1d_ow_co_me = []
        array_2d_ow_co_me = []
        counter = 0
        counter_ow_co_me = 0

        list_data = self.project_list

        list_data_ow_co_me = self.project_list_ow_co_me

        if type(list_data) == int:
            return list_data

        if len(list_data) == 0:
            array_2d = [[]]
        else:
            for data in list_data:
                array_1d.append(data)
                counter = counter + 1
                if counter == 4 or length_check == len(list_data) - 1:
                    counter = 0
                    array_2d.append(array_1d)
                    array_1d = []

                length_check = length_check + 1

        if len(self.project_list_ow_co_me) == 0:
            array_2d_ow_co_me = [[]]
        else:
            for data in list_data_ow_co_me:

                array_1d_ow_co_me.append(data)
                counter_ow_co_me = counter_ow_co_me + 1

                if counter_ow_co_me == 4\
                   or length_check_ow_co_me == len(list_data_ow_co_me) - 1:

                    counter_ow_co_me = 0
                    array_2d_ow_co_me.append(array_1d_ow_co_me)
                    array_1d_ow_co_me = []

                length_check_ow_co_me = length_check_ow_co_me + 1

        '''
            Returns a nested list
            [
                array_list for all projects[
                    [p1 ,p2, p3, p4]
                    [p5 ,p6, p7, p8]
                ]
                array_list for ow_co_me projects[
                    [p1 ,p2, p3, p4]
                    [p5 ,p6, p7, p8]
                ]
            ]
        '''

        return [array_2d, array_2d_ow_co_me]

    def graph_generator_longitudinal(self):

        length_check = 0
        array_2d = []
        array_1d = []
        counter = 0

        if self.l_data is None or self.role != 'admin':
            return [[], []]

        lg_data = self.graph_pre_processor(self.l_data)

        for final_json in lg_data:
            if self.role\
                    not in self.graph_config[final_json]['visibility']:
                length_check = length_check + 1
                continue

            array_1d.append({final_json: lg_data[final_json]})
            counter = counter + 1
            if counter == 2 or length_check == len(lg_data) - 1:
                counter = 0
                array_2d.append(array_1d)
                array_1d = []

            length_check = length_check + 1

        return array_2d


class GraphGeneratorPP(GraphGenerator):

    data = None
    project_id = ''

    def __init__(
            self,
            username,
            info, project_id, role, project_visible=None,
            resources=None, resources_bbrc=None):

        info = get_info_DB.GetInfoPP(
            username, info, project_id, role, project_visible,
            resources, resources_bbrc)

        self.counter_id = 0
        self.role = role
        self.data = info.get_per_project_view()

    def graph_generator(self):

        '''
        Returns a 2d array with each row having 2 columns which will
        be used in the html
        '''

        length_check = 0
        array_2d = []
        array_1d = []
        counter = 0

        graph_data = self.graph_pre_processor(self.data)

        if type(graph_data) == int or graph_data is None:
            return graph_data

        for final_json in graph_data:
            if final_json == 'Stats' or\
                final_json == 'test_grid' or\
                final_json == 'Project details' or\
                    self.role not in\
                    self.graph_config[final_json]['visibility']:

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
        return [
            array_2d, graph_data['Stats'],
            graph_data['Project details'], graph_data['test_grid']]
