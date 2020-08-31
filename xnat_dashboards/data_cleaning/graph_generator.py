import json
from xnat_dashboards.data_cleaning import data_filter
from xnat_dashboards.bbrc import data_filter as data_filter_b
from xnat_dashboards import config


class GraphGenerator:
    """Class for making final changes in data.

    This class makes final changes that are then sent to frontend.
    Which is then displayed using jinja.

    The final changes includes addition of:
    1. id to graphs.
    2. graph description from the dashboard config file.
    3. graph type from the dashboard config file.
    4. default color to graph.

    Then the graph is formatted in a 2D array structure where each
    row contains 2 columns these 2 columns are filled with graphs.

    Args:
        username (list): Name of the user
        info (str): project, subject, experiment and scan details.
        project_visible (list, optional): list of project that should be
            visible to the user by default it will show no project details.
        role (str): Role assigned to user.
        data (dict): Dict containing data of projects, subjects, exp.,
            scans, resources, extra_resources, longitudinal data
    """
    pickle_data = {}
    project_list = []
    project_list_ow_co_me = []
    l_data = {}

    def __init__(
            self, username, role, pickle_data, project_visible=[]):

        self.filtered = data_filter.DataFilter(
            username, pickle_data['info'],
            role, project_visible, pickle_data['resources'])

        projects_data_dict = self.filtered.get_project_list()

        self.counter_id = 0
        self.role = role
        self.l_data = pickle_data['longitudinal_data']
        self.ordered_graphs = self.filtered.reorder_graphs()

        # Check whether extra resources are present in the pickle_data
        if 'extra_resources' in pickle_data\
                and pickle_data['extra_resources'] is not None:
            self.ordered_graphs.update(
                data_filter_b.DataFilter(
                    role, project_visible,
                    pickle_data['extra_resources']).reorder_graphs())

        self.project_list = projects_data_dict['project_list']
        self.project_list_ow_co_me =\
            projects_data_dict['project_list_ow_co_me']

    def add_graph_fields(self, graphs):
        """It pre process the data received from DataFilter.

        Graph field addition add data regarding graph type ie.
        bar, pie etc, graph description, graph color, graph id.

        It also skip graph that should not be visible to user
        as per role.

        Args:
            data (dict): Data of graphs and information that are not plotted
            like Number of subjects, experiment etc from DataFilter.

        Returns:
            dict: Data to frontend.
        """

        # Opens the dashboard_config.json file
        with open(config.DASHBOARD_CONFIG_PATH) as json_file:
            self.graph_config = json.load(json_file)['graph_config']

        if not isinstance(graphs, dict):
            return graphs

        # non_graph that don't require plotting
        non_graph = ['Stats', 'test_grid', 'Project details']

        # Loop through each dict values and if it need to be plotted as
        # graph add the required details from dashboard config file

        for graph in graphs:
            # Skip if key is not a graph
            if graph in non_graph or\
                self.role\
                    not in self.graph_config[graph]['visibility']:
                continue

            # Addition of graph id, js need distinct graph id for each
            # graphs
            graphs[graph]['id'] = self.counter_id
            self.counter_id = self.counter_id + 1

            # Type of graph (bar, line, etc) from config file
            graphs[graph]['graph_type'] =\
                self.graph_config[graph]['type']
            # Description of graph from config file
            graphs[graph]['graph descriptor'] =\
                self.graph_config[graph]['description']
            # Graph color from config file
            graphs[graph]['color'] =\
                self.graph_config[graph]['color']

        return graphs

    def get_overview(self):
        """This first process the data using graph preprocessor.
        Then create a 2D array that help in distribution of graph
        in frontend. Where each row contains 2 graph.

        Returns:
            list: 2D array of graphs and other information.
        """

        length_check = 0
        graphs_2d_list = []
        graphs_1d_list = []
        counter = 0

        overview = self.add_graph_fields(self.ordered_graphs)

        if isinstance(overview, int):
            return overview

        for graph in overview:
            if graph == 'Stats' or\
                self.role\
                    not in self.graph_config[graph]['visibility']:

                # Condition if last key is skipped then add
                # the single column array in overview
                if length_check == len(overview) - 1:
                    graphs_2d_list.append(graphs_1d_list)

                length_check = length_check + 1
                continue

            graphs_1d_list.append({graph: overview[graph]})
            counter = counter + 1

            # Check if we have filled 2 columns or are at the end
            # of the graphs list
            if counter == 2 or length_check == len(overview) - 1:
                counter = 0
                graphs_2d_list.append(graphs_1d_list)
                graphs_1d_list = []

            length_check = length_check + 1

        '''
            Returns a nested list with dict inside
            [
                graphs_2d_list[
                    [project1_info, project2_info]
                    [project3_info, project4_info]
                ]
                overview['Stats']{
                    Projects: count
                    Experiment: count
                    Scans: count
                    Subjects: count
                }
            ]
        '''

        return [graphs_2d_list, overview['Stats']]

    def get_project_list(self):
        """
        Process the project list for displaying the project id.

        Returns:
            project_list_2d (list): The id of project based in a 2dArray
            To be processed by frontend
            project_list_2d_ow_co_me (list): ow_co_me means
            owned_collob_member all variables with this suffix
            represent the project list for owned collaborated or member list
        """
        length_check = 0
        length_check_ow_co_me = 0
        project_list_2d = []
        project_list_1d = []
        project_list_1d_ow_co_me = []
        project_list_2d_ow_co_me = []
        counter = 0
        counter_ow_co_me = 0

        # List of projects
        project_list = self.project_list

        # List of projects that user is a owner, collab or member
        list_data_ow_co_me = self.project_list_ow_co_me

        if isinstance(project_list, int):
            return project_list

        # Create a 2d array with each row containing 4 columns and each column
        # will have single project id
        if len(project_list) == 0:
            project_list_2d = [[]]
        else:
            for project_id in project_list:
                project_list_1d.append(project_id)
                counter = counter + 1
                if counter == 4 or length_check == len(project_list) - 1:
                    counter = 0
                    project_list_2d.append(project_list_1d)
                    project_list_1d = []

                length_check = length_check + 1

        if len(self.project_list_ow_co_me) == 0:
            project_list_2d_ow_co_me = [[]]
        else:
            for project_id in list_data_ow_co_me:

                project_list_1d_ow_co_me.append(project_id)
                counter_ow_co_me = counter_ow_co_me + 1

                if counter_ow_co_me == 4\
                   or length_check_ow_co_me == len(list_data_ow_co_me) - 1:

                    counter_ow_co_me = 0
                    project_list_2d_ow_co_me.append(project_list_1d_ow_co_me)
                    project_list_1d_ow_co_me = []

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

        return [project_list_2d, project_list_2d_ow_co_me]

    def get_longitudinal_graphs(self):
        """Graphs for longitudinal data. Visible to
        admin role only.

        Returns:
            list: 2D array of graphs and other information.
        """

        length_check = 0
        graphs_2d_list = []
        graphs_1d_list = []
        counter = 0

        if self.l_data is None or self.role != 'admin':
            return [[], []]

        l_graphs = self.add_graph_fields(self.l_data)

        for graph in l_graphs:
            if self.role\
                    not in self.graph_config[graph]['visibility']:
                length_check = length_check + 1

                if length_check == len(l_graphs) - 1:
                    graphs_2d_list.append(graphs_1d_list)

                length_check = length_check + 1
                continue

            graphs_1d_list.append({graph: l_graphs[graph]})
            counter = counter + 1
            if counter == 2 or length_check == len(l_graphs) - 1:
                counter = 0
                graphs_2d_list.append(graphs_1d_list)
                graphs_1d_list = []

            length_check = length_check + 1

        return graphs_2d_list


class GraphGeneratorPP(GraphGenerator):
    """Class for making final changes in data for per project view.
    Inherits GraphGenerator class.
    This class makes final changes that are then sent to frontend.
    Which is then displayed using jinja for per project view.

    The final changes includes addition of:
    1. Addition of ID to graphs.
    2. Addition of graph description from the dashboard config file.
    3. Addition of graph type from the dashboard config file.
    4. Addition of default color to graph.

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
            project_id, role, pickle_data, project_visible=None):

        if 'resources' not in pickle_data:
            pickle_data['resources'] = None

        filtered = data_filter.DataFilterPP(
            username, pickle_data['info'], project_id, role, project_visible,
            pickle_data['resources'])

        self.project_id = ''
        self.counter_id = 0
        self.role = role
        self.ordered_graphs = filtered.reorder_graphs_pp()

        if 'extra_resources' in pickle_data and\
                pickle_data['extra_resources'] is not None:

            self.ordered_graphs.update(
                data_filter_b.DataFilterPP(
                    pickle_data['info']['experiments'], project_id, role,
                    project_visible,
                    pickle_data['extra_resources']).reorder_graphs_pp())

    def get_project_view(self):

        """This first process the data using graph preprocessor
        of parent class.
        Then create a 2D array that help in distribution of graph
        in frontend. Where each row contains 2 graph.

        Returns:
            list: 2D array of graphs and other information.
        """
        length_check = 0
        graphs_2d_list = []
        graphs_1d_list = []
        counter = 0

        # Do the required addition using field addition
        project_view = self.add_graph_fields(self.ordered_graphs)

        if isinstance(project_view, int) or project_view is None:
            return project_view

        non_graph = ['Stats', 'test_grid', 'Project details']

        # Loop through each graph field and add it into
        # graph 2d array where each row have 2 columns and each
        # columns contains single graph
        for graph in project_view:
            if graph in non_graph or\
                    self.role not in\
                    self.graph_config[graph]['visibility']:

                # Condition if last key is skipped then add
                # the single column array in project_view
                if length_check == len(project_view) - 1:
                    graphs_2d_list.append(graphs_1d_list)
                length_check = length_check + 1
                continue

            graphs_1d_list.append({graph: project_view[graph]})
            counter = counter + 1

            # Check if we have filled 2 columns or are at the end
            # of the graphs list
            if counter == 2 or length_check == len(project_view) - 1:
                counter = 0
                graphs_2d_list.append(graphs_1d_list)
                graphs_1d_list = []

            length_check = length_check + 1

        '''
            Returns a nested list with dict inside
            [
                graphs_2d_list[
                    [project1_info, project2_info]
                    [project3_info, project4_info]
                ]
                project_view['Stats']{
                    Projects: count
                    Experiment: count
                    Scans: count
                    Subjects: count
                }
            ]
        '''

        graph_stats_data = [
            graphs_2d_list, project_view['Stats'],
            project_view['Project details']]

        # Test grid is a specific dashboard for BBRC XNATs
        # not visible to normal xnat instance
        if 'test_grid' in project_view:
            graph_stats_data.append(project_view['test_grid'])
        else:
            graph_stats_data.append([[], [], []])

        return graph_stats_data
