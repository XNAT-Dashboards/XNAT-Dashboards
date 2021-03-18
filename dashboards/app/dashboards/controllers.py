# Import flask dependencies
from flask import Blueprint, render_template, session, redirect, url_for
from dashboards.data import graph as gg
from dashboards.data import filter as df
from dashboards.data import bbrc as dfb

import pickle
from dashboards import config
import pandas as pd

# Define the blueprint: 'dashboard', set its url prefix: app.url/dashboard
dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')


# logout route
@dashboard.route('/logout/', methods=['GET'])
def logout():
    """logout route here we delete all existing session variables

    Returns:
        route: Redirect to login page.
    """
    # Delete session keys if exist
    fields = ['username', 'server', 'projects', 'role']
    for e in fields:
        if e in session:
            del session[e]
    session['error'] = -1

    return redirect(url_for('auth.login'))


@dashboard.route('/overview/', methods=['GET'])
def overview():
    # Load pickle and check server
    p = pickle.load(open(config.PICKLE_PATH, 'rb'))
    if p['server'] != session['server']:
        msg = 'Pickle does not match with current server (%s/%s)'\
              % (p['server'], session['server'])
        raise Exception(msg)

    role = session['role']
    projects = session['projects']
    filtered = df.DataFilter(p, projects)
    bbrc_filtered = dfb.BBRCDataFilter(p['resources'], projects)
    plot = gg.GraphGenerator(filtered, bbrc_filtered, p)

    overview = plot.get_overview(role)

    n = 4 # split projects in chunks of size 4
    projects = [e['id'] for e in filtered.data['projects']]
    projects_by_4 = [projects[i * n:(i + 1) * n]
                     for i in range((len(projects) + n - 1) // n )]

    return render_template('dashboards/stats_dashboards.html',
                           graph_data=overview[0],
                           stats_data=overview[1],
                           project_list=projects_by_4,
                           username=session['username'].capitalize(),
                           server=session['server'])

def convert_from_df_to_html(test_grid):
    columns = test_grid.columns
    tests_union = list(columns[2:])
    diff_version = list(test_grid.version.unique())
    tests_list = []
    for index, row in test_grid.iterrows():
        row_list = []
        row_list.append(row['session'])
        row_list.append(['version', row['version']])
        for test in tests_union:
            row_list.append(row[test])
        tests_list.append(row_list)

    return [tests_union, tests_list, diff_version]


# this route give the details of the project
@dashboard.route('project/<id>', methods=['GET'])
def project(id):
    """This is the per project dashboard view.

    Args:
        id (str): Id of the project we like to view.

    Returns:
        route: Project details
    """

    # Load pickle and check server
    p = pickle.load(open(config.PICKLE_PATH, 'rb'))
    if p['server'] != session['server']:
        msg = 'Pickle does not match with current server (%s/%s)'\
              % (p['server'], session['server'])
        raise Exception(msg)

    # Get the details for plotting

    ggpp = gg.GraphGeneratorPP(id, session['role'], p, session['projects'])
    graph_data, stats_data, data_array, test_grid = ggpp.get_project_view()
    per_project_view = [graph_data, stats_data, data_array, test_grid]

    test_grid_html = convert_from_df_to_html(test_grid[0])
    # If no data found redirect to login page else render the data
    # with template
    if per_project_view is None:
        return render_template('dashboards/stats_dashboards.html')

    return render_template(
        'dashboards/stats_dashboards_pp.html',
        graph_data=graph_data,
        stats_data=stats_data,
        username=session['username'].capitalize(),
        server=session['server'],
        data_array=data_array,
        test_grid=test_grid_html,
        id=id)
