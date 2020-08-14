# Import flask dependencies
from flask import Blueprint, render_template, session,\
    redirect, url_for
from xnat_dashboards.saved_data_processing import graph_generator_DB
from xnat_dashboards.app.dashboards import model


# Define the blueprint: 'dashboards', set its url prefix: app.url/dashboards
dashboards = Blueprint('dashboards', __name__, url_prefix='/dashboards')


# Logout route
@dashboards.route('/logout/', methods=['GET'])
def logout():

    # Delete session keys if exist
    if 'username' in session:
        del session['username']
    if 'server' in session:
        del session['server']
    if 'project_visible' in session:
        del session['project_visible']
    if 'role_exists' in session:
        del session['role_exists']

    session['error'] = -1

    return redirect(url_for('auth.login_DB'))


@dashboards.route('/db/stats/', methods=['GET'])
def stats_db():

    # If server key doesn't exist return to login page

    if 'server' not in session:
        return redirect(url_for('auth.login_DB'))

    data = model.load_users_data_pk(session['server'])

    # Check if pickle data is of correct server
    if data is not None:

        resources = None
        resources_bbrc = None

        user_data = data['info']

        if 'resources' in data and 'resources_bbrc' in data:
            resources = data['resources']
            resources_bbrc = data['resources_bbrc']

        l_data = data['longitudinal_data']

        # Calling plot generator
        plotting_object = graph_generator_DB.\
            GraphGenerator(
                session['username'],
                user_data,
                l_data,
                session['role_exist'],
                session['project_visible'],
                resources,
                resources_bbrc)

        graph_data_stats = plotting_object.\
            graph_generator()

        longitudinal_data = plotting_object.\
            graph_generator_longitudinal()

        project_lists = plotting_object.\
            project_list_generator()
    else:
        # If server is wrong add error message in session
        session['error'] = 'Wrong server or data'
        'not downloaded'

    # If error message in session redirect to login page else render the data
    if 'error' in session:
        return redirect(url_for('auth.login_DB'))

    else:
        project_list = project_lists[0]
        project_list_ow_co_me = project_lists[1]
        graph_data = graph_data_stats[0]
        stats_data = graph_data_stats[1]

        return render_template(
            'dashboards/stats_dashboards.html',
            graph_data=graph_data,
            project_list=project_list,
            stats_data=stats_data,
            longitudinal_data=longitudinal_data,
            project_list_ow_co_me=project_list_ow_co_me,
            username=session['username'].capitalize(),
            server=session['server'],
            db=True)


# this route give the details of the project
@dashboards.route('db/project/<id>', methods=['GET'])
def project_db(id):

    if session['role_exist'] == '':
        return redirect(url_for('auth.login_DB'))

    data = model.load_users_data_pk(session['server'])
    users_data = data['info']

    resources = None
    resources_bbrc = None

    if 'resources' in data and 'resources_bbrc' in data:
        resources = data['resources']
        resources_bbrc = data['resources_bbrc']

    # Get the details for plotting
    data_array = graph_generator_DB.GraphGeneratorPP(
        session['username'], users_data, id, session['role_exist'],
        session['project_visible'], resources, resources_bbrc
    ).graph_generator()

    # If no data found redirect to login page else render the data
    # with template
    if data_array is None:

        return render_template('dashboards/stats_dashboards.html')

    graph_data = data_array[0]
    stats_data = data_array[1]

    th = data_array[3][0]
    td = data_array[3][1]

    return render_template(
        'dashboards/stats_dashboards_pp.html',
        graph_data=graph_data,
        stats_data=stats_data,
        username=session['username'].capitalize(),
        server=session['server'],
        db=True,
        data_array=data_array[2],
        id=id,
        t_header_info=th,
        t_data_info=td)
