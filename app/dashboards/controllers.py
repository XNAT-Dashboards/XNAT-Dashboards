# Import flask dependencies
from flask import Blueprint, render_template, session, request, redirect, url_for
from generators import graph_generator

# Define the blueprint: 'dashboards', set its url prefix: app.url/dashboards
dashboards = Blueprint('dashboards', __name__, url_prefix='/dashboards')

graph_data = {}
project_list = []
project_list_ow_co_me = []
username = ''
server = ''
stats_data = {}

# Set the route and accepted methods
@dashboards.route('/stats/', methods=['POST', 'GET'])
def stats():

    if request.method == "POST":
        global username, server
        user_details = request.form
        username = user_details['username']
        password = user_details['password']
        server = user_details['server']

        global graph_data
        global project_list
        global project_list_ow_co_me
        global stats_data
        plotting_object = graph_generator.GraphGenerator(username,
                                                         password,
                                                         server)
        graph_data_stats = plotting_object.graph_generator()
        graph_data = graph_data_stats[0]
        stats_data = graph_data_stats[1]
        project_lists = plotting_object.project_list_generator()
        project_list = project_lists[0]
        project_list_ow_co_me = project_lists[1]

        # Disconnecting the api session
        del plotting_object
        return 'correct'
    else:
        if graph_data == {} or type(graph_data) == int:
            session['error'] = graph_data
            return redirect(url_for('auth.login'))
        else:
            return render_template('dashboards/stats_dashboards.html',
                                   graph_data=graph_data,
                                   project_list=project_list,
                                   stats_data=stats_data,
                                   project_list_ow_co_me=project_list_ow_co_me,
                                   username=username.capitalize(),
                                   server=server)


# Logout route
@dashboards.route('/logout/', methods=['GET'])
def logout():
    global graph_data
    graph_data = {}
    session['error'] = -1
    return redirect(url_for('auth.login'))
