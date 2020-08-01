# Import flask dependencies
from flask import Blueprint, render_template, session

# Define the blueprint: 'auth', set its url prefix: app.url/auth
auth = Blueprint('auth', __name__, url_prefix='/auth')

pickle_saver = True


# Set the route and accepted methods
@auth.route('/db/login/')
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
        else:
            display_error = session['error']
            del session['error']
        return render_template('auth/login_DB.html',
                               error=display_error)
    else:
        # If there is no error meaning the user is called login
        # page using browser instead of a redirect
        print("H")
        return render_template('auth/login_DB.html')
