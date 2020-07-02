# Import flask dependencies
from flask import Blueprint, request, redirect,\
                  render_template, session, url_for

# Define the blueprint: 'auth', set its url prefix: app.url/auth
auth = Blueprint('auth', __name__, url_prefix='/auth')


# Set the route and accepted methods
@auth.route('/login/')
def login():

    if('error' in session):
        print('yes')
        if(session['error'] == 500):
            display_error = "Wrong XNAT URI"
        elif(session['error'] == 401):
            display_error = "Wrong Username or Password"
        elif(session['error'] == 1):
            display_error = "Wrong URL"
        elif(session['error'] == 191912):
            display_error = "SSL Error"
        elif(session['error'] == -1):
            display_error = "Logged out"
        else:
            display_error = "No Session Available"
        del session['error']
        return render_template('auth/login.html',
                               error=display_error)
    else:
        return render_template('auth/login.html')
