import json
from dashboards.data import filter as df
from dashboards.data import bbrc as dfb
from dashboards import config


class GraphGenerator:

    def __init__(self, filtered, bbrc_filtered, role):

        self.counter_id = 0
        self.ordered_graphs = filtered
        self.ordered_graphs.update(bbrc_filtered)

        fp = '/home/grg/git/XNAT-Dashboards/config.json'
        config.DASHBOARD_CONFIG_PATH = fp
        j = json.load(open(fp))
        non_graph = ['Stats', 'test_grid', 'Project details']
        self.graphs = {k: v for k, v in j['graphs'].items()
                           if k not in non_graph
                           and role in j['graphs'][k]['visibility']}

    def add_graph_fields(self):

        graphs = []
        for k, v in self.graphs.items():

            # Addition of graph id, js need distinct graph id for each graphs
            g = {}
            g['id'] = self.counter_id
            self.counter_id = self.counter_id + 1

            # Get graph details from configuration file
            g['graph_type'] = v['type']
            g['graph descriptor'] = v['description']
            g['color'] = v['color']
            graphs.append(g)

        return graphs

    def get_overview(self, role):

        # FIXME: this function looks like it can be improved
        length_check = 0
        graphs_2d_list = []
        graphs_1d_list = []
        counter = 0

        overview = self.add_graph_fields()

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

    def __init__(self, project_id, p, role):

        self.counter_id = 0
        self.ordered_graphs = df.filter_data_per_project(p, project_id)
        dfpp = dfb.filter_data_per_project(p['resources'], project_id)
        self.ordered_graphs.update(dfpp)

        fp = '/home/grg/git/XNAT-Dashboards/config.json'
        config.DASHBOARD_CONFIG_PATH = fp
        j = json.load(open(fp))
        non_graph = ['Stats', 'test_grid', 'Project details']
        self.graphs = [e for e in list(j['graphs'].keys())
                       if e not in non_graph
                       and role in self.graphs[e]['visibility']]

    def get_project_view(self):

        length_check = 0
        graphs_2d_list = []
        graphs_1d_list = []
        counter = 0

        # Do the required addition using field addition
        graphs_per_project_view = self.add_graph_fields()

        if isinstance(graphs_per_project_view, int) or graphs_per_project_view is None:
            return graphs_per_project_view

        non_graph = ['Stats', 'test_grid', 'Project details']

        # Loop through each graph field and add it into
        # graph 2d array where each row have 2 columns and each
        # columns contains single graph
        for graph in graphs_per_project_view:
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

        graph_stats_data = [graphs_2d_list, project_view['Stats'],
                            project_view['Project details']]

        # Test grid is a specific dashboard for BBRC XNATs
        # not visible to normal xnat instance
        if 'test_grid' in project_view:
            graph_stats_data.append(project_view['test_grid'])
        else:
            graph_stats_data.append([[], [], []])

        return graph_stats_data
