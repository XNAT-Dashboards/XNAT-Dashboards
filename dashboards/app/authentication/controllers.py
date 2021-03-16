# Import flask dependencies
from flask import Blueprint, render_template, session, request, redirect,\
    url_for
from dashboards import config as cfg
import json
import pyxnat
import pickle

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/login/', methods=['GET', 'POST'])
def login():

    p = pickle.load(open(cfg.PICKLE_PATH, 'rb'))

    # Form submission triggers POST request while other cases yield GET
    method = request.method
    if method == 'GET':
        # First visit / logging out / login errors
        if 'error' in session:
            error = session['error']
            del session['error']
            return render_template('authentication/login.html',
                                   error=error)
        else:
            return render_template('authentication/login.html')

    elif method == 'POST':
        form = request.form
        username = form['username']
        x = pyxnat.Interface(user=username,
                             password=form['password'],
                             server=p['server'],
                             verify=p['verify'])
        can_see_some_projects = len(x.select.projects().get()) != 0

        if can_see_some_projects:

            config = json.load(open(cfg.DASHBOARD_CONFIG_PATH))
            roles = config['roles']

            if username in roles['forbidden']['users']:
                msg = 'User role assigned is forbidden login not allowed'
                session['error'] = msg
                return redirect(url_for('auth.login'))

            role = []
            for each in list(roles.keys()):
                if username in roles[each]['users']:
                    role.append(each)
            if len(role) != 1:
                raise Exception('%s exists in multiple roles' % str(role))
            elif len(role) == 0:
                role = 'guest'  # no role found, guest by default
            else:
                role = role[0]

            # Add data to session
            session['username'] = username
            session['server'] = p['server']
            session['role'] = role
            session['projects'] = roles[role]['projects']

            # Redirect to dashboard
            return redirect(url_for('dashboard.overview'))

        else:
            session['error'] = 'Wrong password/username'
            return redirect(url_for('auth.login'))
