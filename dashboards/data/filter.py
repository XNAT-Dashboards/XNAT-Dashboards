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
    lists = df.groupby(x)[y].apply(list).rename(lambda x: str(x))

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
