import socket
import pandas as pd
import re


class Formatter:

    # Initializing the central interface object in the constructor
    def __init__(self, username):

        self.name = username

    def get_projects_details(self, projects):

        if type(projects) == int:
            return projects

        projects_details = {}
        projects_ims = {}
        project_acccess = {}
        mr_sessions_per_project = {}
        ct_sessions_per_project = {}
        pet_sessions_per_project = {}
        ut_sessions_per_project = {}

        access_list = []
        access_none = []

        for project in projects:
            if project['project_access'] != '':
                access_list.append([project['project_access'], project['id']])
            else:
                access_none.append(project['id'])

        access_df = pd.DataFrame(access_list, columns=['access', 'count'])
        access_df_series = access_df.groupby('access')['count'].apply(list)
        access_final_df = access_df.groupby('access').count()
        access_final_df['list'] = access_df_series
        project_acccess = access_final_df.to_dict()
        project_acccess['count'].update({'No Data': len(access_none)})
        project_acccess['list'].update({'No Data': access_none})

        projects_ims['CT Sessions'] = sum([int(project['proj_ct_count'])
                                           for project in projects
                                           if project['proj_ct_count'] != ''])
        projects_ims['PET Sessions'] = sum([int(project['proj_pet_count'])
                                            for project in projects
                                            if project['proj_pet_count'] != ''
                                            ])
        projects_ims['MR Sessions'] = sum([int(project['proj_mr_count'])
                                           for project in projects
                                           if project['proj_mr_count'] != ''])
        projects_ims['UT Sessions'] = sum([int(project['proj_ut_count'])
                                           for project in projects
                                           if project['proj_ut_count'] != ''])

        for item in projects:

            if item['proj_mr_count'] != '':
                mr_sessions_per_project[item['id']] =\
                    int(item['proj_mr_count'])
            else:
                mr_sessions_per_project[item['id']] = 0

            if item['proj_pet_count'] != '':
                pet_sessions_per_project[item['id']] =\
                    int(item['proj_pet_count'])
            else:
                pet_sessions_per_project[item['id']] = 0

            if item['proj_ct_count'] != '':
                ct_sessions_per_project[item['id']] =\
                    int(item['proj_ct_count'])
            else:
                ct_sessions_per_project[item['id']] = 0

            if item['proj_ut_count'] != '':
                ut_sessions_per_project[item['id']] =\
                    int(item['proj_ut_count'])
            else:
                ut_sessions_per_project[item['id']] = 0

        projects_sessions = {}

        projects_sessions['MR Sessions/Project'] = mr_sessions_per_project
        projects_sessions['PET Sessions/Project'] = pet_sessions_per_project
        projects_sessions['CT Sessions/Project'] = ct_sessions_per_project
        projects_sessions['UT Sessions/Project'] = ut_sessions_per_project

        projects_details['Number of Projects'] = len(projects)
        projects_details['Imaging Sessions'] = {'count': projects_ims}
        projects_details['Projects Visibility'] = project_acccess
        projects_details['Sessions types/Project'] =\
            {'count': projects_sessions}

        projects_details['Total Sessions'] = projects_ims['PET Sessions']\
            + projects_ims['MR Sessions'] + projects_ims['UT Sessions']\
            + projects_ims['CT Sessions']

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

        # Age end

        # Subject handedness information

        handedness = self.dict_generator_overview(
            subjects_data, 'handedness', 'ID', 'handedness')

        # Subject gender information

        gender = self.dict_generator_overview(
            subjects_data, 'gender', 'ID', 'gender')

        # Subjects per project information

        subjects_per_project = self.dict_generator_per_view(
            subjects_data, 'project', 'ID', 'spp')

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

        # Experiments type information

        experiment_type = self.dict_generator_overview(
            experiments, 'xsiType', 'ID', 'xsiType')
        # Experiments per subject information

        experiments_per_subject = self.dict_generator_per_view(
            experiments, 'subject_ID', 'ID', 'eps')

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

        # Scans type information

        type_dict = self.dict_generator_overview(
            scans, 'xnat:imagescandata/type',
            'ID', 'type', 'xnat:imagescandata/id')

        # Scans xsi type information

        xsi_type_dict = self.dict_generator_overview(
            scans, 'xsiType', 'ID', 'xsiType', 'xnat:imagescandata/id')

        # Scans per project information

        scans_per_project = self.dict_generator_per_view(
            scans, 'project', 'ID', 'spp')

        # Scans per subject information

        scans_per_subject = self.dict_generator_per_view(
            scans, 'xnat:imagesessiondata/subject_id', 'ID', 'sps')

        scans_details = {}

        scans_details['Scans Quality'] = scan_quality
        scans_details['Scan Types'] = type_dict
        scans_details['XSI Scan Types'] = xsi_type_dict
        scans_details['Scans/Project'] = scans_per_project
        scans_details['Scans/Subject'] = scans_per_subject
        scans_details['Number of Scans'] = len(scans)

        return scans_details

    def get_projects_details_specific(self, projects):

        try:
            if projects is None:
                raise socket.error
        except socket.error:
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

        return list_data

    def get_resources_details(
            self, resources=None, resources_bbrc=None, project_id=None):

        if resources is None:
            return None

        df = pd.DataFrame(
            resources['resources'],
            columns=['project', 'session', 'resource', 'label'])

        if project_id is not None:

            try:

                df = df.groupby(['project']).get_group(project_id)

            except KeyError:

                return -1

        df['resource'] = df['resource'].map(
            lambda x: re.sub('<Resource Object>', 'Resource Object', str(x)))

        resource_pp = df[df['resource'] != 'No Data'][['project', 'resource']]
        session = df[df['resource'] != 'No Data']['session']
        resource_pp['resource'] = session + ' ' + resource_pp['resource']
        resource_pp = resource_pp.rename(columns={'resource': 'count'})
        resources_pp_df = resource_pp.groupby('project')['count'].apply(list)
        resource_pp = resource_pp.groupby('project').count()
        resource_pp['list'] = resources_pp_df
        resource_pp = resource_pp.to_dict()

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
        resource_types = self.dict_generator_resources(df, 'label', 'resource')

        resource_type_ps = self.dict_generator_resources(
            df, 'label', 'session')

        # Generating specifc resource type
        resource_processing = []

        for resource in resources_bbrc['resources_bbrc']:

            if resource[3] != 0:
                if 'HasUsableT1' in resource[3]:
                    resource_processing.append([
                        resource[0], resource[1], resource[2], 'Exists',
                        resource[3]['HasUsableT1']['has_passed'],
                        resource[3]['version']])
                else:
                    resource_processing.append([
                        resource[0], resource[1], resource[2], 'Not Exists',
                        'No Data', resource[3]['version']])
            else:
                resource_processing.append([
                    resource[0], resource[1], resource[2], 'Not Exists',
                    'No Data', 'No Data'])

        df = pd.DataFrame(
            resource_processing,
            columns=[
                'Project', 'Session', 'bbrc exists', 'Archiving Valid',
                'Has Usable T1', 'version'])

        # Usable t1
        usable_t1 = self.dict_generator_resources(
            df, 'Has Usable T1', 'Session')

        # Archiving validator
        archiving_valid = self.dict_generator_resources(
            df, 'Archiving Valid', 'Session')

        # Version Distribution
        version = self.dict_generator_resources(df, 'version', 'Session')

        # BBRC resource exist
        bbrc_exists = self.dict_generator_resources(
            df, 'bbrc exists', 'Session')

        return {'Resources/Project': resource_pp,
                'Resource Types': resource_types, 'UsableT1': usable_t1,
                'Archiving Validator': archiving_valid,
                'Version Distribution': version, 'BBRC validator': bbrc_exists,
                'Sessions/Resource type': resource_type_ps}

    def dict_generator_resources(self, df, x_name, y_name):

        data = df[df[y_name] != 'No Data'][[
            x_name, y_name]]
        data = data.rename(columns={y_name: 'count'})
        data_df = data.groupby(
            x_name)['count'].apply(list)
        data = data.groupby(x_name).count()
        data['list'] = data_df
        data_dict = data.to_dict()

        return data_dict

    def dict_generator_overview(
            self, data, property_x, property_y, x_new, extra=None):

        property_list = []
        property_none = []

        for item in data:
            if item[property_x] != '':
                if extra is None:
                    property_list.append([item[property_x], item[property_y]])
                else:
                    property_list.append(
                        [item[property_x], item[property_y]+'  '+item[extra]])
            else:
                if extra is None:
                    property_none.append(item[property_y])
                else:
                    property_none.append(item[property_y]+'  '+item[extra])

        property_df = pd.DataFrame(
            property_list, columns=[x_new, 'count'])

        property_df_series = property_df.groupby(
            x_new)['count'].apply(list)
        property_final_df = property_df.groupby(x_new).count()
        property_final_df['list'] = property_df_series
        property_dict = property_final_df.to_dict()
        property_dict['count'].update({'No Data': len(property_none)})
        property_dict['list'].update({'No Data': property_none})

        return property_dict

    def dict_generator_per_view(
            self, data, property_x, property_y, x_new):

        per_list = []

        for item in data:
            per_list.append([item[property_x], item[property_y]])

        per_df = pd.DataFrame(per_list, columns=[x_new, 'count'])
        per_df_series = per_df.groupby(x_new)['count'].apply(list)
        per_df = per_df.groupby(x_new).count()
        per_df['list'] = per_df_series

        per_view = per_df.to_dict()

        return per_view


class FormatterPP(Formatter):

    # Initializing the central interface object in the constructor
    def __init__(self, username, project_id):

        self.name = username
        self.project_id = project_id

    def get_projects_details(self, projects):

        project_dict = {}

        for project in projects:

            if project['id'] == self.project_id:
                project_dict = project

        project_details = {}

        project_details['Total Sessions'] = 0
        project_details['Imaging Sessions'] = {}
        counter_session = {'count': {}}

        if project_dict['proj_mr_count'] != '':
            counter_session['count'].update({
                'MR Sessions': int(project_dict['proj_mr_count'])})
        else:
            counter_session['count'].update({
                'MR Sessions': 0})

        if project_dict['proj_pet_count'] != '':
            counter_session['count'].update({
                'PET Sessions': int(project_dict['proj_mr_count'])})
        else:
            counter_session['count'].update({
                'PET Sessions': 0})

        if project_dict['proj_ct_count'] != '':
            counter_session['count'].update({
                'CT Sessions': int(project_dict['proj_mr_count'])})
        else:
            counter_session['count'].update({
                'CT Sessions': 0})

        if project_dict['proj_ut_count'] != '':
            counter_session['count'].update({
                'UT Sessions': int(project_dict['proj_mr_count'])})
        else:
            counter_session['count'].update({
                'UT Sessions': 0})

        project_details['Total Sessions'] =\
            counter_session['count']['UT Sessions'] +\
            counter_session['count']['PET Sessions'] +\
            counter_session['count']['CT Sessions'] +\
            counter_session['count']['MR Sessions']

        project_details['Imaging Sessions'].update(counter_session)

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

        subjects_details = super().get_subjects_details(subjects_data)
        del subjects_details['Subjects/Project']

        return subjects_details

    def get_experiments_details(self, experiments_data):

        experiments = []

        for experiment in experiments_data:
            if experiment['project'] == self.project_id:
                experiments.append(experiment)

        experiments_details = super().get_experiments_details(experiments)
        del experiments_details['Experiments/Project']

        return experiments_details

    def get_scans_details(self, scans_data):

        scans = []

        for scan in scans_data:
            if scan['project'] == self.project_id:
                scans.append(scan)

        scans_details = super().get_scans_details(scans)
        del scans_details['Scans/Project']

        return scans_details

    def get_resources_details(self, resources=None, resources_bbrc=None):

        if resources is None:
            return None

        resources_out = super().get_resources_details(
            resources, resources_bbrc, self.project_id)

        del resources_out['Resources/Project']

        return resources_out
