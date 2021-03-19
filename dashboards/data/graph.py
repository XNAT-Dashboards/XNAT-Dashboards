import json
from dashboards import config


class GraphGenerator:

    def __init__(self):
        self.counter_id = 0

    def add_graph_fields(self, graphs, role):
        fp = config.DASHBOARD_CONFIG_PATH
        if fp == '':
            fp = '/home/grg/git/XNAT-Dashboards/config.json'
        j = json.load(open(fp))
        cfg = j['graphs']

        for i, graph in enumerate(list(graphs.keys())):
            cg = cfg[graph]

            graphs[graph]['id'] = i

            # get details from configuration file
            graphs[graph]['graph_type'] = cg['type']
            graphs[graph]['graph descriptor'] = cg['description']
            graphs[graph]['color'] = cg['color']

        return graphs

    def get_overview(self, graphs):

        # FIXME: this function looks like it can be improved
        length_check = 0
        graphs_2d_list = []
        graphs_1d_list = []
        counter = 0

        for graph in list(graphs.keys()):
            graphs_1d_list.append({graph: graphs[graph]})
            counter = counter + 1

            # Check if we have filled 2 columns or are at the end
            # of the graphs list
            if counter == 2 or length_check == len(graphs) - 1:
                counter = 0
                graphs_2d_list.append(graphs_1d_list)
                graphs_1d_list = []

            length_check = length_check + 1

        return graphs_2d_list


class GraphGeneratorPP(GraphGenerator):

    def __init__(self):
        self.counter_id = 0

    def get_project_view(self, graphs):

        length_check = 0
        graphs_2d_list = []
        graphs_1d_list = []
        counter = 0

        for graph in list(graphs.keys()):

            graphs_1d_list.append({graph: graphs[graph]})
            counter = counter + 1

            # Check if we have filled 2 columns or are at the end
            # of the graphs list
            if counter == 2 or length_check == len(graphs) - 1:
                counter = 0
                graphs_2d_list.append(graphs_1d_list)
                graphs_1d_list = []

            length_check = length_check + 1

        return graphs_2d_list
