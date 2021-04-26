# Import flask dependencies
from flask import Blueprint, render_template, session, request, redirect, url_for
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
            error = session.pop('error')
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

            # Add data to session
            session['username'] = username
            session['server'] = p['server']
            session['role'] = role
            session['graphs'] = [k for k, v in config['graphs'].items()
                                 if role in v['visibility']]
            session['projects'] = roles[role]['projects']

            # Redirect to dashboard
            return redirect(url_for('dashboard.overview'))

        else:
            session['error'] = 'Wrong password/username.'
            return redirect(url_for('auth.login'))
