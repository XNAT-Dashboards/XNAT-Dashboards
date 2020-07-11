# Import flask dependencies
from flask import Blueprint, render_template, session, request,\
    redirect, url_for
from generators import graph_generator, graph_generator_DB,\
    graph_generator_pp_DB, graph_generator_pp
from app.init_database import mongo
import pickle


# Define the blueprint: 'dashboards', set its url prefix: app.url/dashboards
dashboards = Blueprint('dashboards', __name__, url_prefix='/dashboards')

pickle_saver = True
graph_data_stats = []
project_lists = []
username = ''
password = ''
server = ''
ssl = ''
db = False


# Set the route and accepted methods
@dashboards.route('/stats/', methods=['POST', 'GET'])
def stats():

    if request.method == "POST":

        global username, server, password, ssl
        user_details = request.form
        username = user_details['username']
        password = user_details['password']
        server = user_details['server']
        ssl = False if user_details.get('ssl') is None else True
        global graph_data_stats
        global project_lists
        global db
        plotting_object = graph_generator.GraphGenerator(username,
                                                         password,
                                                         server,
                                                         ssl)
        graph_data_stats = plotting_object.graph_generator()
        project_lists = plotting_object.project_list_generator()

        # Disconnecting the api session
        del plotting_object

        if graph_data_stats == [] or type(graph_data_stats) == int:
            session['error'] = graph_data_stats
            return redirect(url_for('auth.login'))
        else:
            project_list = project_lists[0]
            project_list_ow_co_me = project_lists[1]
            graph_data = graph_data_stats[0]
            stats_data = graph_data_stats[1]
            return render_template('dashboards/stats_dashboards.html',
                                   graph_data=graph_data,
                                   project_list=project_list,
                                   stats_data=stats_data,
                                   project_list_ow_co_me=project_list_ow_co_me,
                                   username=username.capitalize(),
                                   server=server,
                                   db=db)
    else:
        if graph_data_stats == [] or type(graph_data_stats) == int:
            session['error'] = graph_data_stats
            return redirect(url_for('auth.login'))
        elif db:
            return redirect(url_for('dashboards.stats_db'))
        else:
            project_list = project_lists[0]
            project_list_ow_co_me = project_lists[1]
            graph_data = graph_data_stats[0]
            stats_data = graph_data_stats[1]
            return render_template('dashboards/stats_dashboards.html',
                                   graph_data=graph_data,
                                   project_list=project_list,
                                   stats_data=stats_data,
                                   project_list_ow_co_me=project_list_ow_co_me,
                                   username=username.capitalize(),
                                   server=server,
                                   db=db)


# Logout route
@dashboards.route('/logout/', methods=['GET'])
def logout():

    global graph_data_stats, username, password, ssl
    global server, pickle_saver
    pickle_saver = True
    graph_data_stats = []
    username = ''
    password = ''
    server = ''
    ssl = ''

    if 'username' in session:
        del session['username']
    session['error'] = -1

    global db
    if db:
        db = False
        return redirect(url_for('auth.login_DB'))
    else:
        return redirect(url_for('auth.login'))


@dashboards.route('/db/stats/', methods=['GET', 'POST'])
def stats_db():
    global db
    db = True
    if request.method == 'POST':
        global username, server
        user_details = request.form
        username = user_details['username']
        password = user_details['password']
        save_to_DB = False if request.form.get('DB') is None else True
        global graph_data_stats
        global project_lists

        if not save_to_DB:
            if 'username' in session and graph_data_stats != []:
                session['error'] = "Already logged in"
            else:
                try:
                    with open(
                            'pickles/users/'+username+'.pickle',
                            'rb') as handle:
                        user = pickle.load(handle)
                    if user['password'] == password:
                        try:
                            with open(
                                    'pickles/users_data/'+username+'.pickle',
                                    'rb') as handle:

                                user_data = pickle.load(handle)
                        except Exception:
                            session['error'] = "User Registered: Fetching data"
                        plotting_object = graph_generator_DB.GraphGenerator(
                            username,
                            user_data['info'])
                        graph_data_stats = plotting_object.graph_generator()
                        project_lists = plotting_object.\
                            project_list_generator()
                    else:
                        session['error'] = "Wrong Password"
                except Exception:
                    session['error'] = "Username doesn't exist please register"
        else:
            global pickle_saver
            pickle_saver = False

            users = mongo.db.users
            existing_users = users.find_one(
                {'username': request.form['username']})

            if 'username' in session and graph_data_stats != []:
                session['error'] = "Already logged in"
            elif existing_users is not None:
                if existing_users['password'] == password:

                    users_data_tb = mongo.db.users_data
                    users_data = users_data_tb.find_one({'username': username})

                    if users_data is not None:

                        session['username'] = username
                        plotting_object = graph_generator_DB.GraphGenerator(
                            username,
                            users_data['info'])
                        graph_data_stats = plotting_object.graph_generator()
                        project_lists = plotting_object.\
                            project_list_generator()

                    else:
                        session['error'] = "User Registered: Fetching data"

                else:
                    session['error'] = "Wrong Password"

            else:
                session['error'] = "Username doesn't exist please register"

        if 'error' in session:

            return redirect(url_for('auth.login_DB'))

        else:

            project_list = project_lists[0]
            project_list_ow_co_me = project_lists[1]
            graph_data = graph_data_stats[0]
            stats_data = graph_data_stats[1]
            return render_template('dashboards/stats_dashboards.html',
                                   graph_data=graph_data,
                                   project_list=project_list,
                                   stats_data=stats_data,
                                   project_list_ow_co_me=project_list_ow_co_me,
                                   username=username.capitalize(),
                                   server=server,
                                   db=db)

    else:

        if graph_data_stats == [] or type(graph_data_stats) == int:
            session['error'] = graph_data_stats
            return redirect(url_for('auth.login_DB'))
        else:

            project_list = project_lists[0]
            project_list_ow_co_me = project_lists[1]
            graph_data = graph_data_stats[0]
            stats_data = graph_data_stats[1]
            return render_template('dashboards/stats_dashboards.html',
                                   graph_data=graph_data,
                                   project_list=project_list,
                                   stats_data=stats_data,
                                   project_list_ow_co_me=project_list_ow_co_me,
                                   username=username.capitalize(),
                                   server=server,
                                   db=db)


# this route give the details of the movie
@dashboards.route('db/project/<id>', methods=['GET'])
def project_db(id):

    global username

    if pickle_saver:
        with open('pickles/users_data/'+username+'.pickle', 'rb') as handle:
            users_data = pickle.load(handle)
    else:
        users_data_tb = mongo.db.users_data
        users_data = users_data_tb.find_one({'username': username})

    data_array = graph_generator_pp_DB.GraphGenerator(
        username, users_data['info'], id
    ).graph_generator()

    graph_data = data_array[0]
    stats_data = data_array[1]
    members = data_array[2]['member(s)']
    users = data_array[2]['user(s)']
    collaborators = data_array[2]['Collaborator(s)']
    owners = data_array[2]['Owner(s)']
    last_accessed = data_array[2]['last_accessed(s)']
    insert_users = data_array[2]['insert_user(s)']
    insert_date = data_array[2]['insert_date']
    access = data_array[2]['access']
    name = data_array[2]['name']
    last_workflow = data_array[2]['last_workflow']

    return render_template(
        'dashboards/stats_dashboards_pp.html',
        graph_data=graph_data,
        stats_data=stats_data,
        username=username.capitalize(),
        server=server,
        db=db,
        members=members,
        users=users,
        collaborators=collaborators,
        owners=owners,
        last_accessed=last_accessed,
        insert_date=insert_date,
        insert_users=insert_users,
        access=access,
        name=name,
        last_workflow=last_workflow,
        id=id)


# this route give the details of the movie
@dashboards.route('project/<id>', methods=['GET'])
def project(id):

    global username, password, server, ssl

    data_array = graph_generator_pp.GraphGenerator(
        username, password, server, ssl, id
    ).graph_generator()

    graph_data = data_array[0]
    stats_data = data_array[1]
    members = data_array[2]['member(s)']
    users = data_array[2]['user(s)']
    collaborators = data_array[2]['Collaborator(s)']
    owners = data_array[2]['Owner(s)']
    last_accessed = data_array[2]['last_accessed(s)']
    insert_users = data_array[2]['insert_user(s)']
    insert_date = data_array[2]['insert_date']
    access = data_array[2]['access']
    name = data_array[2]['name']
    last_workflow = data_array[2]['last_workflow']

    return render_template(
        'dashboards/stats_dashboards_pp.html',
        graph_data=graph_data,
        stats_data=stats_data,
        username=username.capitalize(),
        server=server,
        db=db,
        members=members,
        users=users,
        collaborators=collaborators,
        owners=owners,
        last_accessed=last_accessed,
        insert_date=insert_date,
        insert_users=insert_users,
        access=access,
        name=name,
        last_workflow=last_workflow,
        id=id)
