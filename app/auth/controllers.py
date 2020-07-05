# Import flask dependencies
from flask import Blueprint, redirect, request,\
                  render_template, session, url_for
from app.init_database import mongo
from pyxnat_db import save_to_db
import threading
# Define the blueprint: 'auth', set its url prefix: app.url/auth
auth = Blueprint('auth', __name__, url_prefix='/auth')


# Set the route and accepted methods
@auth.route('/login/')
def login():

    if 'error' in session:

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


# Set the route and accepted methods
@auth.route('db/register/', methods=['POST', 'GET'])
def register_DB():

    if request.method == 'GET':

        return render_template('auth/register_DB.html')
    else:

        users = mongo.db.users
        existing_users = users.find_one({'username': request.form['username']})
        if existing_users is None:
            username = request.form['username']
            password = request.form['password']
            server = request.form['server']
            ssl = False if request.form.get('ssl') is None else True
            thread = threading.Thread(target=save_data,
                                      args=(username, password, server, ssl))
            thread.start()
        else:
            session['error'] = "Username already exists"
        return redirect(url_for('auth.login_DB'))


def save_data(username, password, server, ssl):
    users = mongo.db.users
    users.insert({'username': username,
                  'password': password,
                  'server': server,
                  'ssl': ssl})
    db = save_to_db.SaveToDb(username, password, server, ssl)
    db.save()


# Set the route and accepted methods
@auth.route('db/login/')
def login_DB():
    if 'error' in session:
        display_error = session['error']
        del session['error']
        print(display_error)
        return render_template('auth/login_DB.html', error=display_error)
    else:
        return render_template('auth/login_DB.html')
