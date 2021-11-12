# Import flask dependencies
from flask import Blueprint, render_template, session, request, redirect, url_for
from dashboards import config as cfg
from dashboards import data as dsh
import json
import pyxnat
import pickle

auth = Blueprint('auth', __name__, url_prefix='/auth')


def __get_modules__(m):
    import pkgutil
    import logging as log
    modules = []
    prefix = m.__name__ + '.'
    log.info('prefix : %s' % prefix)
    for importer, modname, ispkg in pkgutil.iter_modules(m.__path__, prefix):
        module = __import__(modname, fromlist='dummy')
        if not ispkg:
            modules.append(module)
        else:
            modules.extend(__get_modules__(module))
    return modules


def __find_all_graphs__(m):
    """Browses module `m` and looks for any class named as a Graph"""
    import inspect
    modules = []
    classes = []
    modules = __get_modules__(m)
    forbidden_classes = []
    for m in modules:
        for name, obj in inspect.getmembers(m):
            if inspect.isclass(obj) and 'Graph' in name \
                    and obj not in forbidden_classes:
                classes.append(obj)
    return classes


@auth.route('/login/', methods=['GET', 'POST'])
def login():

    p = pickle.load(open(cfg.PICKLE_PATH, 'rb'))

    if request.method == 'GET':
        kwargs = {}
        if 'error' in session:
            kwargs['error'] = session.pop('error')
        return render_template('authentication/login.html', **kwargs)

    elif request.method == 'POST':
        username = request.form['username']
        x = pyxnat.Interface(user=username,
                             password=request.form['password'],
                             server=p['server'],
                             verify=p['verify'])
        has_access = x.head('').ok

        if has_access:

            config = json.load(open(cfg.DASHBOARD_CONFIG_PATH))
            roles = config['roles']

            if username in roles['forbidden']['users']:
                session['error'] = 'Access denied.'
                return redirect(url_for('auth.login'))

            user_roles = [r for r in roles.keys()
                          if username in roles[r]['users']]
            if len(user_roles) > 1:
                raise Exception('%s has multiple roles' % str(username))
            elif len(user_roles) == 0:
                role = 'guest'  # no role found, guest by default
            else:
                role = user_roles[0]

            # Collect graphs and select them based on access rights
            graphs = [graph() for graph in __find_all_graphs__(dsh)]

            # Add data to session
            session['username'] = username
            session['server'] = p['server']
            session['role'] = role
            session['graphs'] = [g.name for g in graphs if role in g.visibility]
            session['projects'] = roles[role]['projects']

            # Redirect to dashboard
            return redirect(url_for('dashboard.overview'))

        else:
            session['error'] = 'Wrong password/username.'
            return redirect(url_for('auth.login'))
