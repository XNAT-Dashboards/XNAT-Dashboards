# Import flask dependencies
from flask import Blueprint, render_template, session, request, redirect, url_for
from generators import graph_generator, project_generator

# Define the blueprint: 'dashboards', set its url prefix: app.url/dashboards
dashboards = Blueprint('dashboards', __name__, url_prefix='/dashboards')

graph_data = {}
project_list = []
username = ''
server = ''


# Set the route and accepted methods
@dashboards.route('/stats/', methods=['POST', 'GET'])
def stats():

    if(request.method == "POST"):
        global username, server
        user_details = request.form
        username = user_details['username']
        password = user_details['password']
        server = user_details['server']
        global graph_data
        global project_list
        graph_data = graph_generator.GraphGenerator(username,
                                                    password,
                                                    server).graph_generator()
        project_list = project_generator.projectGenerator(
                                                        username,
                                                        password,
                                                        server).project_list()

        return 'correct'
    else:
        if(graph_data == {} or type(graph_data) == int):
            session['error'] = graph_data
            return redirect(url_for('auth.login'))
        else:
            return render_template('dashboards/stats_dashboards.html',
                                   graph_data=graph_data,
                                   project_list=project_list,
                                   username=username.capitalize(),
                                   server=server)
