from datetime import date
import pandas as pd
from xnat_dashboards.data_cleaning import data_formatter
import urllib3

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
        # Resource with index 1 represent Session ID
        # Resource with index 0 represent Project ID

        for resource in resources_bbrc:
            # Resource with index 2 represent BBRC Validator
            # Resource with index 3 represent data from tests that is
            # whether a dict or 0, if 0 is present then test for the
            # sessions are not present
            if resource[3] != 0:
                if test in resource[3]:
                    resource_processing.append([
                        resource[0], resource[1], resource[2], 'Exists',
                        resource[3]['version'], resource[3][test][value]])
                else:
                    resource_processing.append([
                        resource[0], resource[1], resource[2], 'Exists',
                        resource[3]['version'], 'No Data'])
            else:
                resource_processing.append([
                    resource[0], resource[1], resource[2], 'Not Exists',
                    'No Data', 'No Data'])

        # Creates the dataframe from the list created
        df = pd.DataFrame(
            resource_processing,
            columns=[
                'Project', 'Session', 'bbrc exists',
                'Archiving Valid', 'version', test])

        return df

    def get_free_surfer_resources(self, resources_bbrc):
        """A method that generates dataframe form freesurfer
        of BBRC resources.

        Args:
            resources_bbrc (list): List of BBRC resource

        Returns:
            Dataframe: A pandas dataframe with each row showing
            the free surfer resources information.
        """
        resource_processing = []
        # Resource with index 1 represent Session ID
        # Resource with index 0 represent Project ID

        for resource in resources_bbrc:
            # Resource with index 5 represent whether free surfer
            # resource is present if -1 is present then free surfer
            # resource for the session is not present
            if resource[5] is not None:
                resource_processing.append([
                    resource[0], resource[1],
                    resource[4], float(resource[5][:-1])])
            else:
                resource_processing.append([
                    resource[0], resource[1], resource[4], 'No Data'])

        # Creates the dataframe from the list created
        df = pd.DataFrame(
            resource_processing,
            columns=[
                'Project', 'Session', 'FreeSurfer',
                'time diff'])

        return df

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
        df_free_surfer = self.get_free_surfer_resources(resources_bbrc)

        if project_id is not None:

            try:

                df_usable_t1 = df_usable_t1.groupby(
                    'Project').get_group(project_id)
                df_con_acq_date = df_con_acq_date.groupby(
                    'Project').get_group(project_id)
                df_free_surfer = df_free_surfer.groupby(
                    'Project').get_group(project_id)

            except KeyError:

                return -1

        # Usable t1
        usable_t1 = data_formatter.Formatter().dict_generator_resources(
            df_usable_t1, 'HasUsableT1', 'Session')
        usable_t1['id_type'] = 'experiment'

        # consisten_acq_date
        consistent_acq_date = data_formatter.Formatter().\
            dict_generator_resources(
            df_con_acq_date, 'IsAcquisitionDateConsistent', 'Session')
        consistent_acq_date['id_type'] = 'experiment'

        # Archiving validator
        archiving_valid = data_formatter.Formatter().dict_generator_resources(
            df_usable_t1, 'Archiving Valid', 'Session')
        archiving_valid['id_type'] = 'experiment'

        # Version Distribution
        version = data_formatter.Formatter().dict_generator_resources(
            df_usable_t1, 'version', 'Session')
        version['id_type'] = 'experiment'

        # BBRC resource exist
        bbrc_exists = data_formatter.Formatter().dict_generator_resources(
            df_usable_t1, 'bbrc exists', 'Session')
        bbrc_exists['id_type'] = 'experiment'

        # Free surfer exists
        free_surfer_exists = data_formatter.Formatter().\
            dict_generator_resources(df_free_surfer, 'FreeSurfer', 'Session')
        free_surfer_exists['id_type'] = 'experiment'

        time_diff = df_free_surfer[
            df_free_surfer['time diff'] != 'No Data'].rename(
                columns={'time diff': 'count'}).set_index(
                'Session').to_dict()

        list_se = df_free_surfer[
            df_free_surfer['time diff'] != 'No Data']['Session'].to_list()
        time_diff['list'] = {key: [key] for key in list_se}

        time_diff['id_type'] = 'experiment'

        return {'UsableT1': usable_t1,
                'Archiving Validator': archiving_valid,
                'Version Distribution': version, 'BBRC validator': bbrc_exists,
                'Consistent Acquisition Date': consistent_acq_date,
                'Free Surfer': free_surfer_exists,
                'Freesurfer end and start hour difference': time_diff}

    def diff_dates(self, resources_bbrc, experiments_data, project_id):
        """Method for Creating Acquisition and insertion dates difference plot.

        It takes 2 dates, one from resource test (acquisition date) and
        another from experiment insert date. It calculates the difference
        between 2 dates and plot graph for each difference and its
        corresponding experiments

        Args:
            resources_bbrc (list): List of bbrc resources.
            experiments_data (list): list of experiments details

        Returns:
            dict: {"count": {"x": "y"}, "list": {"x": "list"}}
        """
        # Create dict format for graph of difference in dates
        experiments = []

        # Get list of experiments
        for experiment in experiments_data:
            if experiment['project'] == project_id:
                experiments.append(experiment)

        if resources_bbrc is None:
            return None

        # Generate a dataframe of Test acq. date and its data (date)
        df = self.generate_resource_df(
            resources_bbrc, 'IsAcquisitionDateConsistent', 'data')

        try:
            df = df.groupby(['Project']).get_group(project_id)
        except KeyError:
            return {'count': {}, 'list': {}}

        df_exp = pd.DataFrame(experiments)

        # Perform a join operation on Experiment ID and Session(Experiment ID)
        merged_inner = pd.merge(
            left=df, right=df_exp, left_on='Session', right_on='ID')

        # Dates acq dict {'IsAcquisitionDateConsistent':{'session_date': date}}
        # below code get the date from the dictionary

        dates_acq_list = []
        dates_acq_dict = merged_inner[
            ['IsAcquisitionDateConsistent']].to_dict()[
                'IsAcquisitionDateConsistent']

        for dates in dates_acq_dict:
            if 'session_date' in dates_acq_dict[dates]:
                dates_acq_list.append(dates_acq_dict[dates]['session_date'])
            else:
                dates_acq_list.append(dates_acq_dict[dates])

        # Acquisition date extracted from dict and added to dataframe

        merged_inner['acq_date'] = dates_acq_list

        # Creates a dataframe with columns as ID, Acq. date and insert date
        df_acq_insert_date = merged_inner[['ID', 'acq_date', 'date']]

        df_acq_insert_date['diff'] = df_acq_insert_date.apply(
            lambda x: self.dates_diff_calc(x['acq_date'], x['date']), axis=1)

        diff_test = df_acq_insert_date[['ID', 'diff']].rename(
            columns={'ID': 'count'})
        per_df_series = diff_test.groupby('diff')['count'].apply(list)
        per_df = diff_test.groupby('diff').count()
        per_df['list'] = per_df_series

        per_df = per_df.rename(columns={'diff': 'Difference in dates'})
        per_df.index = per_df.index.astype(str) + ' days'

        return per_df.to_dict()

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
        if date_1 == 'No Data':
            return 'No Data'
        else:
            date_1_l = list(map(int, date_1.split('-')))
            date_2_l = list(map(int, date_2.split('-')))

            diff = date(
                date_1_l[0], date_1_l[1], date_1_l[2])\
                - date(date_2_l[0], date_2_l[1], date_2_l[2])

            return diff.days

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

            if resource[2] and not isinstance(resource[3], int):

                for test in resource[3]:
                    if test not in tests_union\
                        and\
                            test not in extra:
                        tests_union.append(test)

        # If resource[2] ie BBRC_Validator exists then further proceed
        # For resource[3] which is a dict of tests
        for resource in resources_bbrc:

            if resource[2] and not isinstance(resource[3], int):
                test_list = []
                test_list = [resource[1]]

                test_list.append(['version', resource[3]['version']])

                # Loop through each test if exists then add the details
                # in the tests_list or just add '' in the test_list
                for test in tests_union:
                    test_unit = ''

                    if test in resource[3]:
                        test_unit = [resource[
                            3][test]['has_passed'],
                            resource[
                            3][test]['data']]

                    test_list.append(test_unit)

                if resource[0] == project_id:
                    tests_list.append(test_list)

        # Create a list of different version of tests that are present
        # this diff_version list is used in the filtering of test grid
        diff_version = []

        for td_v in tests_list:
            if td_v[1][1] not in diff_version:
                diff_version.append(td_v[1][1])

        return [tests_union, tests_list, diff_version]
