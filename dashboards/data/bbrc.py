import pandas as pd
import logging as log
from datetime import date


def get_tests(df, tests, value='has_passed'):
    archiving = df[['archiving_validator']].query('archiving_validator != 0')
    if archiving.empty:
        log.warning('No tests found.')
        return None
    archiving['version'] = archiving.apply(lambda row: row['archiving_validator']['version'], axis=1)
    for t in tests:
        archiving[t] = archiving.apply(lambda row: row['archiving_validator'].get(t, {value: 'No Data'})[value], axis=1)
    columns = list(tests)
    columns.append('version')
    return archiving[columns]


def which_sessions_have_validators(br):

    # make a list of all existing validators
    validators = set()
    for r in br:
        if r[2] != 0:
            for e in r[3]:
                validators.add(e)

    vl, count = {}, {}

    # for each validator make a list of sessions having it
    for v in validators:
        has_val, has_not_val = [], []
        for r in br:
            if v in r[3]:
                has_val.append(r[0])
            else:
                has_not_val.append(r[0])
        vl[v] = {'Sessions with Validator': has_val,
                 'Sessions without Validator': has_not_val}
        count[v] = {'Sessions with Validator': len(has_val),
                    'Sessions without Validator': len(has_not_val)}

    return {'count': count, 'list': vl}


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
         'BBRC validators': which_sessions_have_validators(data),
         'Is acquisition data consistent across the whole session?': cad}
    return d


def diff_dates(resources_bbrc, project_id):

    if resources_bbrc is None:
        print('RESOURCES_BBRC is NONE')
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


def build_test_grid(br):

    p, exp_id, archiving_validator, bv, insert_date = br[0]

    if archiving_validator == 0:
        msg = 'Project %s has no validators. Test grid not available.' % p
        log.warning(msg)
        return [], [], []

    excluded = ['version', 'experiment_id', 'generated']
    columns = ['project', 'exp_id', 'archiving_validator', 'bv', 'insert_date']
    df = pd.DataFrame(br, columns=columns).set_index('exp_id')
    tests = sorted(set([e for e in list(archiving_validator.keys())
                        if e not in excluded]))
    data = get_tests(df, tests, 'data')
    has_passed = get_tests(df, tests)

    versions = list(has_passed.version.unique())

    d = []
    for eid, r in data.iterrows():
        row = [eid, ['version', r['version']]]
        for test in tests:
            item = [bool(has_passed.loc[eid][test]), r[test]]
            row.append(item)
        d.append(row)

    return [tests, d, versions]
