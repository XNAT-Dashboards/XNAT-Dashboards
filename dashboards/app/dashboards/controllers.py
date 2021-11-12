from flask import Blueprint, render_template, session, redirect, url_for
from dashboards.data import graph as g
from dashboards.data import filter as df
from dashboards.data import bbrc
import dashboards.pickle
import pickle
import dashboards
from dashboards import config

db = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@db.route('/logout/', methods=['GET'])
def logout():
    session.clear()
    session['error'] = 'Logged out.'
    return redirect(url_for('auth.login'))


@db.route('/overview/', methods=['GET'])
def overview():
    # Load pickle and filter projects
    p = pickle.load(open(config.PICKLE_PATH, 'rb'))
    projects = session['projects']
    p = df.filter_data(p, projects)

    graphs = [g.ProjectGraph, g.SubjectGraph, g.PerProjectSessionGraph,
              g.SessionGraph, g.SessionsPerSubjectGraph, g.ScanQualityGraph,
              g.ResourcePerTypeGraph, g.ResourcesPerSessionGraph,
              g.UsableT1SessionGraph, g.ResourcesOverTimeGraph,
              g.ValidatorGraph,
              g.ConsistentAcquisitionDateGraph]

    # Collect graphs and select them based on access rights
    graphs = [v() for v in graphs]
    graphs = [e for e in graphs if e.name in session['graphs']]
    graphs = [e.get_chart(i, p) for i, e in enumerate(graphs)]

    data = {'graphs': graphs,
            'stats': dashboards.pickle.get_stats(p),
            'projects': dashboards.pickle.get_projects_by_4(p),
            'username': session['username'],
            'server': session['server']}
    return render_template('dashboards/overview.html', **data)


@db.route('project/<project_id>', methods=['GET'])
def project(project_id):
    # # Load pickle and filter one project
    # # (Do we check that user is allowed to see it?)
    p = pickle.load(open(config.PICKLE_PATH, 'rb'))
    p = df.filter_data(p, [project_id])

    all_graphs = [g.SessionsPerSubjectGraph, g.ScanQualityGraph,
              g.ScanTypeGraph, g.ScansPerSessionGraph,
              g.UsableT1SessionGraph, g.VersionGraph,
              g.ValidatorGraph, g.ConsistentAcquisitionDateGraph,
              g.DateDifferenceGraph]
    all_graphs = [v() for v in all_graphs]
    graphs = []
    for i, e in enumerate(all_graphs):
        if e.name in session['graphs']:
            try:
                graphs.append(e.get_chart(i, p))
            except KeyError:
                print('Skipping ' + e.name)

    # session['excel'] = (tests_list, diff_version)
    stats = dashboards.pickle.get_stats(p)
    stats.pop('Projects')

    data = {'graphs': graphs,
            'stats': stats,
            'project': dashboards.pickle.get_project_details(p),
            'grid': bbrc.build_test_grid(p),
            'username': session['username'],
            'server': session['server'],
            'id': project_id}
    return render_template('dashboards/project.html', **data)


@db.route('/wiki/', methods=['GET'])
def wiki():
    # Load pickle and filter projects
    p = pickle.load(open(config.PICKLE_PATH, 'rb'))
    projects = session['projects']
    p = df.filter_data(p, projects)
    data = {'username': session['username'],
            'projects': dashboards.pickle.get_projects_by_4(p),

            'server': session['server']}
    return render_template('dashboards/wiki.html', **data)
