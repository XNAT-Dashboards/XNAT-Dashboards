# Import flask dependencies
from flask import Blueprint, render_template, session,\
    redirect, url_for
from xnat_dashboards.data_cleaning import graph_generator
from xnat_dashboards.app.dashboards import model

# Define the blueprint: 'dashboard', set its url prefix: app.url/dashboard
dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')


# Logout route
@dashboard.route('/logout/', methods=['GET'])
def logout():
    """Logout route here we delete all existing session variables

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
    if 'role_exist' in session:
        del session['role_exist']

    session['error'] = -1

    return redirect(url_for('auth.login'))


@dashboard.route('/stats/', methods=['GET'])
def stats():
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
        return redirect(url_for('auth.login'))

    pickle_data = model.load_users_data(session['server'])

    # Check if pickle data is of correct server
    if pickle_data is not None:

        # Calling plot generator
        plotting_object = graph_generator.\
            GraphGenerator(
                session['username'],
                session['role_exist'],
                pickle_data,
                session['project_visible'])

        overview = plotting_object.get_overview()

        longitudinal_data = plotting_object.get_longitudinal_graphs()

        project_lists = plotting_object.get_project_list()
    else:
        # If mismatch between login server url and pickle server url
        # add error message in session
        session['error'] = 'Wrong server url of pickle or data'
        'not downloaded'

    # If error message in session redirect to login page else render the data
    if 'error' in session:
        return redirect(url_for('auth.login'))

    else:
        project_list = project_lists[0]
        project_list_ow_co_me = project_lists[1]
        graphs = overview[0]
        stats = overview[1]

        return render_template(
            'dashboards/stats_dashboards.html',
            graph_data=graphs,
            project_list=project_list,
            stats_data=stats,
            longitudinal_data=longitudinal_data,
            project_list_ow_co_me=project_list_ow_co_me,
            username=session['username'].capitalize(),
            server=session['server'],
            db=True)


# this route give the details of the project
@dashboard.route('project/<id>', methods=['GET'])
def project(id):
    """This is the per project dashboard view.

    Args:
        id (str): Id of the project we like to view.

    Returns:
        route: Project details
    """
    if session['role_exist'] == '':
        return redirect(url_for('auth.login'))

    pickle_data = model.load_users_data(session['server'])

    # Get the details for plotting
    per_project_view = graph_generator.GraphGeneratorPP(
        session['username'], id, session['role_exist'],
        pickle_data, session['project_visible']
    ).get_project_view()

    # If no data found redirect to login page else render the data
    # with template
    if per_project_view is None:

        return render_template('dashboards/stats_dashboards.html')

    graphs = per_project_view[0]
    stats = per_project_view[1]

    return render_template(
        'dashboards/stats_dashboards_pp.html',
        graph_data=graphs,
        stats_data=stats,
        username=session['username'].capitalize(),
        server=session['server'],
        db=True,
        test_grid=per_project_view[3],
        data_array=per_project_view[2],
        id=id)
