# Import flask dependencies
from flask import Blueprint, render_template, session, redirect, url_for
from dashboards.data import graph as g
from dashboards.data import filter as df
from dashboards.data import bbrc

import pickle
from dashboards import config
import pandas as pd

# Define the blueprint: 'dashboard', set its url prefix: app.url/dashboard
dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard.route('/logout/', methods=['GET'])
def logout():

    session.clear()
    session['error'] = 'Logged out.'
    return redirect(url_for('auth.login'))


@dashboard.route('/overview/', methods=['GET'])
def overview():

    # Load pickle and filter projects
    p = pickle.load(open(config.PICKLE_PATH, 'rb'))
    projects = session['projects']
    p = df.filter_data(p, projects)

    # Collect graphs and select them based on access rights
    graphs = df.get_graphs(p)
    graphs = g.add_graph_fields(graphs)
    graphs = {k: v for k, v in graphs.items() if k in session['graphs']}

    data = {'overview': g.split_by_2(graphs),
            'stats': df.get_stats(p),
            'projects': g.get_projects_by_4(p),
            'username': session['username'],
            'server': session['server']}
    return render_template('dashboards/overview.html', **data)


@dashboard.route('project/<project_id>', methods=['GET'])
def project(project_id):
    # Load pickle and filter one project
    # (Do we check that user is allowed to see it?)
    p = pickle.load(open(config.PICKLE_PATH, 'rb'))
    p = df.filter_data(p, [project_id])
    graphs = df.get_graphs_per_project(p)

    # Filter graphs based on access rights
    graphs = {k: v for k, v in graphs.items() if k in session['graphs']}
    graphs = g.add_graph_fields(graphs)

    # session['excel'] = (tests_list, diff_version)

    stats = df.get_stats(p)
    stats.pop('Projects')

    data = {'project_view': g.split_by_2(graphs),
            'stats': stats,
            'project': df.get_project_details(p),
            'test_grid': bbrc.build_test_grid(p),
            'username': session['username'],
            'server': session['server'],
            'id': project_id}
    return render_template('dashboards/projectview.html', **data)

