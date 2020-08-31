# Import flask dependencies
from flask import Blueprint, render_template, session, request, redirect,\
    url_for
from xnat_dashboards.app.authentication import model


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

    servers_list = model.login_urls()

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
                error=display_error,
                servers_list=servers_list)
        else:
            # If there is no error meaning the user is called login
            # page using browser instead of a redirect
            return render_template(
                'authentication/login.html', servers_list=servers_list)

    else:

        # Fetch details from form

        user_details = request.form

        username = user_details['username']
        password = user_details['password']
        server_name = user_details['server']

        for server in servers_list:

            if server_name == server['name']:

                server_url = server['url']
                ssl = server['verify']

                break

        # Check from API whether user exist in the XNAT instance
        exists = model.user_exists(username, password, server_url, ssl)

        if type(exists) == int:
            # If exist check whether the XNAT instance is same
            config = model.user_role_config(username)

            # If same xnat instance check role assign to user
            if config:
                # If no role assigned to a user then guest is set
                # as default role
                if username in config['user roles']:
                    session['role_exist'] = config['user roles'][username]
                else:
                    session['role_exist'] = 'guest'

                # Add data to session
                session['username'] = username
                session['server'] = server_url
                session['project_visible'] = config['project_visible']

                # Redirect to dashboard
                return redirect(url_for('dashboard.stats'))
            else:

                # User is forbiden to login
                session['error'] = "User role assigned is "
                "forbidden login not allowed"
                return redirect(url_for('auth.login'))
        else:

            # Wrong password or username
            session['error'] = "Wrong Password or Username"
            return redirect(url_for('auth.login'))
