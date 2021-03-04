# Import flask dependencies
from flask import Blueprint, render_template, session, request, redirect,\
    url_for
from dashboards import config as cfg
import json


# Define the blueprint: 'auth', set its url prefix: app.url/auth
auth = Blueprint('auth', __name__, url_prefix='/auth')


# Set the route and accepted methods
@auth.route('/login/', methods=['GET', 'POST'])
def login():

    """
    This is the login route. Uses authentication model for checking
    the user details.

    User Exist function checks whether user exist on the XNAT instance.
    If user exist we proceed further.
    Then this checks user roles whether user role is assigned, If user
    roles isn't assigned we set it as guest.

    Returns:
        route: It routes to dashboard if user details are correct
        else reloads the page

    """

    import pickle
    p = pickle.load(open(cfg.PICKLE_PATH, 'rb'))

    if request.method == 'GET':

        # Checks if there is a error key in session
        if 'error' in session:

            if session['error'] == -1:
                display_error = "Logged out"
                del session['error']
            else:
                display_error = session['error']
                del session['error']
            return render_template(
                'authentication/login.html',
                error=display_error)
        else:
            # If there is no error meaning the user is called login
            # page using browser instead of a redirect
            return render_template(
                'authentication/login.html')

    else:

        form = request.form
        username = form['username']
        # Check from API whether user exist in the XNAT instance
        import pyxnat
        x = pyxnat.Interface(user=username,
                             password=form['password'],
                             server=p['server'],
                             verify=p['verify'])
        exists = len(x.select.projects().get()) != 0

        if exists:
            # If exist check whether the XNAT instance is same
            config = json.load(open(cfg.DASHBOARD_CONFIG_PATH))
            roles = config['roles']

            if username in roles['forbidden']['users']:
                # User is forbiden
                session['error'] = 'User role assigned is '\
                                   'forbidden login not allowed'
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
            session['project_visible'] = roles[role]['projects']

            # Redirect to dashboard
            return redirect(url_for('dashboard.stats'))

        else:
            # Wrong password or username
            session['error'] = 'Wrong Password or Username'
            return redirect(url_for('auth.login'))
