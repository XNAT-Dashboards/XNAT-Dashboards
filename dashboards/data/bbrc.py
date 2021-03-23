import pandas as pd
import logging as log
from datetime import date


def get_tests(df, tests, value='has_passed'):
    print(tests)
    archiving = df[['archiving_validator']].query('archiving_validator != 0')
    archiving['version'] = archiving.apply(lambda row: row['archiving_validator']['version'], axis=1)
    for t in tests:
        archiving[t] = archiving.apply(lambda row: row['archiving_validator'].get(t, {value: 'No Data'})[value], axis=1)
    columns = list(tests)
    columns.append('version')
    return archiving[columns]


def generate_bbrc_validators_dict(df):

    bv = {'count': {}, 'list': {}}
    series = pd.Series([x for e in df['BBRC_Validators'] for x in e])
    series_dict = (series.value_counts()).to_dict()
    for k, v in series_dict.items():
        bv['count'][k] = {}
        bv['count'][k]['Sessions with Validator'] = v
        list_ = df[pd.DataFrame(df.BBRC_Validators.tolist()).isin([k]).any(1).values]
        ses = [x for x in list_['Session']]
        bv['list'][k] = {}
        bv['list'][k]['Sessions with Validator'] = ses
        df2 = df.set_index('Session')
        df_missing_ses = df2.loc[set(df2.index).difference(ses)].sort_index()
        df_missing_ses = df_missing_ses.reset_index()
        bv['count'][k]['Sessions without Validator'] = len(df_missing_ses['Session'])
        bv['list'][k]['Sessions without Validator'] = list(df_missing_ses['Session'])

    return bv


def get_resource_details(resources, project_id=None):

    # Generating specifc resource type
    columns = ['Project', 'Session', 'archiving_validator', 'BBRC_Validators',
               'Insert date']
    data = pd.DataFrame(resources, columns=columns).set_index('Session')
    tests = get_tests(data, ['HasUsableT1', 'IsAcquisitionDateConsistent'])
    data = data.join(tests).reset_index()

    if project_id is not None:
        data = data.groupby('Project').get_group(project_id)

    # Usable t1
    from dashboards.data import filter
    usable_t1 = filter.res_df_to_dict(data, 'HasUsableT1', 'Session')
    usable_t1['id_type'] = 'experiment'

    # Version Distribution
    version = filter.res_df_to_dict(data, 'version', 'Session')
    version['id_type'] = 'experiment'

    # consisten_acq_date
    cad = filter.res_df_to_dict(data, 'IsAcquisitionDateConsistent', 'Session')
    cad['id_type'] = 'experiment'

    d = {'Sessions with usable T1': usable_t1,
         'Version Distribution': version,
         'BBRC validators': generate_bbrc_validators_dict(data),
         'Is acquisition data consistent across the whole session?': cad}
    return d


def diff_dates(resources_bbrc, project_id):

    if resources_bbrc is None:
        return None

    # Generate a dataframe of TestAcquisitionDate and its InsertDate
    columns = ['Project', 'Session', 'archiving_validator', 'bv', 'Insert date']
    df = pd.DataFrame(resources_bbrc, columns=columns).set_index('Session')
    tests = get_tests(df, ['IsAcquisitionDateConsistent'], 'data')
    df = df.join(tests).reset_index()

    # Filter by project_id
    try:
        df = df.groupby(['Project']).get_group(project_id)
    except KeyError:
        print('ERROR', project_id)
        return {'count': {}, 'list': {}}

    # Drop experiments with No Date information
    dates_acq_list = []
    dates_acq_dict = df[['IsAcquisitionDateConsistent']].to_dict()['IsAcquisitionDateConsistent']

    for k, v in dates_acq_dict.items():
        if isinstance(v, dict) and 'session_date' in v:
            dates_acq_list.append(v['session_date'])
        else:
            msg = 'Invalid IsAcquisitionDateConsistent value {}'.format(v)
            log.warning(msg)
            dates_acq_list.append('No Data')
    df['Acq date'] = dates_acq_list
    df = df[df['Acq date'] != 'No Data']

    # if DataFrame empty
    if df.empty:
        print('ERROR DF EMPTY')
        return {'count': {}, 'list': {}}

    # Calculates the time difference
    df['Diff'] = df.apply(lambda x: dates_diff_calc(x['Acq date'], x['Insert date']), axis=1)

    # Create the dictionary: {"count": {"x": "y"}, "list": {"x": "list"}}
    df_diff = df[['Session', 'Diff']].rename(
        columns={'Session': 'count'})
    cut = pd.cut(df_diff.Diff, [0, 2, 10, 100, 1000, 10000])
    df_series = df_diff.groupby(cut)['count'].apply(list)
    df_diff = df_diff.groupby(cut).count()
    df_diff['list'] = df_series
    df_diff.index = df_diff.index.astype(str) + ' days'

    return df_diff.to_dict()


def dates_diff_calc(date_1, date_2):
    """This method returns the difference in days between 2 date strings."""
    # Calculates difference between 2 dates
    date_1_l = list(map(int, date_1.split('-')))
    date_2_l = list(map(int, date_2.split('-')))

    d1 = date(date_1_l[0], date_1_l[1], date_1_l[2])
    d2 = date(date_2_l[0], date_2_l[1], date_2_l[2])
    diff = d1 - d2

    return abs(diff.days)


def generate_test_grid_bbrc(resources_bbrc):

    tests_union = []
    project, exp_id, archiving_validator, bv, insert_date = resources_bbrc[0]
    for test in archiving_validator:
        if test not in tests_union and test not in ['version', 'experiment_id', 'generated']:
                tests_union.append(test)
    # Loop through each test
    keyList = ['session', 'version'] + tests_union
    info_dic = {key: [] for key in keyList}
    cat_dic = {key: [] for key in keyList}
    all_dic = {key: [] for key in keyList}
    for resource in resources_bbrc:
        project, exp_id, archiving_validator, bv, insert_date = resource
        if bv and archiving_validator != 0:
            for d in [info_dic, cat_dic, all_dic]:
                d['session'].append(exp_id)
                d['version'].append(archiving_validator['version'])
            for test in tests_union:
                if test in archiving_validator:
                    info_dic[test].append(archiving_validator[test]['data'])
                    cat_dic[test].append(archiving_validator[test]['has_passed'])
                    all_dic[test].append([archiving_validator[test]['has_passed'],
                                          archiving_validator[test]['data']])
                else:
                    info_dic[test].append('')
                    cat_dic[test].append('')
                    all_dic[test].append([False, ''])
    df_info = pd.DataFrame(info_dic)
    df_cat = pd.DataFrame(cat_dic)
    df_all = pd.DataFrame(all_dic)
    return df_all, df_info, df_cat


def filter_data_per_project(resources, project_id):

    resources_bbrc = [e for e in resources if len(e) > 4]
    graphs = get_resource_details(resources_bbrc, project_id)
    bbrc_resources = [e for e in resources_bbrc if e[0] == project_id]
    project, exp_id, archiving_validator, bv, insert_date = bbrc_resources[0]
    if archiving_validator != 0:
        test_grid = generate_test_grid_bbrc(bbrc_resources)
        graphs['test_grid'] = test_grid

    dd = diff_dates(resources_bbrc, project_id)
    graphs['Dates difference (Acquisition date - Insertion date)'] = dd

    return graphs
