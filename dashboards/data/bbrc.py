from dashboards.data import filter as df
import pandas as pd
import logging as log
from datetime import date


class BBRCDataFilter(df.DataFilter):

    def __init__(self, resources, visible_projects):

        bbrc_resources = []
        for r in [e for e in resources if len(e) > 4]:
            project = r[0]
            if project not in visible_projects or "*" in visible_projects:
                bbrc_resources.append(r)

        self.resources_bbrc = bbrc_resources

    def reorder_graphs(self):

        ordered_graphs = {}
        resources = self.get_resource_details(self.resources_bbrc)
        del resources['Version Distribution']

        ordered_graphs.update(resources)
        return ordered_graphs

    def generate_resource_df(self, resources_bbrc, test, value):

        resource_processing = []
        for resource in resources_bbrc:
            project, exp_id, archiving_validator, bv, insert_date = resource
            if archiving_validator != 0:
                if test in archiving_validator:
                    item = [project, exp_id, 'Exists',
                            archiving_validator['version'],
                            archiving_validator[test][value],
                            bv, insert_date]
                    resource_processing.append(item)
                else:
                    item = [project, exp_id, 'Exists',
                            archiving_validator['version'], 'No Data',
                            bv, insert_date]
                    resource_processing.append(item)
            else:
                item = [project, exp_id, 'Missing', 'No Data', 'No Data',
                        bv, insert_date]
                resource_processing.append(item)

        # Creates the dataframe from the list created
        columns = ['Project', 'Session', 'Archiving Valid', 'version', test,
                   'BBRC_Validators', 'Insert date']
        df = pd.DataFrame(resource_processing, columns=columns)
        return df

    def generate_bbrc_validators_dict(self, df):

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

    def get_resource_details(self, resources_bbrc, project_id=None):

        # Generating specifc resource type
        df_usable_t1 = self.generate_resource_df(
            resources_bbrc, 'HasUsableT1', 'has_passed')
        df_con_acq_date = self.generate_resource_df(
            resources_bbrc, 'IsAcquisitionDateConsistent', 'has_passed')
        columns = ['Project', 'Session', 'Archiving Valid', 'BBRC_Validators',
                   'Inserted date']
        df = pd.DataFrame(resources_bbrc, columns=columns)

        if project_id is not None:
            df_usable_t1 = df_usable_t1.groupby('Project').get_group(project_id)
            df_con_acq_date = df_con_acq_date.groupby('Project').get_group(project_id)
            df = df.groupby('Project').get_group(project_id)

        # Usable t1
        usable_t1 = self.dict_generator_resources(
            df_usable_t1, 'HasUsableT1', 'Session')
        usable_t1['id_type'] = 'experiment'

        # consisten_acq_date
        consistent_acq_date = self.dict_generator_resources(
            df_con_acq_date, 'IsAcquisitionDateConsistent', 'Session')
        consistent_acq_date['id_type'] = 'experiment'

        # Version Distribution
        version = self.dict_generator_resources(
            df_usable_t1, 'version', 'Session')
        version['id_type'] = 'experiment'

        # BBRC Validators
        bv = self.generate_bbrc_validators_dict(df)

        return {'Sessions with usable T1': usable_t1,
                'Version Distribution': version, 'BBRC validators': bv,
                'Is acquisition data consistent across the whole session?': consistent_acq_date}

    def diff_dates(self, resources_bbrc, project_id):

        if resources_bbrc is None:
            return None

        # Generate a dataframe of TestAcquisitionDate and its InsertDate
        df = self.generate_resource_df(
            resources_bbrc, 'IsAcquisitionDateConsistent', 'data')

        # Filter by project_id
        try:
            df = df.groupby(['Project']).get_group(project_id)
        except KeyError:
            return {'count': {}, 'list': {}}

        # Drop experiments with No Date information
        dates_acq_list = []
        dates_acq_dict = df[['IsAcquisitionDateConsistent']].to_dict()['IsAcquisitionDateConsistent']

        for d in dates_acq_dict:
            if 'session_date' in dates_acq_dict[d]:
                dates_acq_list.append(dates_acq_dict[d]['session_date'])
            else:
                dd = dates_acq_dict[d]
                msg = 'Invalid IsAcquisitionDateConsistent value {}'.format(dd)
                log.warning(msg)
                dates_acq_list.append('No Data')
        df['Acq date'] = dates_acq_list
        df = df[df['Acq date'] != 'No Data']

        # if DataFrame empty
        if df.empty:
            return {'count': {}, 'list': {}}

        # Create a dataframe with columns as Session, AcqDate and InsertDate
        df_acq_insert_date = df[['Session', 'Acq date', 'Insert date']]

        # Calculates the time difference
        df_acq_insert_date['Diff'] = df_acq_insert_date.apply(
            lambda x: self.dates_diff_calc(x['Acq date'], x['Insert date']), axis=1)

        # Create the dictionary: {"count": {"x": "y"}, "list": {"x": "list"}}
        df_diff = df_acq_insert_date[['Session', 'Diff']].rename(
            columns={'Session': 'count'})
        cut = pd.cut(df_diff.Diff, [0, 2, 10, 100, 1000, 10000])
        df_series = df_diff.groupby(cut)['count'].apply(list)
        df_diff = df_diff.groupby(cut).count()
        df_diff['list'] = df_series
        df_diff.index = df_diff.index.astype(str) + ' days'

        return df_diff.to_dict()

    def dates_diff_calc(self, date_1, date_2):
        """This method calculates different between 2 dates strings.

        This method takes 2 date string, converts them in datetime
        object and calculate the difference between the 2 date in days
        unit.

        Args:
            date_1 (str): Date string of date 1.
            date_2 (str): Date string of date 2.

        Returns:
            int: Difference in days.
        """
        # Calculates difference between 2 dates
        date_1_l = list(map(int, date_1.split('-')))
        date_2_l = list(map(int, date_2.split('-')))

        d1 = date(date_1_l[0], date_1_l[1], date_1_l[2])
        d2 = date(date_2_l[0], date_2_l[1], date_2_l[2])
        diff = d1 - d2

        return abs(diff.days)

    def generate_test_grid_bbrc(self, resources_bbrc, project_id):

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
            if bv and project == project_id and archiving_validator != 0:
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
                        all_dic[test].append(['', ''])

        df_info = pd.DataFrame(info_dic)
        df_cat = pd.DataFrame(cat_dic)
        df_all = pd.DataFrame(all_dic)
        return df_all, df_info, df_cat


class DataFilterPP(BBRCDataFilter):
    def __init__(self, resources, project_id):
        self.project_id = project_id
        self.resources_bbrc = [e for e in resources if len(e) > 4]

    def reorder_graphs_pp(self):

        ordered_graphs = {}

        resources = self.get_resource_details(self.resources_bbrc,
                                              self.project_id)
        ordered_graphs.update(resources)

        test_grid = self.generate_test_grid_bbrc(self.resources_bbrc,
                                                 self.project_id)
        ordered_graphs.update({'test_grid': test_grid})

        dd = self.diff_dates(self.resources_bbrc, self.project_id)
        d = {'Dates difference (Acquisition date - Insertion date)': dd}
        ordered_graphs.update(d)

        return ordered_graphs
