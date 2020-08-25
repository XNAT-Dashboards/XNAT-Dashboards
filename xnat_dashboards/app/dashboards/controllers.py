# Import flask dependencies
from flask import Blueprint, render_template, session,\
    redirect, url_for
from xnat_dashboards.data_cleaning import graph_generator
from xnat_dashboards.app.dashboards import model

# Define the blueprint: 'dashboards', set its url prefix: app.url/dashboards
dashboards = Blueprint('dashboards', __name__, url_prefix='/dashboards')


# Logout route
@dashboards.route('/logout/', methods=['GET'])
def logout():
    """Logout route here we delete all existing sesson variables

    Returns:
        route: Redirect to login page.
    """
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
    """This is the overview dashboard route.

    First we check whether pickle file have same server details
    if same server details exists we load the pickle data.
    Then sends the data processed from graph generator file
    to the frontend.

    Returns:
        route: The jinja html templates to frontend
    """
    # If server key doesn't exist return to login page

    if 'server' not in session:
        return redirect(url_for('auth.login_DB'))

    data = model.load_users_data(session['server'])

    # Check if pickle data is of correct server
    if data is not None:

        # Calling plot generator
        plotting_object = graph_generator.\
            GraphGenerator(
                session['username'],
                session['role_exist'],
                data,
                session['project_visible'])

        graph_data_stats = plotting_object.\
            graph_generator()

        longitudinal_data = plotting_object.\
            graph_generator_longitudinal()

        project_lists = plotting_object.\
            project_list_generator()
    else:
        # If mismatch between login server url and pickle server url
        # add error message in session
        session['error'] = 'Wrong server url of pickle or data'
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
    """This is the per project dashboard view.

    Args:
        id (str): Id of the project we like to view.

    Returns:
        route: Project details
    """
    if session['role_exist'] == '':
        return redirect(url_for('auth.login_DB'))

    data = model.load_users_data(session['server'])

    # Get the details for plotting
    data_array = graph_generator.GraphGeneratorPP(
        session['username'], id, session['role_exist'],
        data, session['project_visible']
    ).graph_generator()

    # If no data found redirect to login page else render the data
    # with template
    if data_array is None:

        return render_template('dashboards/stats_dashboards.html')

    graph_data = data_array[0]
    stats_data = data_array[1]

    return render_template(
        'dashboards/stats_dashboards_pp.html',
        graph_data=graph_data,
        stats_data=stats_data,
        username=session['username'].capitalize(),
        server=session['server'],
        db=True,
        test_grid=data_array[3],
        data_array=data_array[2],
        id=id)
