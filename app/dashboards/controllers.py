# Import flask dependencies
from flask import Blueprint, render_template, session, request, redirect, url_for
from pyxnat_connection import graph_generator

# Define the blueprint: 'dashboards', set its url prefix: app.url/dashboards
dashboards = Blueprint('dashboards', __name__, url_prefix='/dashboards')


data = {}

# Set the route and accepted methods
@dashboards.route('/stats/', methods=['POST', 'GET'])
def stats():

    if(request.method == "POST"):
        user_details = request.form
        username = user_details['username']
        password = user_details['password']
        server = user_details['server']
        global data
        data = graph_generator.GraphGenerator(username,
                                            password,
                                            server).graph_generator()
        return 'correct'
    else:
        if(data == {} or type(data) == int):
            session['error'] = data
            return redirect(url_for('auth.login'))
        else:
            return render_template('dashboards/stats_dashboards.html',
                                   data=data)
