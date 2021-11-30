from flask import Blueprint, render_template, session, request, redirect, url_for
from functools import wraps
from dashboards import graph as g
from dashboards import filter as df
from dashboards import bbrc
import dashboards.pickle
import pickle
import dashboards
from dashboards import config

app = Blueprint('dashboards', __name__, url_prefix='/')


@app.route('/logout/', methods=['GET'])
def logout():
    session.clear()
    session['error'] = 'Logged out.'
    return redirect(url_for('dashboards.login'))


@app.route('/overview/', methods=['GET'])
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
            'role': session['role'],
            'server': session['server']}
    return render_template('overview.html', **data)


@app.route('project/<project_id>', methods=['GET'])
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
            'role': session['role'],
            'id': project_id}
    return render_template('project.html', **data)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('username') is None:
            return redirect('/login', code=302)
        return f(*args, **kwargs)
    return decorated_function


@app.route('/protected/<path:filename>')
@login_required
def protected(filename):
    import os.path as op
    from flask import send_from_directory
    wd = op.join(op.dirname(dashboards.__file__), 'app', 'protected')
    return send_from_directory(wd, filename)


@app.route('/wiki/', methods=['GET'])
def wiki():
    # Load pickle and filter projects
    p = pickle.load(open(config.PICKLE_PATH, 'rb'))
    projects = session['projects']
    p = df.filter_data(p, projects)

    items = [e() for e in g.__find_all_commands__(dashboards, pattern='Card')]

    card_deco = '<div class="card wiki"><a name="{name}"></a>{img}<div class="card-body">'\
                '<h2 class="card-title">{title}</h2>{desc}<br>{links}</div></div>'

    items = [e.to_dict() for e in items]
    items = {e['title']: e for e in items}
    titles = sorted([k for k, v in items.items()])
    items = [items[e] for e in titles]

    cards = [card_deco.format(**e) for e in items]
    toc = ' - '.join(['<a href="#%s">%s</a>' % (e['name'], e['title']) for e in items])

    wiki = '<div class="row"> %s </div>' % ' '.join(cards)

    data = {'username': session['username'],
            'role': session['role'],
            'projects': dashboards.pickle.get_projects_by_4(p),
            'wiki': wiki,
            'toc': toc,
            'server': session['server']}
    return render_template('wiki.html', **data)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    p = pickle.load(open(config.PICKLE_PATH, 'rb'))

    if request.method == 'GET':
        kwargs = {}
        if 'error' in session:
            kwargs['error'] = session.pop('error')
        return render_template('login.html', **kwargs)

    elif request.method == 'POST':
        username = request.form['username']
        import pyxnat
        x = pyxnat.Interface(user=username,
                             password=request.form['password'],
                             server=p['server'],
                             verify=p['verify'])
        has_access = x.head('').ok

        if has_access:
            import json
            cfg = json.load(open(config.DASHBOARD_CONFIG_PATH))
            roles = cfg['roles']

            if username in roles['forbidden']['users']:
                session['error'] = 'Access denied.'
                return redirect(url_for('dashboards.login'))

            user_roles = [r for r in roles.keys()
                          if username in roles[r]['users']]
            if len(user_roles) > 1:
                raise Exception('%s has multiple roles' % str(username))
            elif len(user_roles) == 0:
                role = 'guest'  # no role found, guest by default
            else:
                role = user_roles[0]

            commands = g.__find_all_commands__(dashboards)
            commands = {e.__name__.split('.')[-1].lower()[:-5]: e for e in commands}

            # Collect graphs and select them based on access rights
            graphs = [v() for e, v in commands.items()]

            # Add data to session
            session['username'] = username
            session['server'] = p['server']
            session['role'] = role
            session['graphs'] = [g.name for g in graphs if role in g.visibility]
            session['projects'] = roles[role]['projects']

            # Redirect to dashboard
            return redirect(url_for('dashboards.overview'))

        else:
            session['error'] = 'Wrong password/username.'
            return redirect(url_for('dashboards.login'))
