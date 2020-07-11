# Import flask dependencies
from flask import Blueprint, redirect, request, jsonify,\
    render_template, session, url_for
import os
from app.init_database import mongo
from pyxnat_db import save_to_db, save_to_pickle
import threading

# Define the blueprint: 'auth', set its url prefix: app.url/auth
auth = Blueprint('auth', __name__, url_prefix='/auth')

pickle_saver = True
saved_flag = -1         # Check whether the saving is done correctly
delete_username = None  # Flag whether to delete username registered
# If there is error in fetching


# Set the route and accepted methods
@auth.route('/login/')
def login():

    global saved_flag

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
                               error=display_error, saved_flag=saved_flag)
    else:
        return render_template('auth/login.html', saved_flag=saved_flag)


# Set the route and accepted methods
@auth.route('db/register/', methods=['POST', 'GET'])
def register_DB():
    global saved_flag

    if request.method == 'GET':

        return render_template('auth/register_DB.html', saved_flag=saved_flag)
    else:

        if pickle_saver:
            exists = os.path.exists(
                'pickles/users/'+request.form['username']+'.pickle')

            existing_users = None if exists is False else True
        else:
            users = mongo.db.users
            existing_users = users.find_one(
                {'username': request.form['username']})

        # Checking if user exists in DB
        if existing_users is None:

            username = request.form['username']
            password = request.form['password']
            server = request.form['server']
            ssl = False if request.form.get('ssl') is None else True
            db = False if request.form.get('DB') is None else True

            thread = threading.Thread(
                target=save_data,
                args=(username, password, server, db, ssl))

            # Start a thread for saving the data on database from pyxnat_api
            thread.start()
            # Set save flag to 200 meaning the data is currently saving on
            # another thread
            saved_flag = 200

            # A alert to user to wait at login page, If something wrong in the
            # submitted details a error will occur within 10 seconds and user
            # will be redirected
            session['error'] = 'wait'
        else:
            # Alert to user that username already exist on login page
            session['error'] = "userexist"

        return redirect(url_for('auth.login_DB'))


# Run on the thread created during registration of user
def save_data(username, password, server, ssl, db, test=False):

    if db:
        pk = save_to_pickle.SaveToPk(username, password, server, ssl)
        pk.save_user(username, password, server, ssl)
        save_flag = pk.save_data()
    else:
        db = save_to_db.SaveToDb(username, password, server, ssl, test)
        db.save_user(username, password, server, ssl)
        save_flag = db.save_data()

    # If everything went correct then it will take more time to save data
    # If some problem arises then user need to save flag status from 0
    # will be changed as per response from the save_to_db
    global saved_flag

    if save_flag != 0:
        global delete_username
        delete_username = username
        if save_flag == 500:
            saved_flag = 500    # URI error
        elif save_flag == 401:
            saved_flag = 401    # Password or username error
        elif save_flag == 1:
            saved_flag = 1      # Wrong URL
        elif save_flag == 191912:
            saved_flag = 191912     # SSL error
        elif save_flag == 1000:
            saved_flag = 1000       # Database error
        else:
            saved_flag = 300     # Unknown error

    else:
        saved_flag = 0


@auth.route('db/status')
def status():

    # This is a route which is called asynch to check the
    # Status of the data saving step
    # This route is called every one second to check status
    # of the saving process

    global saved_flag

    if saved_flag == 200:
        return jsonify(dict(status=('saving')))
        # Returs that data is being saved
    elif saved_flag == 500:
        session['error'] = 'URI Error'
    elif saved_flag == 401:
        session['error'] = 'Username and password Error'
    elif saved_flag == 1:
        session['error'] = 'Wrong URL'
    elif saved_flag == 191912:
        session['error'] = 'SSL Error'
    else:
        session['error'] = 'saved'

    saved_flag = -1

    # If some problem occurs then session variable is assigned
    # with the appropriate error message and redirected again to
    # login page with error or if no error occur no redirection takes place
    return jsonify(dict(status=('completed')))


# Set the route and accepted methods
@auth.route('db/login/')
def login_DB():
    global saved_flag

    # Checks if there is a error key in session
    if 'error' in session:
        # If there is a error key means 4 cases
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
        # Case 4: Error has occured from saved data
        else:
            # Since error occured in saved data during fetching of info
            # We have already saved user details thus we need to delete
            # user details from users collections

            display_error = session['error']
            del session['error']
            global delete_username
            if delete_username is not None:
                users = mongo.db.users
                users.delete_one({'username': delete_username})
                delete_username = None

        return render_template('auth/login_DB.html',
                               error=display_error,
                               saved_flag=saved_flag)
    else:
        # If there is no error meaning the user is called login
        # page using browser instead of a redirect

        return render_template('auth/login_DB.html',
                               saved_flag=saved_flag)
