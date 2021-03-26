# Import flask dependencies
from flask import Blueprint, render_template, session, redirect, url_for
from dashboards.data import graph as g
from dashboards.data import filter as df
from dashboards.data import bbrc

import pickle
from dashboards import config

# Define the blueprint: 'dashboard', set its url prefix: app.url/dashboard
dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard.route('/logout/', methods=['GET'])
def logout():

    session.clear()
    session['error'] = 'Logged out.'
    return redirect(url_for('auth.login'))


@dashboard.route('/overview/', methods=['GET'])
def overview():

    # Load pickle and check server
    p = pickle.load(open(config.PICKLE_PATH, 'rb'))

    projects = session['projects']
    p = df.filter_data(p, projects)
    graphs = df.get_graphs(p)
    stats = df.get_stats(p)

    # Select graphs based on access rights
    user_graphs = {k: v for k, v in graphs.items() if k in session['graphs']}

    role = session['role']
    graph_fields = g.add_graph_fields(user_graphs, role)
    overview_data = g.split_by_2(graph_fields)

    n = 4  # split projects in chunks of size 4
    projects = [pr['id'] for pr in p['projects']
                if pr['id'] in projects or "*" in projects]
    projects_by_4 = [projects[i * n:(i + 1) * n]
                     for i in range((len(projects) + n - 1) // n)]

    data = {'overview': overview_data,
            'stats': stats,
            'projects': projects_by_4,
            'username': session['username'],
            'server': session['server']}
    return render_template('dashboards/overview.html', **data)


@dashboard.route('project/<project_id>', methods=['GET'])
def project(project_id):

    # Load pickle and check server
    p = pickle.load(open(config.PICKLE_PATH, 'rb'))

    # Get the details for plotting
    p = df.filter_data(p, [project_id])
    project_details = df.get_project_details(p, project_id)
    stats = df.get_stats(p)
    stats.pop('Projects')
    graphs = df.get_graphs_per_project(p)

    bbrc_resources = [e for e in p['resources'] if len(e) > 4]
    graphs.update(bbrc.get_resource_details(bbrc_resources, project_id))
    project, exp_id, archiving_validator, bv, insert_date = bbrc_resources[0]
    if archiving_validator != 0:
        test_grid = bbrc.generate_test_grid_bbrc(bbrc_resources)
    else:
        test_grid = [], [], []

    dd = bbrc.diff_dates(bbrc_resources, project_id)
    graphs['Dates difference (Acquisition date - Insertion date)'] = dd

    user_graphs = {k: v for k, v in graphs.items() if k in session['graphs']}

    graph_fields_pp = g.add_graph_fields(user_graphs, session['role'])
    project_view = g.split_by_2(graph_fields_pp)

    # session['excel'] = (tests_list, diff_version)

    data = {'project_view': project_view,
            'stats': stats,
            'project': project_details,
            'test_grid': test_grid,
            'username': session['username'],
            'server': session['server'],
            'id': project_id}
    return render_template('dashboards/projectview.html', **data)
