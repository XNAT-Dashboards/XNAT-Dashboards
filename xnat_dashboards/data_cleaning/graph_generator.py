import json
from xnat_dashboards.data_cleaning import data_filter
from xnat_dashboards.bbrc import data_filter as data_filter_b
from xnat_dashboards import path_creator


class GraphGenerator:
    """Class for making final changes in data.

    This class makes final changes that are then sent to frontend.
    Which is then displayed using jinja.

    Args:
        username (list): Name of the user
        info (str): project, subject, experiment and scan details.
        project_visible (list, optional): list of project that should be
            visible to the user.
        role (str): Role assigned to user.
        data (dict): Dict containing data of projects, subjects, exp.,
            scans, resources, extra_resources, longitudinal data
    """
    data = {}
    project_list = []
    project_list_ow_co_me = []

    def __init__(
            self, username, role, data, project_visible=None):

        if 'resources' not in data:
            data['resources'] = None

        self.info = data_filter.DataFilter(
            username, data['info'],
            role, project_visible, data['resources'])

        projects_data_dict = self.info.get_project_list()

        self.counter_id = 0
        self.role = role
        self.l_data = data['longitudinal_data']
        self.data_ordered = self.info.get_info()

        if 'extra_resources' in data:
            self.data_ordered.update(
                data_filter_b.DataFilter(
                    role, project_visible,
                    data['extra_resources']).get_info())

        self.project_list = projects_data_dict['project_list']
        self.project_list_ow_co_me =\
            projects_data_dict['project_list_ow_co_me']

    def graph_pre_processor(self, data):
        """It pre process the data received from GetInfo.

        Graph pre processor add data regarding graph type ie.
        bar, pie etc, graph description, graph color, graph id.

        It also skip graph that should not be visible to user
        as per role.

        Args:
            data (dict): Data of graphs and information from GetInfo

        Returns:
            dict: Data to frontend.
        """

        with open(path_creator.get_dashboard_config_path()) as json_file:
            self.graph_config = json.load(json_file)['graph_config']

        if type(data) != dict:
            return data

        final_json_dict = data

        skip_data = ['Stats', 'test_grid', 'Project details']

        for final_json in final_json_dict:
            if final_json in skip_data or\
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

        return final_json_dict

    def graph_generator(self):
        """This first process the data using graph preprocessor.
        Then create a 2D array that help in distribution of graph
        in frontend. Where each row contains 2 graph.

        Returns:
            list: 2D array of graphs and other information.
        """

        length_check = 0
        array_2d = []
        array_1d = []
        counter = 0

        graph_data = self.graph_pre_processor(self.data_ordered)
        print(graph_data)
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
        """
        Process the project list for displaying the project id.

        Returns:
            array_2D (list): The id of project based in a 2dArray
            To be processed by frontend
            array_2d_ow_co_me (list): arrayow_co_me means
            owned_collob_member all variables with this suffix
            represent the project list for owned collaborated or member list
        """
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
        """Graphs for longitudinal data. Visible to
        admin role only.

        Returns:
            list: 2D array of graphs and other information.
        """

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
    """Class for making final changes in data for per project view.
    Inherits GraphGenerator class.
    This class makes final changes that are then sent to frontend.
    Which is then displayed using jinja.

    Args:
        username (list): Name of the user
        project_id (str): id of the project.
        role (str): role assigned to the user.
        data (dict): Dict containing data of projects, subjects, exp.,
            scans, resources, extra_resources, longitudinal data
        project_visible (list, optional): list of project that should be
            visible to the user.
    """

    def __init__(
            self,
            username,
            project_id, role, data, project_visible=None):

        if 'resources' not in data:
            data['resources'] = None

        info_obj = data_filter.DataFilterPP(
            username, data['info'], project_id, role, project_visible,
            data['resources'])

        self.project_id = ''
        self.counter_id = 0
        self.role = role
        self.data_ordered = info_obj.get_per_project_view()

        if 'extra_resources' in data:

            self.data_ordered.update(
                data_filter_b.DataFilterPP(
                    data['info']['experiments'], project_id, role,
                    project_visible,
                    data['extra_resources']).get_per_project_view())

    def graph_generator(self):

        """This first process the data using graph preprocessor
        of parent class.
        Then create a 2D array that help in distribution of graph
        in frontend. Where each row contains 2 graph.

        Returns:
            list: 2D array of graphs and other information.
        """
        length_check = 0
        array_2d = []
        array_1d = []
        counter = 0

        graph_data = self.graph_pre_processor(self.data_ordered)

        if type(graph_data) == int or graph_data is None:
            return graph_data

        skip_data = ['Stats', 'test_grid', 'Project details']

        for final_json in graph_data:
            if final_json in skip_data or\
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

        graph_stats_data = [
            array_2d, graph_data['Stats'],
            graph_data['Project details']]

        if 'test_grid' in graph_data:
            graph_stats_data.append(graph_data['test_grid'])
        else:
            graph_stats_data.append([[], [], []])

        return graph_stats_data
