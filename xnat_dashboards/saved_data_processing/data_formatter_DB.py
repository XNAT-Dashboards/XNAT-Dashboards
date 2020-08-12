import pandas as pd
import re
from datetime import date


class Formatter:

    # Initializing the central interface object in the constructor
    def __init__(self, username):

        self.name = username

    def get_projects_details(self, projects):

        if type(projects) == int:
            return projects

        projects_details = {}

        project_acccess = self.dict_generator_overview(
            projects, 'project_access', 'id', 'access')
        project_acccess['id_type'] = 'project'

        projects_details['Number of Projects'] = len(projects)
        projects_details['Projects Visibility'] = project_acccess

        return projects_details

    def get_subjects_details(self, subjects_data):

        if type(subjects_data) == int:
            return subjects_data

        subjects_details = {}

        # Subject age information

        age_list = []
        age_none = []

        for subject in subjects_data:
            if subject['age'] != '':
                if int(subject['age']) > 0 and int(subject['age']) < 130:
                    age_list.append([int(subject['age']), subject['ID']])
                else:
                    age_none.append(subject['ID'])
            else:
                age_none.append(subject['ID'])

        age_df = pd.DataFrame(age_list, columns=['age', 'count'])

        age_df['age'] = pd.cut(
            x=age_df['age'],
            bins=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 130],
            labels=['0-10', '10-20', '20-30', '30-40', '40-50', '50-60',
                    '60-70', '70-80', '80-90', '90-100', 'Above_100'])

        age_ranged = age_df.groupby('age')['count'].apply(list)
        age_final_df = age_df.groupby('age').count()
        age_final_df['list'] = age_ranged

        age_range = age_final_df.to_dict()

        age_range['count'].update({'No Data': len(age_none)})
        age_range['list'].update({'No Data': age_none})
        age_range['id_type'] = 'subject'
        # Age end

        # Subject handedness information

        handedness = self.dict_generator_overview(
            subjects_data, 'handedness', 'ID', 'handedness')
        handedness['id_type'] = 'subject'

        # Subject gender information

        gender = self.dict_generator_overview(
            subjects_data, 'gender', 'ID', 'gender')
        gender['id_type'] = 'subject'

        # Subjects per project information

        subjects_per_project = self.dict_generator_per_view(
            subjects_data, 'project', 'ID', 'spp')
        subjects_per_project['id_type'] = 'subject'

        # Number of subjects information
        subjects_details['Number of Subjects'] = len(subjects_data)

        subjects_details['Subjects/Project'] = subjects_per_project
        subjects_details['Age Range'] = age_range
        subjects_details['Gender'] = gender
        subjects_details['Handedness'] = handedness

        return subjects_details

    def get_experiments_details(self, experiments):

        if type(experiments) == int:
            return experiments

        experiments_details = {}

        experiments_details['Number of Experiments'] = len(experiments)

        # Experiments per project information

        experiments_per_project = self.dict_generator_per_view(
            experiments, 'project', 'ID', 'epp')
        experiments_per_project['id_type'] = 'experiment'

        # Experiments type information

        experiment_type = self.dict_generator_overview(
            experiments, 'xsiType', 'ID', 'xsiType')
        experiment_type['id_type'] = 'experiment'

        # Experiments per subject information

        experiments_per_subject = self.dict_generator_per_view(
            experiments, 'subject_ID', 'ID', 'eps')
        experiments_per_subject['id_type'] = 'experiment'

        experiments_types_per_project = self.dict_generator_per_view_stacked(
            experiments, 'project', 'xsiType', 'ID')
        experiments_types_per_project['id_type'] = 'experiment'

        experiments_details['Sessions types/Project'] =\
            experiments_types_per_project

        experiments_details['Experiments/Subject'] = experiments_per_subject
        experiments_details['Experiment Types'] = experiment_type
        experiments_details['Experiments/Project'] = experiments_per_project

        return experiments_details

    def get_scans_details(self, scans):

        if type(scans) == int:
            return scans

        scan_quality = self.dict_generator_overview(
            scans, 'xnat:imagescandata/quality', 'ID',
            'quality', 'xnat:imagescandata/id')
        scan_quality['id_type'] = 'experiment'

        # Scans type information

        type_dict = self.dict_generator_overview(
            scans, 'xnat:imagescandata/type',
            'ID', 'type', 'xnat:imagescandata/id')
        type_dict['id_type'] = 'experiment'

        # Scans xsi type information

        xsi_type_dict = self.dict_generator_overview(
            scans, 'xsiType', 'ID', 'xsiType', 'xnat:imagescandata/id')
        xsi_type_dict['id_type'] = 'experiment'

        # Scans per project information

        scans_per_project = self.dict_generator_overview(
            scans, 'project', 'ID', 'spp', 'xnat:imagescandata/id')
        scans_per_project['id_type'] = 'experiment'

        # Scans per subject information

        scans_per_subject = self.dict_generator_overview(
            scans, 'xnat:imagesessiondata/subject_id',
            'ID', 'sps', 'xnat:imagescandata/id')
        scans_per_subject['id_type'] = 'experiment'

        scans_details = {}

        scans_details['Scans Quality'] = scan_quality
        scans_details['Scan Types'] = type_dict
        scans_details['XSI Scan Types'] = xsi_type_dict
        scans_details['Scans/Project'] = scans_per_project
        scans_details['Scans/Subject'] = scans_per_subject
        scans_details['Number of Scans'] = len(scans)

        return scans_details

    def get_projects_details_specific(self, projects):

        '''
        This method reuturn 2 list
        List of projects visible
        List of project where user is owner, collab or member
        '''

        if projects is None:
            return 1

        project_list_owned_collab_member = []

        for project in projects:
            project_owner = project['project_owners']
            project_collabs = project['project_collabs']
            project_member = project['project_members']
            user = self.name

            if project_owner.find(user) != -1\
               or project_collabs.find(user) != -1\
               or project_member.find(user) != -1:
                project_list_owned_collab_member.append(project['id'])

        project_list_all = [project['id'] for project in projects]

        list_data = {}
        list_data['project_list'] = project_list_all
        list_data['project_list_ow_co_me'] = project_list_owned_collab_member

        '''
        Return type is dict
        '''

        return list_data

    def get_resources_details(
            self, resources=None, resources_bbrc=None, project_id=None):

        '''
        Returns details about resource for each session as well as
        if bbrc resources exist then that resources details as well
        '''

        if resources is None:
            return None

        df = pd.DataFrame(
            resources,
            columns=['project', 'session', 'resource', 'label'])

        if project_id is not None:   # Code for per project view

            try:

                df = df.groupby(['project']).get_group(project_id)

            except KeyError:

                return -1

        df['resource'] = df['resource'].map(
            lambda x: re.sub('<Resource Object>', 'Resource Object', str(x)))

        resource_pp = df[df['resource'] != 'No Data'][['project', 'resource']]
        session = df[df['resource'] != 'No Data']['session']
        resource_pp['resource'] = session + '/' + resource_pp['resource']
        resource_pp = resource_pp.rename(columns={'resource': 'count'})
        resources_pp_df = resource_pp.groupby('project')['count'].apply(list)
        resource_pp = resource_pp.groupby('project').count()
        resource_pp['list'] = resources_pp_df
        resource_pp = resource_pp.to_dict()
        resource_pp['id_type'] = 'experiment'
        res_pp_no_data = df[
            df['resource'] == 'No Data'].groupby('project').count()

        no_data_rpp = res_pp_no_data.index.difference(
            resources_pp_df.index).to_list()

        if len(no_data_rpp) != 0:
            no_data_update = {}

            for item in no_data_rpp:
                no_data_update[item] = 0

            resource_pp['count'].update(no_data_update)

        # Resource types
        resource_types = self.dict_generator_resources(df, 'label', 'session')
        resource_types['id_type'] = 'experiment'

        resource_type_ps = self.dict_generator_resources(
            df, 'label', 'session')
        resource_type_ps['id_type'] = 'experiment'

        if resources_bbrc is None:

            return {
                'Resources/Project': resource_pp,
                'Resource Types': resource_types}

        # Generating specifc resource type
        df_usable_t1 = self.generate_resource_df(
            resources_bbrc, 'HasUsableT1', 'has_passed')
        df_con_acq_date = self.generate_resource_df(
            resources_bbrc, 'IsAcquisitionDateConsistent', 'has_passed')

        if project_id is not None:

            try:

                df_usable_t1 = df_usable_t1.groupby(
                    'Project').get_group(project_id)
                df_con_acq_date = df_con_acq_date.groupby(
                    'Project').get_group(project_id)

            except KeyError:

                return -1

        # Usable t1
        usable_t1 = self.dict_generator_resources(
            df_usable_t1, 'HasUsableT1', 'Session')
        usable_t1['id_type'] = 'experiment'

        # consisten_acq_date
        consistent_acq_date = self.dict_generator_resources(
            df_con_acq_date, 'IsAcquisitionDateConsistent', 'Session')
        consistent_acq_date['id_type'] = 'experiment'

        # Archiving validator
        archiving_valid = self.dict_generator_resources(
            df_usable_t1, 'Archiving Valid', 'Session')
        archiving_valid['id_type'] = 'experiment'

        # Version Distribution
        version = self.dict_generator_resources(
            df_usable_t1, 'version', 'Session')
        version['id_type'] = 'experiment'

        # BBRC resource exist
        bbrc_exists = self.dict_generator_resources(
            df_usable_t1, 'bbrc exists', 'Session')
        bbrc_exists['id_type'] = 'experiment'

        return {'Resources/Project': resource_pp,
                'Resource Types': resource_types, 'UsableT1': usable_t1,
                'Archiving Validator': archiving_valid,
                'Version Distribution': version, 'BBRC validator': bbrc_exists,
                'Sessions/Resource type': resource_type_ps,
                'Consistent Acquisition Date': consistent_acq_date}

    def generate_resource_df(self, resources_bbrc, test, value):

        '''
        A method that generates dataframe.
        This first takes bbrc resources and run test method on those
        reources, these test are specific to
        bbrc (Barcelona beta) pyxnat branch
        '''

        resource_processing = []

        for resource in resources_bbrc:

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

        df = pd.DataFrame(
            resource_processing,
            columns=[
                'Project', 'Session', 'bbrc exists',
                'Archiving Valid', 'version', test])

        return df

    def dict_generator_resources(self, df, x_name, y_name):

        '''
        Generate dict format from dataframe that is used by plotly,
        takes resources df as input and returns dict
        x_name denotes the property that will be plotted on x axis
        and y_name which will be plotted on y axis
        '''

        data = df[df[y_name] != 'No Data'][[
            x_name, y_name]]
        data = data.rename(columns={y_name: 'count'})
        data_df = data.groupby(
            x_name)['count'].apply(list)
        data = data.groupby(x_name).count()
        data['list'] = data_df
        data_dict = data.to_dict()

        '''
        {
            count:{x:y},
            list:{x:y_list}
        }
        '''

        return data_dict

    def dict_generator_overview(
            self, data, property_x, property_y, x_new, extra=None):

        '''
        Generate dict format that is used by plotly takes, data like
        project details, scan, experiments, subject as field
        property_x denotes the property that will be plotted on x axis
        and property y which will be plotted on y axis
        '''

        property_list = []
        property_none = []

        for item in data:
            if item[property_x] != '':
                if extra is None:
                    property_list.append([item[property_x], item[property_y]])
                else:
                    property_list.append(
                        [
                            item[property_x],
                            item[property_y] + '/' + item[extra]])
            else:
                if extra is None:
                    property_none.append(item[property_y])
                else:
                    property_none.append(item[property_y] + '/' + item[extra])

        property_df = pd.DataFrame(
            property_list, columns=[x_new, 'count'])

        property_df_series = property_df.groupby(
            x_new)['count'].apply(list)
        property_final_df = property_df.groupby(x_new).count()
        property_final_df['list'] = property_df_series
        property_dict = property_final_df.to_dict()

        if len(property_none) != 0:
            property_dict['count'].update({'No Data': len(property_none)})
            property_dict['list'].update({'No Data': property_none})

        '''
        {
            count:{x:y},
            list:{x:y_list}
        }
        '''

        return property_dict

    def dict_generator_per_view(
            self, data, property_x, property_y, x_new):

        '''
        Generate dict format that is used by plotly for per project view,
        data like project details, scan, experiments, subject as field
        property_x denotes the property that will be plotted on x axis
        and property y which will be plotted on y axis
        '''

        per_list = []

        for item in data:
            per_list.append([item[property_x], item[property_y]])

        per_df = pd.DataFrame(per_list, columns=[x_new, 'count'])
        per_df_series = per_df.groupby(x_new)['count'].apply(list)
        per_df = per_df.groupby(x_new).count()
        per_df['list'] = per_df_series

        per_view = per_df.to_dict()

        '''
        {
            count:{x:y},
            list:{x:y_list}
        }
        '''

        return per_view

    def dict_generator_per_view_stacked(
            self, data, property_x, property_y, property_z):

        '''
        Generate dict format that is used by plotly for stacked graphs view,
        data like project details, scan, experiments, subject as field
        example:
        Graph Session types per project:
        property_x = project
        property_y = xsiType
        property_z = ID

        x_axis is project, y are the stacked count of property y based
        on property_z
        '''

        per_list = []

        for item in data:
            per_list.append(
                [item[property_x], item[property_y], item[property_z]])

        per_df = pd.DataFrame(
            per_list, columns=[property_x, property_y, property_z])

        per_df_series = per_df.groupby(
            [property_x, property_y])[property_z].apply(list)

        per_df = per_df.groupby([property_x, property_y]).count()
        per_df['list'] = per_df_series

        dict_tupled = per_df.to_dict()

        dict_output_list = {}
        for item in dict_tupled['list']:
            dict_output_list[item[0]] = {}

        for item in dict_tupled['list']:
            dict_output_list[
                item[0]].update({item[1]: dict_tupled['list'][item]})

        dict_output_count = {}

        for item in dict_tupled[property_z]:
            dict_output_count[item[0]] = {}

        for item in dict_tupled[property_z]:
            dict_output_count[
                item[0]].update({item[1]: dict_tupled[property_z][item]})

        '''
        {
            count:{prop_x:{prop_y:prop_z_count}},
            list:{prop_x:{prop_y:prop_z_list}}
        }
        '''
        return {'count': dict_output_count, 'list': dict_output_list}


class FormatterPP(Formatter):

    # Initializing the central interface object in the constructor
    def __init__(self, username, project_id):

        self.name = username
        self.project_id = project_id

    def get_projects_details(self, projects):

        # Returns data for per project view

        project_dict = {}

        for project in projects:

            if project['id'] == self.project_id:
                project_dict = project

        project_details = {}

        project_details['Owner(s)'] = project_dict['project_owners']\
            .split('<br/>')

        project_details['Collaborator(s)'] = project_dict['project_collabs']\
            .split('<br/>')
        if project_details['Collaborator(s)'][0] == '':
            project_details['Collaborator(s)'] = ['------']

        project_details['member(s)'] = project_dict['project_members']\
            .split('<br/>')
        if project_details['member(s)'][0] == '':
            project_details['member(s)'] = ['------']

        project_details['user(s)'] = project_dict['project_users']\
            .split('<br/>')
        if project_details['user(s)'][0] == '':
            project_details['user(s)'] = ['------']

        project_details['last_accessed(s)'] =\
            project_dict['project_last_access'].split('<br/>')

        project_details['insert_user(s)'] = project_dict['insert_user']

        project_details['insert_date'] = project_dict['insert_date']
        project_details['access'] = project_dict['project_access']
        project_details['name'] = project_dict['name']

        project_details['last_workflow'] =\
            project_dict['project_last_workflow']

        return project_details

    def get_subjects_details(self, subjects):

        subjects_data = []

        for subject in subjects:
            if subject['project'] == self.project_id:
                subjects_data.append(subject)

        # Using code from the parent class for processing
        subjects_details = super().get_subjects_details(subjects_data)
        del subjects_details['Subjects/Project']
        # Delete project information

        return subjects_details

    def get_experiments_details(self, experiments_data):

        experiments = []

        for experiment in experiments_data:
            if experiment['project'] == self.project_id:
                experiments.append(experiment)

        # Using code from the parent class for processing
        experiments_details = super().get_experiments_details(experiments)
        del experiments_details['Experiments/Project']
        # Delete project information

        return experiments_details

    def get_scans_details(self, scans_data):

        scans = []

        for scan in scans_data:
            if scan['project'] == self.project_id:
                scans.append(scan)

        # Using code from the parent class for processing
        scans_details = super().get_scans_details(scans)
        del scans_details['Scans/Project']
        # Delete project information

        return scans_details

    def get_resources_details(self, resources=None, resources_bbrc=None):

        if resources is None:
            return None

        # Using code from the parent class for processing
        resources_out = super().get_resources_details(
            resources, resources_bbrc, self.project_id)

        if type(resources_out) != int and 'Resources/Project' in resources_out:
            del resources_out['Resources/Project']

        return resources_out

    def diff_dates(self, resources_bbrc, experiments_data):

        # Create dict format for graph of difference in dates
        experiments = []

        # Get list of experiments
        for experiment in experiments_data:
            if experiment['project'] == self.project_id:
                experiments.append(experiment)

        if resources_bbrc is None:
            return None

        # Generate a dataframe of Test acq. date and its data (date)
        df = super().generate_resource_df(
            resources_bbrc, 'IsAcquisitionDateConsistent', 'data')

        df = df.groupby(['Project']).get_group(self.project_id)
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

        # Code to formate the dataframe for frontend
        df_diff = df_acq_insert_date

        diff_test = df_diff[['ID', 'diff']].rename(
            columns={'ID': 'count'})
        per_df_series = diff_test.groupby('diff')['count'].apply(list)
        per_df = diff_test.groupby('diff').count()
        per_df['list'] = per_df_series

        per_df = per_df.rename(columns={'diff': 'Difference in dates'})
        per_df.index = per_df.index.astype(str) + ' days'

        return per_df.to_dict()

    def dates_diff_calc(self, date_1, date_2):

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

    def generate_test_grid_bbrc(self, resources_bbrc):

        if resources_bbrc is None:
            return [[], []]

        tests_list = []
        extra = ['version', 'experiment_id', 'generated']
        tests_union = []

        # Creates a tests_unions list which has all tests union
        # except the values present in extra list
        for resource in resources_bbrc:

            if resource[2] == 'Exists' and type(resource[3]) != int:

                for test in resource[3]:
                    if test not in tests_union\
                        and\
                            test not in extra:
                        tests_union.append(test)

        # If resource[2] ie BBRC_Validator exists then further proceed
        # For resource[3] which is a dict of tests
        for resource in resources_bbrc:

            if resource[2] == 'Exists' and type(resource[3]) != int:
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

                if resource[0] == self.project_id:
                    tests_list.append(test_list)

        return [tests_union, tests_list]
