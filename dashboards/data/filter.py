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
    p['resources'] = [e for e in p['resources'] if e[0] in visible_projects
                      or "*" in visible_projects]


def get_stats(p):
    stats = {'Projects': len(p['projects']),
             'Subjects': len(p['subjects']),
             'Experiments': len(p['experiments']),
             'Scans': len(p['scans'])}
    return stats


def get_graphs(p):

    projects_details = dict_generator_overview(p['projects'], 'project_access', 'id')
    projects_details['id_type'] = 'project'

    x, y = 'project', 'ID'
    df = pd.DataFrame([[e[x], e[y]] for e in p['subjects']], columns=[x, y])
    subjects_details = res_df_to_dict(df, x, y)
    subjects_details['id_type'] = 'subject'

    experiments_details = {}
    experiment_type = dict_generator_overview(p['experiments'], 'xsiType', 'ID')
    experiment_type['id_type'] = 'experiment'
    experiments_types_per_project = res_df_to_stacked(p['experiments'], 'project', 'xsiType', 'ID')
    experiments_types_per_project['id_type'] = 'experiment'
    prop_exp = proportion_graphs(p['experiments'], 'subject_ID', 'ID', 'Subjects with ', ' experiment(s)')
    prop_exp['id_type'] = 'subject'
    experiments_details['Imaging sessions'] = experiments_types_per_project

    experiments_details['Total amount of sessions'] = experiment_type
    experiments_details['Sessions per subject'] = prop_exp

    columns = ['xnat:imagescandata/quality', 'ID', 'xnat:imagescandata/id']
    scan_quality = dict_generator_overview(p['scans'], *columns)
    scan_quality['id_type'] = 'experiment'

    graphs = {'Projects': projects_details,
              'Subjects': subjects_details,
              'Resources (over time)': {'count': p['longitudinal_data']}}

    graphs.update(experiments_details)
    resources = [e for e in p['resources'] if len(e) == 4]
    graphs['Resources per type'] = get_nres_per_type(resources)
    graphs['Resources per session'] = get_nres_per_session(resources)

    br = [e for e in p['resources'] if len(e) > 4]

    from dashboards.data import bbrc
    resources = bbrc.get_resource_details(br)
    del resources['Version Distribution']
    graphs.update(resources)

    return graphs


def get_nres_per_type(resources):
    columns = ['project', 'session', 'resource', 'label']
    df = pd.DataFrame(resources, columns=columns)
    # Resource types
    resource_types = res_df_to_dict(df, 'label', 'session')
    resource_types['id_type'] = 'experiment'
    return resource_types


def get_nres_per_session(resources):
    columns = ['project', 'session', 'abstract_id', 'resource_name']
    df = pd.DataFrame(resources, columns=columns)
    df2 = df[['session', 'project']].set_index('session')
    counts = df[['session', 'resource_name']].groupby('session').count()
    counts = counts.rename(columns={'resource_name': 'nres'})
    df2 = df2.join(counts).reset_index().drop_duplicates()

    res_count = res_df_to_stacked(df2, 'project', 'nres', 'session')
    res_count['id_type'] = 'experiment'
    od = OrderedDict(sorted(res_count['count'].items(),
                            key=lambda x: len(x[0]), reverse=True))
    ordered_ = {a: {str(c) + ' Resources/Session': d for c, d in b.items()}
                for a, b in od.items()}
    return {'count': ordered_, 'list': res_count['list']}


def proportion_graphs(data, x, y, prefix, suffix):

    data_list = [[item[x], item[y]] for item in data]

    df = pd.DataFrame(data_list, columns=['per_view', 'count'])

    # Group by property x as per_view and count
    df_proportion = df.groupby(
        'per_view', as_index=False).count().groupby('count').count()

    # Use count to group by property x
    df_proportion['list'] = df.groupby(
        'per_view', as_index=False).count().groupby(
            'count')['per_view'].apply(list)

    df_proportion.index = prefix + df_proportion.index.astype(str) + suffix

    return df_proportion.rename(columns={'per_view': 'count'}).to_dict()


def res_df_to_dict(df, x, y):

    df = df[[x, y]].query('%s != "No Data"' % y)
    lists = df.groupby(x)[y].apply(list)
    counts = lists.apply(lambda row: len(row))
    return pd.DataFrame({'list': lists, 'count': counts}).to_dict()




def res_df_to_stacked(df, x, y, z):

    if isinstance(df, list):
        per_list = [[e[x], e[y], e[z]] for e in df]
        df = pd.DataFrame(per_list, columns=[x, y, z])

    series = df.groupby([x, y])[z].apply(list)
    data = df.groupby([x, y]).count()
    data['list'] = series
    counts, lists = {}, {}

    for (p, n), row in data.iterrows():
        lists.setdefault(p, {})
        counts.setdefault(p, {})
        lists[p][n] = row.list
        counts[p][n] = row[z]

    return {'count': counts, 'list': lists}


def dict_generator_overview(data, x, y, extra=None):
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

    df = pd.DataFrame(property_list, columns=[x, y])[[y, x]]
    d = res_df_to_dict(df, x, y)
    if len(property_none) != 0:
        d['count'].update({'No Data': len(property_none)})
        d['list'].update({'No Data': property_none})

    return d


def get_graphs_per_project(p):

    # Graph 0
    ed = {}
    prop_exp = proportion_graphs(p['experiments'], 'subject_ID', 'ID', 'Subjects with ', ' experiment(s)')
    prop_exp['id_type'] = 'subject'
    ed['Sessions per subject'] = prop_exp

    # Graph #1
    fp = op.join(op.dirname(dashboards.__file__),
                 '..', 'data', 'whitelist.json')
    whitelist = json.load(open(fp))
    filtered_scans = [s for s in p['scans'] if s['xnat:imagescandata/type'] in whitelist]
    columns = ['xnat:imagescandata/type', 'ID', 'xnat:imagescandata/id']
    type_dict = dict_generator_overview(filtered_scans, *columns)
    type_dict['id_type'] = 'experiment'

    # Graph #2
    prop_scan = proportion_graphs(p['scans'], 'ID', 'xnat:imagescandata/id', '', ' scans')
    prop_scan['id_type'] = 'subject'

    # Graph #3
    columns = ['xnat:imagescandata/quality', 'ID', 'xnat:imagescandata/id']
    scan_quality = dict_generator_overview(p['scans'], *columns)
    scan_quality['id_type'] = 'experiment'

    scd = {'Scan quality': scan_quality,
           'Scan Types': type_dict,
           'Scans per session': prop_scan}

    ed.update(scd)

    return ed


def get_projects_details_pp(p, project_id):
    res = {}

    p = [e for e in p['projects'] if e['id'] == project_id][0]

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
