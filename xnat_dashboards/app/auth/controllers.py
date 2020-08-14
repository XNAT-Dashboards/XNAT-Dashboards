# Import flask dependencies
from flask import Blueprint, render_template, session, request, redirect,\
    url_for
from xnat_dashboards.app.auth import model

# Define the blueprint: 'auth', set its url prefix: app.url/auth
auth = Blueprint('auth', __name__, url_prefix='/auth')

pickle_saver = True


# Set the route and accepted methods
@auth.route('/db/login/', methods=['GET', 'POST'])
def login_DB():

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
                'auth/login_DB.html',
                error=display_error)
        else:
            # If there is no error meaning the user is called login
            # page using browser instead of a redirect
            return render_template('auth/login_DB.html')

    else:

        # Fetch details from form

        user_details = request.form

        username = user_details['username']
        password = user_details['password']
        server = user_details['server']
        ssl = False if user_details.get('ssl') is None else True

        # Check from API whether user exist in the XNAT instance
        exists = model.user_exists(username, password, server, ssl)

        if type(exists) == int:
            # If exist check whether the XNAT instance is same
            config = model.user_role_config(username)

            # If same xnat instance check role assign to user
            if config:
                # If no role assign to user assigne guest as default role
                if username in config['user roles']:
                    session['role_exist'] = config['user roles'][username]
                else:
                    session['role_exist'] = 'guest'

                # Add data to session
                session['username'] = username
                session['server'] = server
                session['project_visible'] = config['project_visible']

                # Redirect to dashboard
                return redirect(url_for('dashboards.stats_db'))
            else:

                # Wrong Xnat instance pickle data found
                session['error'] = "Wrong Server details"
                return redirect(url_for('auth.login_DB'))
        else:

            # Wrong password or username
            session['error'] = "Wrong Password or Username"
            return redirect(url_for('auth.login_DB'))
