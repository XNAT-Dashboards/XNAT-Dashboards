# Import flask dependencies
from flask import Blueprint, session, render_template
from pyxnat_connection import graph_generator

# Define the blueprint: 'dashboards', set its url prefix: app.url/dashboards
dashboards = Blueprint('dashboards', __name__, url_prefix='/dashboards')


# Set the route and accepted methods
@dashboards.route('/stats/', methods=['GET'])
def stats():

    user_details = session['user_d']
    username = user_details['username']
    password = user_details['password']
    server = user_details['server']

    data = graph_generator.GraphGenerator(username,
                                          password,
                                          server).graph_generator()

    return render_template('dashboards/stats_dashboards.html', data=data)
