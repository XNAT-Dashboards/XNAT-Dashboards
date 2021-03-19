import json
from dashboards import config


class GraphGenerator:

    def __init__(self):
        self.counter_id = 0

    def add_graph_fields(self, graphs, role):
        fp = config.DASHBOARD_CONFIG_PATH
        fp = '/home/grg/git/XNAT-Dashboards/config.json'
        j = json.load(open(fp))

        self.graphs = j['graphs']

        # non_graph that don't require plotting
        non_graph = ['Stats', 'test_grid', 'Project details']

        for graph in graphs:
            # Skip if key is not a graph
            if graph in non_graph or role not in self.graphs[graph]['visibility']:
                continue

            # Addition of graph id, js need distinct graph id for each graphs
            graphs[graph]['id'] = self.counter_id
            self.counter_id = self.counter_id + 1

            # Type of graph (bar, line, etc) from config file
            graphs[graph]['graph_type'] = self.graphs[graph]['type']
            # Description of graph from config file
            graphs[graph]['graph descriptor'] = self.graphs[graph]['description']
            # Graph color from config file
            graphs[graph]['color'] = self.graphs[graph]['color']

        return graphs

    def get_overview(self, overview, role):

        # FIXME: this function looks like it can be improved
        length_check = 0
        graphs_2d_list = []
        graphs_1d_list = []
        counter = 0

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

        return graphs_2d_list


class GraphGeneratorPP(GraphGenerator):

    def __init__(self):
        self.counter_id = 0

    def get_project_view(self, project_view, role):

        length_check = 0
        graphs_2d_list = []
        graphs_1d_list = []
        counter = 0

        # Do the required addition using field addition

        if isinstance(project_view, int) or project_view is None:
            return project_view

        non_graph = ['Stats', 'test_grid', 'Project details']

        # Loop through each graph field and add it into
        # graph 2d array where each row have 2 columns and each
        # columns contains single graph
        for graph in project_view:
            if graph in non_graph or role not in self.graphs[graph]['visibility']:

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

        # graph_stats_data = [graphs_2d_list, project_view['Stats'],
        #                     project_view['Project details']]

        # Test grid is a specific dashboard for BBRC XNATs
        # not visible to normal xnat instance
        # if 'test_grid' in project_view:
        #     graph_stats_data.append(project_view['test_grid'])
        # else:
        #     graph_stats_data.append([[], [], []])


        return graphs_2d_list
