import pandas as pd
import logging as log
from datetime import date
from collections import OrderedDict


def get_tests(df, tests, value='has_passed'):
    archiving = df[['archiving_validator']].replace({0: 'No Data'})
    if archiving.empty:
        log.warning('No tests found.')
        return None

    archiving['version'] = archiving.apply(lambda row: row['archiving_validator']['version']
    if row['archiving_validator'] != 'No Data' else row['archiving_validator'], axis=1)
    for t in tests:
        archiving[t] = archiving.apply(lambda row: row['archiving_validator'].get(t, {value: 'No Data'})[value]
        if row['archiving_validator'] != 'No Data' else row['archiving_validator'],
        axis=1)
    columns = list(tests)
    columns.append('version')
    return archiving[columns]


def which_sessions_have_validators(br):
    # make a list of all existing validators
    validators = set()
    for r in list(br['BBRC_Validators']):
        for e in r:
            validators.add(e)

    vl, count = {}, {}

    # for each validator make a list of sessions having it
    for v in validators:
        has_val, has_not_val = [], []
        for r, s in zip(br['BBRC_Validators'], br['Session']):
            if v in r:
                has_val.append(s)
            else:
                has_not_val.append(s)
        vl[v] = {'Sessions with Validator': has_val,
                 'Sessions without Validator': has_not_val}
        count[v] = {'Sessions with Validator': len(has_val),
                    'Sessions without Validator': len(has_not_val)}
    d = {'count': count, 'list': vl}
    series = pd.Series([x for e in br['BBRC_Validators'] for x in e])
    series_dict = (series.value_counts()).to_dict()
    key_list = series_dict.keys()
    d['list'] = OrderedDict((k, d['list'][k]) for k in key_list)
    d['count'] = OrderedDict((k, d['count'][k]) for k in key_list)
    return d


def diff_dates(df):
    # Generate a dataframe of TestAcquisitionDate and its InsertDate
    tests = get_tests(df, ['IsAcquisitionDateConsistent'], 'data')
    df = df.join(tests).reset_index()

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
        return {}

    # Calculates the time difference
    df['Diff'] = df.apply(lambda x: dates_diff_calc(x['Acq date'], x['Insert date']), axis=1)

    # Create the dictionary: {"count": {"x": "y"}, "list": {"x": "list"}}
    df_diff = df[['Session', 'Diff']].rename(
        columns={'Session': 'count'})
    cut = pd.cut(df_diff.Diff, [0, 2, 10, 100, 1000, 10000], include_lowest=True)
    df_series = df_diff.groupby(cut)['count'].apply(list)
    df_diff = df_diff.groupby(cut).count()
    df_diff['list'] = df_series
    df_diff.index = df_diff.index.astype(str) + ' days'
    df_diff = df_diff.to_dict()
    df_diff['id_type'] = 'experiment'
    return df_diff


def dates_diff_calc(date_1, date_2):
    """This method returns the difference in days between 2 date strings."""
    # Calculates difference between 2 dates
    date_1_l = list(map(int, date_1.split('-')))
    date_2_l = list(map(int, date_2.split('-')))

    d1 = date(date_1_l[0], date_1_l[1], date_1_l[2])
    d2 = date(date_2_l[0], date_2_l[1], date_2_l[2])
    diff = d1 - d2

    return abs(diff.days)


def build_test_grid(p):
    columns = ['Project', 'Session', 'archiving_validator', 'BBRC_Validators',
               'Insert date']
    resources = [e for e in p['resources'] if len(e) > 4]
    df = pd.DataFrame(resources, columns=columns).set_index('Session')

    if df[['archiving_validator']].query('archiving_validator != 0').empty:
        msg = 'Project has no ArchivingValidators. Test grid not available.'
        log.warning(msg)
        return [], [], []

    excluded = ['version', 'experiment_id', 'generated']
    tests = set(df.iloc[0]['archiving_validator']).difference(excluded)
    tests = sorted(tests)

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
