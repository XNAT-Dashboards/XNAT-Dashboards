# Import flask dependencies
from flask import Blueprint, render_template, session, redirect, url_for
from dashboards.data import graph as g
from dashboards.data import filter as df
from dashboards.data import bbrc as dfb

import pickle
from dashboards import config

# Define the blueprint: 'dashboard', set its url prefix: app.url/dashboard
dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard.route('/logout/', methods=['GET'])
def logout():

    fields = ['username', 'server', 'projects', 'role']
    for e in fields:
        if e in session:
            del session[e]

    session['error'] = 'Logged out.'
    return redirect(url_for('auth.login'))


@dashboard.route('/overview/', methods=['GET'])
def overview():
    # Load pickle and check server
    p = pickle.load(open(config.PICKLE_PATH, 'rb'))
    if p['server'] != session['server']:
        msg = 'Pickle does not match with current server (%s/%s)'\
              % (p['server'], session['server'])
        raise Exception(msg)

    projects = session['projects']
    df.filter_data(p, projects)
    graphs = df.get_graphs(p)
    stats = df.get_stats(p)

    #resources = [e for e in p['resources'] if len(e) > 4]
    bbrc_filtered = dfb.filter_data(p['resources'], projects)
    graphs.update(bbrc_filtered)

    data = {k: v for k, v in graphs.items() if k in session['graphs']}

    role = session['role']
    graph_fields = g.add_graph_fields(data, role)
    overview = g.split_by_2(graph_fields)

    n = 4  # split projects in chunks of size 4
    projects = [pr['id'] for pr in p['projects'] if pr['id'] in projects
                or "*" in projects]
    projects_by_4 = [projects[i * n:(i + 1) * n]
                     for i in range((len(projects) + n - 1) // n)]

    data = {'overview': overview,
            'stats': stats,
            'projects': projects_by_4,
            'username': session['username'].capitalize(),
            'server': session['server']}
    return render_template('dashboards/overview.html', **data)


def from_df_to_html(test_grid):
    columns = test_grid.columns
    tests_union = list(columns[2:])
    diff_version = list(test_grid.version.unique())

    tests_list = []
    for index, row in test_grid.iterrows():
        row_list = [row['session'], 'version', row['version']]
        for test in tests_union:
            row_list.append(row[test])
        tests_list.append(row_list)

    return [tests_union, tests_list, diff_version]


@dashboard.route('project/<project_id>', methods=['GET'])
def project(project_id):

    # Load pickle and check server
    p = pickle.load(open(config.PICKLE_PATH, 'rb'))
    if p['server'] != session['server']:
        msg = 'Pickle does not match with current server (%s/%s)'\
              % (p['server'], session['server'])
        raise Exception(msg)

    # Get the details for plotting
    df.filter_data(p, [project_id])
    project_details = df.get_projects_details_pp(p, project_id)
    stats = df.get_stats(p)
    stats.pop('Projects')
    data = df.get_graphs_per_project(p)

    resources = [e for e in p['resources'] if len(e) > 4]
    dfpp = dfb.filter_data_per_project(resources, project_id)
    data.update(dfpp)

    role = session['role']

    test_grid = data.get('test_grid')
    html = [], [], []

    if test_grid:
        tests_union, tests_list, diff_version = test_grid
        html = from_df_to_html(tests_union)
        data.pop('test_grid')

    data = {k: v for k, v in data.items() if k in session['graphs']}

    graph_fields_pp = g.add_graph_fields(data, role)
    project_view = g.split_by_2(graph_fields_pp)

    # session['excel'] = (tests_list, diff_version)

    data = {'project_view': project_view,
            'stats': stats,
            'project': project_details,
            'test_grid': html,
            'username': session['username'].capitalize(),
            'server': session['server'],
            'id': project_id}
    return render_template('dashboards/projectview.html', **data)
