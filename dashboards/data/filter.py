import json
import os.path as op
from collections import OrderedDict
import dashboards
import pandas as pd


def filter_data(p, visible_projects='*'):
    p['projects'] = [e for e in p['projects'] if e['id'] in visible_projects
                     or "*" in visible_projects]
    p['experiments'] = [e for e in p['experiments']
                        if e['project'] in visible_projects
                        or "*" in visible_projects]
    p['scans'] = [e for e in p['scans'] if e['project'] in visible_projects
                  or "*" in visible_projects]
    p['subjects'] = [e for e in p['subjects'] if e['project'] in visible_projects
                     or "*" in visible_projects]

    resources = [e for e in p['resources'] if len(e) == 4]
    p['resources'] = [(project, a, b, c) for (project, a, b, c) in resources
                      if project not in visible_projects
                      or "*" in visible_projects]


def get_stats(p):
    stats = {'Projects': len(p['projects']),
             'Subjects': len(p['subjects']),
             'Experiments': len(p['experiments']),
             'Scans': len(p['scans'])}
    return stats


def get_graphs(p):

    project_acccess = dict_generator_overview(p['projects'], 'project_access', 'id', 'access')
    project_acccess['id_type'] = 'project'
    projects_details = project_acccess

    subjects_per_project = dict_generator_per_view(p['subjects'], 'project', 'ID', 'spp')
    subjects_per_project['id_type'] = 'subject'
    subjects_details = subjects_per_project

    experiments_details = {}
    experiment_type = dict_generator_overview(p['experiments'], 'xsiType', 'ID', 'xsiType')
    experiment_type['id_type'] = 'experiment'
    experiments_types_per_project = dict_generator_per_view_stacked(p['experiments'], 'project', 'xsiType', 'ID')
    experiments_types_per_project['id_type'] = 'experiment'
    prop_exp = proportion_graphs(p['experiments'], 'subject_ID', 'ID', 'Subjects with ', ' experiment(s)')
    prop_exp['id_type'] = 'subject'
    experiments_details['Imaging sessions'] = experiments_types_per_project

    experiments_details['Total amount of sessions'] = experiment_type
    experiments_details['Sessions per subject'] = prop_exp

    columns = ['xnat:imagescandata/quality', 'ID', 'quality',
               'xnat:imagescandata/id']
    scan_quality = dict_generator_overview(p['scans'], *columns)
    scan_quality['id_type'] = 'experiment'

    ordered_graphs = {'Projects': projects_details,
                      'Subjects': subjects_details,
                      'Resources (over time)': {'count': p['longitudinal_data']}}

    ordered_graphs.update(experiments_details)
    # ordered_graphs.update(scans_details)
    ordered_graphs.update(get_resources_details(p['resources']))
    return ordered_graphs


def get_resources_details(resources, project_id=None):

    df = pd.DataFrame(resources,
                      columns=['project', 'session', 'resource', 'label'])

    # Resource types
    resource_types = dict_generator_resources(df, 'label', 'session')
    resource_types['id_type'] = 'experiment'

    resource_type_ps = dict_generator_resources(df, 'label', 'session')
    resource_type_ps['id_type'] = 'experiment'

    pro_exp_list = [[item[0], item[1]] for item in resources]

    pro_exp_df = pd.DataFrame(pro_exp_list, columns=['project', 'session'])

    # Create a Dataframe that have 3 columns where
    # 1st column: project_x will have projects
    # 2nd column: session will have session details
    # 3rd column: project_y will have count of resources
    pro_exp_count = pro_exp_df.groupby('session').count().reset_index()
    project_session = pro_exp_df.drop_duplicates(subset="session")
    resource_count_df = pd.merge(
        project_session, pro_exp_count, on='session')

    resource_count_df['project_y'] = resource_count_df[
        'project_y'].astype(int)

    # Send the above created data from to dict_generator_per_view_stacked
    # This will create the format required for stacked plot
    resource_count_dict = dict_generator_per_view_stacked(
        resource_count_df, 'project_x', 'project_y', 'session')
    resource_count_dict['id_type'] = 'experiment'
    ordered = OrderedDict(sorted(resource_count_dict['count'].items(),
                                 key=lambda x: len(x[0]), reverse=True))
    ordered_ = {a: {str(c)+' Resources/Session': d for c, d in b.items()} for a, b in ordered.items()}
    resource_count_dict_ordered = {'count': ordered_, 'list': resource_count_dict['list']}

    return {'Resources per type': resource_types,
            'Resources per session': resource_count_dict_ordered}


def proportion_graphs(data, x, y, prefix, suffix):

    data_list = [[item[x], item[y]] for item in data]

    # Create a data frame
    df = pd.DataFrame(data_list, columns=['per_view', 'count'])

    # Group by property x as per_view and count
    df_proportion = df.groupby(
        'per_view', as_index=False).count().groupby('count').count()

    # Use count to group by property x
    df_proportion['list'] = df.groupby(
        'per_view', as_index=False).count().groupby(
            'count')['per_view'].apply(list)

    # Add prefix and suffix to count for easy understanding
    # Eg. Number of subject with 1 experiments
    # Here prefix is Number of subject with and suffix is experiments
    # and count is 1
    df_proportion.index = prefix + df_proportion.index.astype(str) + suffix

    return df_proportion.rename(columns={'per_view': 'count'}).to_dict()


def dict_generator_resources(df, x_name, y_name):

    data = df[df[y_name] != 'No Data'][[x_name, y_name]]
    data = data.rename(columns={y_name: 'count'})
    data_df = data.groupby(x_name)['count'].apply(list)
    data = data.groupby(x_name).count()
    data['list'] = data_df
    data_dict = data.to_dict()

    return data_dict


def dict_generator_overview(data, x, y, x_new, extra=None):
    """Generate a dictionary from the data list of project, subjects,
    experiments and scans in the format required for graphs.

    Args:
        data (list): List of projects or subjects or exp or scans
        x (str): The name which will be on X axis of graph
        y (str): The name which will be on Y axis of graph
        x_new (str): The new name which will be shown on X axis of graph
        extra (str, optional): Add another value to be concatenated
            in x_axis, when click on graph occurs. Useful when
            the x_axis values are not unique and by default will not
            be used for concatenation.

    Returns:
        Dict: For each graph this format is used
        {"count": {"x": "y"}, "list": {"x": "list"}}
    """

    property_list = []
    property_none = []

    for item in data:
        if item[x] != '':
            i = [item[x], item[y]]
            if extra is not None:
                i[1] += item[extra]
            property_list.append(i)
        else:
            i = item[y]
            if extra is not None:
                i += '/' + item[extra]
            property_none.append(i)

    property_df = pd.DataFrame(property_list, columns=[x_new, 'count'])

    property_df_series = property_df.groupby(x_new)['count'].apply(list)
    property_final_df = property_df.groupby(x_new).count()
    property_final_df['list'] = property_df_series
    d = property_final_df.to_dict()

    if len(property_none) != 0:
        d['count'].update({'No Data': len(property_none)})
        d['list'].update({'No Data': property_none})

    return d


def dict_generator_per_view(data, x, y, x_new):
    """Generate a dictionary from the data list of subjects,
    experiments and scans in the format required for graphs.
    The generated data is only for single project.

    Args:
        data (list): List of projects or subjects or exp or scans
        x (str): The name which will be on X axis of graph
        y (str): The name which will be on Y axis of graph
        x_new (str): The new name which will be shown on X axis of graph

    Returns:
         Dict: For each graph this format is used
            {"count": {"x": "y"}, "list": {"x": "list"}}
    """
    per_list = [[item[x], item[y]] for item in data]

    per_df = pd.DataFrame(per_list, columns=[x_new, 'count'])
    per_df_series = per_df.groupby(x_new)['count'].apply(list)
    per_df = per_df.groupby(x_new).count()
    per_df['list'] = per_df_series

    per_view = per_df.to_dict()

    return per_view


def dict_generator_per_view_stacked(data, x, y, z):
    """Generate dict format that is used by plotly for stacked graphs view,
    data like project details, scan, experiments, subject as field

    x and y are used to group by the pandas data frame
    and both are used on x axis values while z is used on y axis.
    Args:
        data (list): List of data project, subject, scan and experiments
        x (str): The name which will be on X axis of graph
        y (str): The name which will be on X axis of graph
        z (str): The name which will be on Y axis of graph

    Returns:
        dict:{count:{prop_x:{prop_y:prop_z_count}},
        list:{prop_x:{prop_y:prop_z_list}}
        }
    """

    per_df = data

    if isinstance(data, list):
        per_list = [[item[x], item[y], item[z]] for item in data]
        columns = [x, y, z]
        per_df = pd.DataFrame(per_list, columns=columns)

    per_df_series = per_df.groupby([x, y])[z].apply(list)

    per_df = per_df.groupby([x, y]).count()
    per_df['list'] = per_df_series

    dict_tupled = per_df.to_dict()

    dict_output_list = {}
    for item in dict_tupled['list']:
        dict_output_list[item[0]] = {}

    for item in dict_tupled['list']:
        d = {item[1]: dict_tupled['list'][item]}
        dict_output_list[item[0]].update(d)

    dict_output_count = {}

    for item in dict_tupled[z]:
        dict_output_count[item[0]] = {}

    for item in dict_tupled[z]:
        d = {item[1]: dict_tupled[z][item]}
        dict_output_count[item[0]].update(d)

    return {'count': dict_output_count, 'list': dict_output_list}


def filter_data_per_project(p, project_id):
    stats = {}

    pd = get_projects_details_pp(p['projects'], project_id)

    # Pre processing for subject details required
    subjects = [s for s in p['subjects'] if s['project'] == project_id]
    sd = dict_generator_per_view(subjects, 'project', 'ID', 'spp')
    sd['id_type'] = 'subject'

    # Pre processing experiment details
    experiments = [e for e in p['experiments'] if e['project'] == project_id]
    ed = {}
    experiment_type = dict_generator_overview(experiments, 'xsiType', 'ID', 'xsiType')
    experiment_type['id_type'] = 'experiment'
    experiments_types_per_project = dict_generator_per_view_stacked(experiments, 'project', 'xsiType', 'ID')
    experiments_types_per_project['id_type'] = 'experiment'
    prop_exp = proportion_graphs(experiments, 'subject_ID', 'ID', 'Subjects with ', ' experiment(s)')
    prop_exp['id_type'] = 'subject'
    ed['Sessions per subject'] = prop_exp

    # Pre processing scans details
    scans = [s for s in p['scans'] if s['project'] == project_id]
    # Scans type information
    fp = op.join(op.dirname(dashboards.__file__), '..', 'data',
                 'whitelist.json')
    whitelist = json.load(open(fp))

    filtered_scans = [s for s in scans if s['xnat:imagescandata/type'] in whitelist]

    columns = ['xnat:imagescandata/type', 'ID', 'type', 'xnat:imagescandata/id']
    type_dict = dict_generator_overview(filtered_scans, *columns)
    type_dict['id_type'] = 'experiment'

    prop_scan = proportion_graphs(scans, 'ID', 'xnat:imagescandata/id', '', ' scans')
    prop_scan['id_type'] = 'subject'

    columns = ['xnat:imagescandata/quality', 'ID', 'quality',
               'xnat:imagescandata/id']
    scan_quality = dict_generator_overview(scans, *columns)
    scan_quality['id_type'] = 'experiment'

    scd = {'Scan quality': scan_quality,
           'Scan Types': type_dict,
           'Scans per session': prop_scan}

    stats = {'Subjects': len(subjects),
             'Experiments': len(experiments),
             'Scans': len(scans)}

    ordered_graphs = {'Project details': pd,
                      'Stats': stats}
    ordered_graphs.update(ed)
    ordered_graphs.update(scd)

    return ordered_graphs


def get_projects_details_pp(projects, project_id):

    res = {}

    p = [e for e in projects if e['id'] == project_id][0]

    res['Owner(s)'] = p['project_owners'].split('<br/>')

    res['Collaborator(s)'] = p['project_collabs'].split('<br/>')
    if res['Collaborator(s)'][0] == '':
        res['Collaborator(s)'] = ['None']

    res['Member(s)'] = p['project_members'].split('<br/>')
    if res['Member(s)'][0] == '':
        res['Member(s)'] = ['None']

    res['User(s)'] = p['project_users'].split('<br/>')
    if res['User(s)'][0] == '':
        res['User(s)'] = ['None']

    res['last_accessed'] = p['project_last_access'].split('<br/>')

    for e in ['insert_user', 'insert_date', 'project_access', 'name',
              'project_last_workflow']:
        res[e] = p[e]

    return res


# def get_resources_details_pp(resources, project_id):
#     res = get_resources_details(resources, project_id)
#     if 'Resources per session' in res:
#         del res['Resources per session']
#
#     return res
