from datetime import date
import pandas as pd
from dashboards.data_cleaning import data_formatter
import urllib3
import logging as log

# Remove warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
pd.options.mode.chained_assignment = None


class Formatter:
    """Formatting Class.

    This class contains method that are used for formatting the
    BBRC resources data fetched from the pickle and sent to DataFilter class

    """

    def generate_resource_df(self, resources_bbrc, test, value):
        """A method that generates dataframe from BBRC Validator
        and Archiving Validator of BBRC resources.

        Args:
            resources_bbrc (list): List of BBRC resource
            test (str): Test name we want to generate df
            value (str): key inside test dict

        Returns:
            Dataframe: A pandas dataframe with each row showing whether
            the test has passed, failed or No information regarding test
        """
        resource_processing = []
        for resource in resources_bbrc:
            project, exp_id, archiving_validator, bbrc_validators, insert_date = resource
            if archiving_validator != 0:
                if test in archiving_validator:
                    resource_processing.append([
                        project, exp_id, 'Exists',
                        archiving_validator['version'], archiving_validator[test][value], bbrc_validators, insert_date])
                else:
                    resource_processing.append([
                        project, exp_id, 'Exists',
                        archiving_validator['version'], 'No Data', bbrc_validators, insert_date])
            else:
                resource_processing.append([
                    project, exp_id, 'Missing',
                    'No Data', 'No Data', bbrc_validators, insert_date])

        # Creates the dataframe from the list created
        df = pd.DataFrame(
            resource_processing,
            columns=[
                'Project', 'Session', 'Archiving Valid',
                'version', test, 'BBRC_Validators', 'Insert date'])

        return df

    def generate_bbrc_validators_dict(self, df):

        bbrc_validators = {'count': {}, 'list': {}}
        series = pd.Series([x for _list in df['BBRC_Validators'] for x in _list])
        series_dict = (series.value_counts()).to_dict()
        for k, v in series_dict.items():
            bbrc_validators['count'][k] = {}
            bbrc_validators['count'][k]['Sessions with Validator'] = v
            list_ = df[pd.DataFrame(df.BBRC_Validators.tolist()).isin([k]).any(1).values]
            ses = pd.Series([x for x in list_['Session']])
            bbrc_validators['list'][k] = {}
            bbrc_validators['list'][k]['Sessions with Validator'] = list(ses)
            missing_ses = []
            for s in df['Session']:
                if s not in list(ses):
                    missing_ses.append(s)
            bbrc_validators['count'][k]['Sessions wihtout Validator'] = len(missing_ses)
            bbrc_validators['list'][k]['Sessions without Validator'] = missing_ses
        return bbrc_validators

    def get_resource_details(self, resources_bbrc, project_id=None):
        """
        This method process the resources that are saved as in pickle file.
        it generates the required format for each plot.

        Args:
            resources_bbrc ( list): Each resource have its corresponding
                ID, project ID, label and experiment id.
            project_id (String, optional): For per project view, the project id
                by default it will not return any project details.

        Returns:
            dict/int: If resource exist then a dict with the corresponding data
                else -1.

            For each graph this format is used
            {"count": {"x": "y"}, "list": {"x": "list"}}
        """
        # Generating specifc resource type
        df_usable_t1 = self.generate_resource_df(
            resources_bbrc, 'HasUsableT1', 'has_passed')
        df_con_acq_date = self.generate_resource_df(
            resources_bbrc, 'IsAcquisitionDateConsistent', 'has_passed')
        df = pd.DataFrame(resources_bbrc, columns=['Project', 'Session',
                                                   'Archiving Valid', 'BBRC_Validators', 'Inserted date'])

        if project_id is not None:

            try:

                df_usable_t1 = df_usable_t1.groupby(
                    'Project').get_group(project_id)
                df_con_acq_date = df_con_acq_date.groupby(
                    'Project').get_group(project_id)
                df = df.groupby(
                    'Project').get_group(project_id)

            except KeyError:

                return -1

        # Usable t1
        usable_t1 = data_formatter.Formatter().dict_generator_resources(
            df_usable_t1, 'HasUsableT1', 'Session')
        usable_t1['id_type'] = 'experiment'

        # consisten_acq_date
        consistent_acq_date = data_formatter.Formatter(). \
            dict_generator_resources(
            df_con_acq_date, 'IsAcquisitionDateConsistent', 'Session')
        consistent_acq_date['id_type'] = 'experiment'

        # Version Distribution
        version = data_formatter.Formatter().dict_generator_resources(
            df_usable_t1, 'version', 'Session')
        version['id_type'] = 'experiment'

        # BBRC Validators
        bbrc_validators = self.generate_bbrc_validators_dict(df)

        return {'Sessions with usable T1': usable_t1,
                'Version Distribution': version, 'BBRC validators': bbrc_validators,
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
        dates_acq_dict = df[
            ['IsAcquisitionDateConsistent']].to_dict()['IsAcquisitionDateConsistent']
        for date in dates_acq_dict:
            if 'session_date' in dates_acq_dict[date]:
                dates_acq_list.append(dates_acq_dict[date]['session_date'])
            else:
                log.warning('Invalid IsAcquisitionDateConsistent value {}'.format(dates_acq_dict[date]))
                dates_acq_list.append('No Data')
        df['Acq date'] = dates_acq_list
        df = df[df['Acq date'] != 'No Data']

        # if DataFrame empty
        if df.empty == True:
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

        diff = date(
            date_1_l[0], date_1_l[1], date_1_l[2]) \
               - date(date_2_l[0], date_2_l[1], date_2_l[2])

        return abs(diff.days)

    def generate_test_grid_bbrc(self, resources_bbrc, project_id):
        """This method is used to create the data for the
        test grid.

        Args:
            resources_bbrc (list): BBRC resource for each experiments

        Returns:
            list: Generates a list where each session have a all
            test details and version information
        """
        if resources_bbrc is None:
            return [[], []]

        tests_list = []
        extra = ['version', 'experiment_id', 'generated']
        tests_union = []

        # Creates a tests_unions list which has all tests union
        # except the values present in extra list
        for resource in resources_bbrc:
            project, exp_id, archiving_validator, bbrc_validators, insert_date = resource
            if bbrc_validators and not isinstance(archiving_validator, int):

                for test in archiving_validator:
                    if test not in tests_union \
                            and \
                            test not in extra:
                        tests_union.append(test)

        # If bbrc_validator exists then further proceed
        # for archiving_validator which is a dict of tests
        for resource in resources_bbrc:
            project, exp_id, archiving_validator, bbrc_validators, insert_date = resource
            if bbrc_validators and not isinstance(archiving_validator, int):
                test_list = [exp_id, ['version', archiving_validator['version']]]

                # Loop through each test if exists then add the details
                # in the tests_list or just add '' in the test_list
                for test in tests_union:
                    test_unit = ''

                    if test in archiving_validator:
                        test_unit = [archiving_validator[test]['has_passed'],
                                     archiving_validator[test]['data']]

                    test_list.append(test_unit)

                if project == project_id:
                    tests_list.append(test_list)

        # Create a list of different version of tests that are present
        # this diff_version list is used in the filtering of test grid
        diff_version = []

        for td_v in tests_list:
            if td_v[1][1] not in diff_version:
                diff_version.append(td_v[1][1])

        return [tests_union, tests_list, diff_version]
