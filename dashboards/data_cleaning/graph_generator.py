import json
from dashboards.data_cleaning import data_filter as df
from dashboards.bbrc import data_filter as dfb
from dashboards import config


class GraphGenerator:

    def __init__(self, filtered, bbrc_filtered, p):

        self.counter_id = 0
        self.filtered = filtered  # df.DataFilter(p, projects)

        self.ordered_graphs = self.filtered.reorder_graphs()
        self.ordered_graphs.update(bbrc_filtered.reorder_graphs())

    def add_graph_fields(self, graphs, role):
        # Load configuration
        j = json.load(open(config.DASHBOARD_CONFIG_PATH))
        self.graphs = j['graphs']

        # non_graph that don't require plotting
        non_graph = ['Stats', 'test_grid', 'Project details']

        for graph in graphs:
            # Skip if key is not a graph
            if graph in non_graph or role not in self.graphs[graph]['visibility']:
                continue

            # Addition of graph id, js need distinct graph id for each
            # graphs
            graphs[graph]['id'] = self.counter_id
            self.counter_id = self.counter_id + 1

            # Type of graph (bar, line, etc) from config file
            graphs[graph]['graph_type'] = self.graphs[graph]['type']
            # Description of graph from config file
            graphs[graph]['graph descriptor'] = self.graphs[graph]['description']
            # Graph color from config file
            graphs[graph]['color'] = self.graphs[graph]['color']

        return graphs

    def get_overview(self, role):
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

        overview = self.add_graph_fields(self.ordered_graphs, role)

        for graph in overview:
            if graph == 'Stats' or role not in self.graphs[graph]['visibility']:

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
            scans, resources, extra_resources
        project_visible (list, optional): list of project that should be
            visible to the user.
    """

    def __init__(self, project_id, role, p, project_visible=None):

        self.counter_id = 0
        self.role = role
        filtered = df.DataFilterPP()
        self.ordered_graphs = filtered.reorder_graphs_pp(p, project_id)

        dfpp = dfb.DataFilterPP(p['resources'], project_id)
        dfpp = dfpp.reorder_graphs_pp()

        self.ordered_graphs.update(dfpp)

    def get_project_view(self):

        length_check = 0
        graphs_2d_list = []
        graphs_1d_list = []
        counter = 0

        # Do the required addition using field addition
        project_view = self.add_graph_fields(self.ordered_graphs, self.role)

        if isinstance(project_view, int) or project_view is None:
            return project_view

        non_graph = ['Stats', 'test_grid', 'Project details']

        # Loop through each graph field and add it into
        # graph 2d array where each row have 2 columns and each
        # columns contains single graph
        for graph in project_view:
            if graph in non_graph or\
                    self.role not in\
                    self.graphs[graph]['visibility']:

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

        graph_stats_data = [graphs_2d_list, project_view['Stats'],
                            project_view['Project details']]

        # Test grid is a specific dashboard for BBRC XNATs
        # not visible to normal xnat instance
        if 'test_grid' in project_view:
            graph_stats_data.append(project_view['test_grid'])
        else:
            graph_stats_data.append([[], [], []])

        return graph_stats_data
