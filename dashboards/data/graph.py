from dashboards import config


def add_graph_fields(graphs):
    fp = config.DASHBOARD_CONFIG_PATH
    if not fp:
        import os.path as op
        import dashboards
        fp = op.join(op.dirname(op.dirname(dashboards.__file__)), 'config.json')
    import json
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


def split_by_2(graphs):

    n = 2  # split projects in chunks of size 2
    items = list(graphs.items())
    graphs_by_2 = [[dict([e]) for e in items[i * n:(i + 1) * n]]
                   for i in range((len(items) + n - 1) // n)]
    return graphs_by_2


def get_projects_by_4(p):
    """ The frontend displays a list of projects in 4 columns. This function
    splits the list of the projects visible by the user in chunks of size 4
    and returns it."""
    
    # Split the list of visible projects by chunks of size 4
    projects = [e['id'] for e in p['projects']]
    n = 4  # split projects in chunks of size 4
    projects_by_4 = [projects[i * n:(i + 1) * n]
                     for i in range((len(projects) + n - 1) // n)]
    return projects_by_4
