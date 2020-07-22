# Import flask dependencies
from flask import Blueprint, render_template, session, request,\
    redirect, url_for
from saved_data_processing import graph_generator_DB, graph_generator_pp_DB
from realtime_data_processing import graph_generator_pp, graph_generator
from app.init_database import mongo
from app.dashboards import model


# Define the blueprint: 'dashboards', set its url prefix: app.url/dashboards
dashboards = Blueprint('dashboards', __name__, url_prefix='/dashboards')

pickle_saver = True  # Initially True as pickle saving is default
graph_data_stats = []  # Contains graph Data loaded globally for get request
project_lists = []  # Contains project list globally for get request
username = ''  # For saving username globally
password = ''  # For saving password globally
server = ''  # For saving server url globally
ssl = ''  # For saving username globally
role_exist = ''
db = False  # For specifying that connected to DB or pickle


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
            descriptor = model.graph_descriptor()  # Graph Descriptor
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
                                   db=db,
                                   descriptor=descriptor)
    else:
        # If user reloads page without logging out then should again show data

        if graph_data_stats == [] or type(graph_data_stats) == int:
            session['error'] = graph_data_stats
            return redirect(url_for('auth.login'))
        elif db:
            return redirect(url_for('dashboards.stats_db'))
        else:
            descriptor = model.graph_descriptor()  # Graph Descriptor
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
                                   db=db,
                                   descriptor=descriptor)


# Logout route
@dashboards.route('/logout/', methods=['GET'])
def logout():

    global graph_data_stats, username, password, ssl
    global server, pickle_saver, role_exist
    pickle_saver = True
    graph_data_stats = []
    username = ''
    password = ''
    server = ''
    ssl = ''
    role_exist = ''

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
        server = user_details['server']
        ssl = False if user_details.get('ssl') is None else True
        save_to_DB = False if request.form.get('DB') is None else True
        global graph_data_stats
        global project_lists

        if not save_to_DB:  # If save_to_DB is false then use pickle
            if 'username' in session and graph_data_stats != []:
                session['error'] = "Already logged in"
            else:
                exist = model.user_exists(username, password, server, ssl)

                global role_exist
                if type(exist) == int:
                    role_exist = model.user_role_exist(username)

                    if role_exist:

                        user_data = model.load_users_data_pk(role_exist)
                        resources = model.load_resources_pk(role_exist)
                        resources_bbrc = model.load_resources_bbrc_pk(
                            role_exist)

                        if user_data is not None:
                            plotting_object = graph_generator_DB.\
                                GraphGenerator(
                                    username,
                                    user_data['info'],
                                    resources,
                                    resources_bbrc)

                            graph_data_stats = plotting_object.\
                                graph_generator()

                            project_lists = plotting_object.\
                                project_list_generator()
                        else:
                            session['error'] = "User Registered: Fetching data"

                    else:
                        session['error'] = "Wrong Password"
                        role_exist = ''
                else:
                    session['error'] = exist[0]
        else:  # Use Database and pickle saver value to False over dashboard
            global pickle_saver
            pickle_saver = False

            exist = model.user_exists(username, password, server, ssl)

            if 'username' in session and graph_data_stats != []:
                session['error'] = "Already logged in"
            elif type(exist) == int:
                role_exist = model.user_role_exist(username)

                if role_exist:

                    users_data = mongo.db.users_data.find_one(
                        {'role': role_exist})
                    resources = mongo.db.resources.find_one(
                        {'role': role_exist})

                    session['username'] = username
                    plotting_object = graph_generator_DB.GraphGenerator(
                        username,
                        users_data['info'],
                        resources)
                    graph_data_stats = plotting_object.graph_generator()
                    project_lists = plotting_object.\
                        project_list_generator()

                else:
                    session['error'] = "User role doesn't exist"

            else:
                session['error'] = exist[0]

        if 'error' in session:

            return redirect(url_for('auth.login_DB'))

        else:
            descriptor = model.graph_descriptor()  # Graph Descriptor
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
                                   db=db,
                                   descriptor=descriptor)

    else:
        # If user reloads page
        if graph_data_stats == [] or type(graph_data_stats) == int:
            session['error'] = graph_data_stats
            return redirect(url_for('auth.login_DB'))
        else:
            descriptor = model.graph_descriptor()  # Graph Descriptor
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
                                   db=db,
                                   descriptor=descriptor)


# this route give the details of the project
@dashboards.route('db/project/<id>', methods=['GET'])
def project_db(id):

    global username
    global role_exist

    if role_exist == '':
        return redirect(url_for('auth.login_DB'))

    if pickle_saver:
        users_data = model.load_users_data_pk(role_exist)
        resources = model.load_resources_pk(role_exist)
        resources_bbrc = model.load_resources_bbrc_pk(role_exist)
    else:
        users_data_tb = mongo.db.users_data
        users_data = users_data_tb.find_one({'role': role_exist})
        resources = mongo.db.resources.find_one({'role': role_exist})
        resources_bbrc = mongo.db.resources_bbrc.find_one(
            {'role': role_exist})

    data_array = graph_generator_pp_DB.GraphGenerator(
        username, users_data['info'], id, resources, resources_bbrc
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
    descriptor = model.graph_descriptor()  # Graph Descriptor

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
        id=id,
        descriptor=descriptor)


# this route give the details of the project
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
    descriptor = model.graph_descriptor()  # Graph Descriptor

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
        id=id,
        descriptor=descriptor)
