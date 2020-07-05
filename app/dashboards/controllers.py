# Import flask dependencies
from flask import Blueprint, render_template, session, request,\
                  redirect, url_for
from generators import graph_generator
from app.init_database import mongo


# Define the blueprint: 'dashboards', set its url prefix: app.url/dashboards
dashboards = Blueprint('dashboards', __name__, url_prefix='/dashboards')

graph_data_stats = []
project_lists = []
username = ''
server = ''
db = False


# Set the route and accepted methods
@dashboards.route('/stats/', methods=['POST', 'GET'])
def stats():

    if request.method == "POST":
        global username, server
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
    global graph_data_stats
    graph_data_stats = []
    session['error'] = -1

    if 'username' in session:
        del session['username']
    global db

    if db:
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

        global graph_data_stats
        global project_lists
        users = mongo.db.users
        existing_users = users.find_one({'username': request.form['username']})

        if 'username' in session and graph_data_stats != []:
            session['error'] = "Already logged in"
        elif existing_users is not None:
            if existing_users['password'] == password:

                users_data_tb = mongo.db.users_data
                users_data = users_data_tb.find_one(
                            {'username': username})

                if users_data is not None:

                    session['username'] = username
                    plotting_array = graph_generator.GraphGenerator(
                                                username,
                                                password,
                                                None,
                                                db=db).process_db(
                                                    users_data['info'],
                                                    users_data['project_list']
                                                )
                    graph_data_stats = plotting_array[0]
                    project_lists = plotting_array[1]

                else:
                    session['error'] = "User Registered: Data fetching incomplete"

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
