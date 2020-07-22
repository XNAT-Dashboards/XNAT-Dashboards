# Import flask dependencies
from flask import Blueprint, render_template, session

# Define the blueprint: 'auth', set its url prefix: app.url/auth
auth = Blueprint('auth', __name__, url_prefix='/auth')

pickle_saver = True


# Set the route and accepted methods
@auth.route('/login/')
def login():

    if 'error' in session:

        if session['error'] == 500:
            display_error = "Wrong XNAT URI"
        elif session['error'] == 401:
            display_error = "Wrong Username or Password"
        elif session['error'] == 1:
            display_error = "Wrong URL"
        elif session['error'] == 191912:
            display_error = "SSL Error"
        elif session['error'] == -1:
            display_error = "Logged out"
        else:
            display_error = "No Session Available"
        del session['error']
        return render_template('auth/login.html',
                               error=display_error)
    else:
        return render_template('auth/login.html')


# Set the route and accepted methods
@auth.route('db/login/')
def login_DB():

    # Checks if there is a error key in session
    if 'error' in session:
        # If there is a error key means 3 cases
        # Case 1: User logged out
        if session['error'] == -1:
            display_error = "Logged out"
            del session['error']
        # Case 2: User already exist
        elif session['error'] == 'userexist':
            display_error = "Username already exist"
            del session['error']
        # Case 3: Waiting for saving thread
        elif session['error'] == 'wait':
            display_error = "Please wait for 10 seconds Checking....."
            del session['error']
        elif session['error'] == 'saved':
            display_error = "Saved user details"
            del session['error']

        return render_template('auth/login_DB.html',
                               error=display_error)
    else:
        # If there is no error meaning the user is called login
        # page using browser instead of a redirect

        return render_template('auth/login_DB.html')
