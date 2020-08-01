# Import flask dependencies
from flask import Blueprint, render_template, session, request,\
    redirect, url_for
from saved_data_processing import graph_generator_DB, graph_generator_pp_DB
from app.dashboards import model


# Define the blueprint: 'dashboards', set its url prefix: app.url/dashboards
dashboards = Blueprint('dashboards', __name__, url_prefix='/dashboards')

graph_data_stats = []  # Contains graph Data loaded globally for get request
project_lists = []  # Contains project list globally for get request
username = ''  # For saving username globally
password = ''  # For saving password globally
server = ''  # For saving server url globally
ssl = ''  # For saving username globally
role_exist = ''


# Logout route
@dashboards.route('/logout/', methods=['GET'])
def logout():

    global graph_data_stats, username, password, ssl
    global server, role_exist
    graph_data_stats = []
    username = ''
    password = ''
    server = ''
    ssl = ''
    role_exist = ''

    if 'username' in session:
        del session['username']
    session['error'] = -1

    return redirect(url_for('auth.login_DB'))


@dashboards.route('/db/stats/', methods=['GET', 'POST'])
def stats_db():

    if request.method == 'POST':
        global username, server
        user_details = request.form
        username = user_details['username']
        password = user_details['password']
        server = user_details['server']
        ssl = False if user_details.get('ssl') is None else True
        global graph_data_stats
        global project_lists

        if 'username' in session and graph_data_stats != []:
            session['error'] = "Already logged in"
        else:
            exist = model.user_exists(username, password, server, ssl)

            global role_exist

            if type(exist) == int:
                config = model.user_role_config(username)

                if config:
                    if username in config['user roles']:
                        role_exist = config['user roles'][username]
                    else:
                        role_exist = 'guest'

                    user_data = model.load_users_data_pk(server)
                    resources = model.load_resources_pk(server)
                    resources_bbrc = model.load_resources_bbrc_pk(
                            server)

                    if user_data is not None:
                        plotting_object = graph_generator_DB.\
                            GraphGenerator(
                                username,
                                user_data['info'],
                                role_exist,
                                config['project_visible'],
                                resources,
                                resources_bbrc)

                        graph_data_stats = plotting_object.\
                            graph_generator()

                        project_lists = plotting_object.\
                            project_list_generator()
                    else:
                        session['error'] = 'Wrong server or data'
                        'not downloaded'

                else:
                    session['error'] = "Wrong Password"
                    role_exist = ''
            else:
                session['error'] = exist

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
                                   db=True)

    else:
        # If user reloads page
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
                                   db=True)


# this route give the details of the project
@dashboards.route('db/project/<id>', methods=['GET'])
def project_db(id):

    global username
    global role_exist

    if role_exist == '':
        return redirect(url_for('auth.login_DB'))

    users_data = model.load_users_data_pk(server)
    resources = model.load_resources_pk(server)
    resources_bbrc = model.load_resources_bbrc_pk(server)

    config = model.user_role_config(username)

    # Get the details for plotting
    data_array = graph_generator_pp_DB.GraphGenerator(
        username, users_data['info'], id, role_exist,
        config['project_visible'], resources, resources_bbrc
    ).graph_generator()

    if data_array is None:

        return render_template('dashboards/stats_dashboards_pp.html')

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
        db=True,
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
