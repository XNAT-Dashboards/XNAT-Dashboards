import json
import os.path as op
from collections import OrderedDict
import dashboards
import pandas as pd


def filter_data(p, visible_projects='*'):
    """Filter data from the pickle object based on the
    provided list of accessible projects."""
    p_filtered = p.copy()
    p_filtered['projects'] = [e for e in p['projects']
                              if e['id'] in visible_projects
                              or "*" in visible_projects]
    p_filtered['experiments'] = [e for e in p['experiments']
                                 if e['project'] in visible_projects
                                 or "*" in visible_projects]
    p_filtered['scans'] = [e for e in p['scans']
                           if e['project'] in visible_projects
                           or "*" in visible_projects]
    p_filtered['subjects'] = [e for e in p['subjects']
                              if e['project'] in visible_projects
                              or "*" in visible_projects]
    p_filtered['resources'] = [e for e in p['resources']
                               if e[0] in visible_projects
                               or "*" in visible_projects]
    return p_filtered


def get_stats(p):
    stats = {'Projects': len(p['projects']),
             'Subjects': len(p['subjects']),
             'Experiments': len(p['experiments']),
             'Scans': len(p['scans'])}
    return stats


def get_graphs(p):
    data, x, y = p['projects'], 'project_access', 'id'
    df = pd.DataFrame([[e[x], e[y]] for e in data], columns=[x, y])
    prd = res_df_to_dict(df, x, y)
    prd['id_type'] = 'project'

    data, x, y = p['subjects'], 'project', 'ID'
    df = pd.DataFrame([[e[x], e[y]] for e in data], columns=[x, y])
    sd = res_df_to_dict(df, x, y)
    sd['id_type'] = 'subject'

    data, x, y = p['experiments'], 'xsiType', 'ID'
    df = pd.DataFrame([[e[x], e[y]] for e in data], columns=[x, y])
    ed = res_df_to_dict(df, x, y)
    ed['id_type'] = 'experiment'

    edpp = res_df_to_stacked(p['experiments'], 'project', 'xsiType', 'ID')
    edpp['id_type'] = 'experiment'

    prop_exp = proportion_graphs(p['experiments'], 'subject_ID', 'ID', 'Subjects with ', ' experiment(s)')
    prop_exp['id_type'] = 'subject'

    columns = ['xnat:imagescandata/quality', 'ID', 'xnat:imagescandata/id']
    x, y = columns[:2]
    df = pd.DataFrame([[e[x], e[y]] for e in p['scans']], columns=columns[:2])
    df[x].replace({'': 'No Data'}, inplace=True)
    scan_quality = res_df_to_dict(df, x, y)
    scan_quality['id_type'] = 'experiment'

    resources = [e for e in p['resources'] if len(e) == 4]

    graphs = {'Projects': prd,
              'Subjects': sd,
              'Imaging sessions': edpp,
              'Total amount of sessions': ed,
              'Sessions per subject': prop_exp,
              'Scan quality': scan_quality,
              'Resources per type': get_nres_per_type(resources),
              'Resources per session': get_nres_per_session(resources),
              'Resources (over time)': {'count': p['longitudinal_data']}}

    br = [e for e in p['resources'] if len(e) > 4]

    from dashboards.data import bbrc
    columns = ['Project', 'Session', 'archiving_validator', 'BBRC_Validators',
               'Insert date']
    data = pd.DataFrame(br, columns=columns).set_index('Session')
    resources = bbrc.get_resource_details(data)
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
    x, y = columns[:2]
    df = pd.DataFrame([[e[x], e[y]] for e in filtered_scans],
                      columns=columns[:2])
    type_dict = res_df_to_dict(df, x, y)
    type_dict['id_type'] = 'experiment'

    # Graph #2
    prop_scan = proportion_graphs(p['scans'], 'ID', 'xnat:imagescandata/id', '', ' scans')
    prop_scan['id_type'] = 'subject'

    # Graph #3
    columns = ['xnat:imagescandata/quality', 'ID', 'xnat:imagescandata/id']
    x, y = columns[:2]
    df = pd.DataFrame([[e[x], e[y]] for e in p['scans']], columns=columns[:2])
    df[x].replace({'': 'No Data'}, inplace=True)
    scan_quality = res_df_to_dict(df, x, y)
    scan_quality['id_type'] = 'experiment'

    scd = {'Scan quality': scan_quality,
           'Scan Types': type_dict,
           'Scans per session': prop_scan}

    ed.update(scd)

    # Validators
    from dashboards.data import bbrc
    resources = [e for e in p['resources'] if len(e) > 4]
    columns = ['Project', 'Session', 'archiving_validator', 'BBRC_Validators',
               'Insert date']
    data = pd.DataFrame(resources, columns=columns).set_index('Session')
    print('data', data)
    archiving = data.query('archiving_validator != 0')

    # NOTE: this assumes projects with validators always ArchivingValidators
    # and inversely
    if not archiving.empty:
        br = bbrc.get_resource_details(data)
        ed.update(br)

        dd = bbrc.diff_dates(data)
        ed['Dates difference (Acquisition date - Insertion date)'] = dd
    else:
        br = {'BBRC validators': bbrc.which_sessions_have_validators(data.reset_index())}
        ed.update(br)

    return ed


def get_project_details(p):
    """Extract from the pickle object detailed information about
    a given project and parse it in a comprehensive dict structure."""

    res = {}
    project = p['projects'][0]

    fields = {'Owner(s)': 'project_owners',
              'Member(s)': 'project_members',
              'Collaborator(s)': 'project_collabs',
              'User(s)': 'project_users',
              'last_accessed': 'project_last_access'}

    for k, v in fields.items():
        res[k] = project[v].strip().split(' <br/> ')
        if res[k][0] == '':
            res[k] = ['None']

    for e in ['insert_user', 'insert_date', 'project_access', 'name',
              'project_last_workflow']:
        res[e] = project[e]

    return res
