# Import flask dependencies
from flask import Blueprint, request, redirect,\
                  render_template, session, url_for

# Define the blueprint: 'auth', set its url prefix: app.url/auth
auth = Blueprint('auth', __name__, url_prefix='/auth')


# Set the route and accepted methods
@auth.route('/login/')
def login():
    return render_template('auth/login.html')
