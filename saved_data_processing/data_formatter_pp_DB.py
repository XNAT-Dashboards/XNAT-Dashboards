import pandas as pd
import re


class Formatter:

    projects = None
    subjects = None
    experiments = None
    name = None
    scans = None
    project_id = None

    # Initializing the central interface object in the constructor
    def __init__(self, username, info,
                 project_id, resources=None, resources_bbrc=None):

        self.name = username
        self.projects = info['projects']
        self.subjects = info['subjects']
        self.experiments = info['experiments']
        self.scans = info['scans']
        self.resources = resources
        self.project_id = project_id
        self.resources_bbrc = resources_bbrc

    def get_projects_details(self):

        projects = self.projects
        project_dict = {}

        for project in projects:

            if project['id'] == self.project_id:
                project_dict = project

        project_details = {}

        project_details['Total Sessions'] = 0
        project_details['Imaging Sessions'] = {}

        if project_dict['proj_mr_count'] != '':
            project_details['Total Sessions'] =\
                project_details['Total Sessions']\
                + int(project_dict['proj_mr_count'])
            project_details['Imaging Sessions'].update({
                'MR Sessions': int(project_dict['proj_mr_count'])})
        else:
            project_details['Imaging Sessions'].update({
                'MR Sessions': 0})

        if project_dict['proj_pet_count'] != '':
            project_details['Total Sessions'] =\
                project_details['Total Sessions']\
                + int(project_dict['proj_pet_count'])
            project_details['Imaging Sessions'].update({
                'PET Sessions': int(project_dict['proj_mr_count'])})
        else:
            project_details['Imaging Sessions'].update({
                'PET Sessions': 0})

        if project_dict['proj_ct_count'] != '':
            project_details['Total Sessions'] =\
                project_details['Total Sessions']\
                + int(project_dict['proj_ct_count'])
            project_details['Imaging Sessions'].update({
                'CT Sessions': int(project_dict['proj_mr_count'])})
        else:
            project_details['Imaging Sessions'].update({
                'CT Sessions': 0})

        if project_dict['proj_ut_count'] != '':
            project_details['Total Sessions'] =\
                project_details['Total Sessions']\
                + int(project_dict['proj_ut_count'])
            project_details['Imaging Sessions'].update({
                'UT Sessions': int(project_dict['proj_mr_count'])})
        else:
            project_details['Imaging Sessions'].update({
                'UT Sessions': 0})

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

    def get_subjects_details(self):

        subjects = self.subjects
        subjects_data = []

        for subject in subjects:
            if subject['project'] == self.project_id:
                subjects_data.append(subject)

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

        # Subject handedness information

        hand_list = []
        hand_none = []

        for subject in subjects_data:
            if subject['handedness'] != '':
                hand_list.append([subject['handedness'], subject['ID']])
            else:
                hand_none.append(subject['ID'])

        hand_df = pd.DataFrame(hand_list, columns=['handedness', 'count'])
        hand_df_series = hand_df.groupby('handedness')['count'].apply(list)
        hand_final_df = hand_df.groupby('handedness').count()
        hand_final_df['list'] = hand_df_series
        handedness = hand_final_df.to_dict()
        handedness['count'].update({'No Data': len(hand_none)})
        handedness['list'].update({'No Data': hand_none})

        # Subject gender information

        gender_list = []
        gender_none = []

        for subject in subjects_data:
            if subject['gender'] != '':
                gender_list.append(
                    [subject['gender'][0].upper(), subject['ID']])
            else:
                gender_none.append(subject['ID'])

        gender_df = pd.DataFrame(gender_list, columns=['gender', 'count'])
        gender_df_series = gender_df.groupby('gender')['count'].apply(list)
        gender_final_df = gender_df.groupby('gender').count()
        gender_final_df['list'] = gender_df_series
        gender = gender_final_df.to_dict()
        gender['count'].update({'No Data': len(gender_none)})
        gender['list'].update({'No Data': gender_none})

        # Number of subjects information
        subjects_details['Number of Subjects'] = len(subjects_data)

        subjects_details['Age Range'] = age_range
        subjects_details['Gender'] = gender
        subjects_details['Handedness'] = handedness

        return subjects_details

    def get_experiments_details(self):

        experiments_data = self.experiments
        experiments = []

        for experiment in experiments_data:
            if experiment['project'] == self.project_id:
                experiments.append(experiment)

        experiments_details = {}

        experiments_details['Number of Experiments'] = len(experiments)

        # Experiments type information

        xsiType_list = []
        xsiType_none = []

        for experiment in experiments:
            if experiment['xsiType'] != '':
                xsiType_list.append([experiment['xsiType'], experiment['ID']])
            else:
                xsiType_none.append(experiment['ID'])

        xsiType_df = pd.DataFrame(xsiType_list, columns=['xsiType', 'count'])
        xsiType_df_series = xsiType_df.groupby('xsiType')['count'].apply(list)
        xsiType_final_df = xsiType_df.groupby('xsiType').count()
        xsiType_final_df['list'] = xsiType_df_series
        experiment_type = xsiType_final_df.to_dict()
        experiment_type['count'].update({'No Data': len(xsiType_none)})
        experiment_type['list'].update({'No Data': xsiType_none})

        # Experiments per subject information

        eps_list = []

        for experiment in experiments:
            eps_list.append([experiment['subject_ID'], experiment['ID']])

        eps_df = pd.DataFrame(eps_list, columns=['eps', 'count'])
        eps_df_series = eps_df.groupby('eps')['count'].apply(list)
        eps_df = eps_df.groupby('eps').count()
        eps_df['list'] = eps_df_series
        experiments_per_subject = eps_df.to_dict()

        experiments_details['Experiments/Subject'] = experiments_per_subject
        experiments_details['Experiment Types'] = experiment_type

        return experiments_details

    def get_scans_details(self):

        scans_data = self.scans
        scans = []

        for scan in scans_data:
            if scan['project'] == self.project_id:
                scans.append(scan)

        scans_details = {}

        scan_quality_list = []
        scan_quality_none = []

        for scan in scans:
            if scan['xnat:imagescandata/quality'] != '':
                scan_quality_list.append(
                    [scan['xnat:imagescandata/quality'], scan['ID']])
            else:
                scan_quality_none.append(scan['ID'])

        scan_quality_df = pd.DataFrame(
            scan_quality_list, columns=['quality', 'count'])
        scan_quality_df_series = scan_quality_df.groupby(
            'quality')['count'].apply(list)
        scan_quality_final_df = scan_quality_df.groupby('quality').count()
        scan_quality_final_df['list'] = scan_quality_df_series
        scan_quality = scan_quality_final_df.to_dict()
        scan_quality['count'].update({'No Data': len(scan_quality_none)})
        scan_quality['list'].update({'No Data': scan_quality_none})

        # Scans type information

        type_list = []
        type_none = []

        for scan in scans:
            if scan['xnat:imagescandata/type'] != '':
                type_list.append(
                    [scan['xnat:imagescandata/type'], scan['ID']])
            else:
                type_none.append(scan['ID'])

        type_df = pd.DataFrame(type_list, columns=['type', 'count'])
        type_df_series = type_df.groupby('type')['count'].apply(list)
        type_final_df = type_df.groupby('type').count()
        type_final_df['list'] = type_df_series
        type_dict = type_final_df.to_dict()
        type_dict['count'].update({'No Data': len(type_none)})
        type_dict['list'].update({'No Data': type_none})

        # Scans xsi type information

        xsiType_list = []
        xsiType_none = []

        for scan in scans:
            if scan['xsiType'] != '':
                xsiType_list.append([scan['xsiType'], scan['ID']])
            else:
                xsiType_none.append(scan['ID'])

        xsiType_df = pd.DataFrame(xsiType_list, columns=['xsiType', 'count'])
        xsiType_df_series = xsiType_df.groupby('xsiType')['count'].apply(list)
        xsiType_final_df = xsiType_df.groupby('xsiType').count()
        xsiType_final_df['list'] = xsiType_df_series
        xsi_type_dict = xsiType_final_df.to_dict()
        xsi_type_dict['count'].update({'No Data': len(xsiType_none)})
        xsi_type_dict['list'].update({'No Data': xsiType_none})

        # Scans per subject information

        sps_list = []

        for scan in scans:
            sps_list.append(
                [scan['xnat:imagesessiondata/subject_id'], scan['ID']])

        sps_df = pd.DataFrame(sps_list, columns=['sps', 'count'])
        sps_df_series = sps_df.groupby('sps')['count'].apply(list)
        sps_df = sps_df.groupby('sps').count()
        sps_df['list'] = sps_df_series
        scans_per_subject = sps_df.to_dict()

        scans_details['Scans Quality'] = scan_quality
        scans_details['Scan Types'] = type_dict
        scans_details['XSI Scan Types'] = xsi_type_dict
        scans_details['Scans/Subject'] = scans_per_subject
        scans_details['Number of Scans'] = len(scans)

        return scans_details

    def get_resources_details(self):

        resources = self.resources

        if resources is None:
            return None

        df = pd.DataFrame(
            resources['resources'],
            columns=['project', 'session', 'resource', 'label'])

        try:

            df = df.groupby(['project']).get_group(self.project_id)
            del df['project']

        except KeyError:

            return -1
        df['resource'] = df['resource'].map(
            lambda x: re.sub('<Resource Object>', 'Resource Object', str(x)))

        resource_ps = df[df['resource'] != 'No Data'][['session', 'resource']]
        resource_ps = resource_ps.rename(columns={'resource': 'count'})
        resources_ps_df = resource_ps.groupby('session')['count'].apply(list)
        resource_ps = resource_ps.groupby('session').count()
        resource_ps['list'] = resources_ps_df
        resource_ps = resource_ps.to_dict()

        no_data = df[df[
            'label'] == 'No Data']['session'].to_list()

        if len(no_data) != 0:

            no_data_dict = {}
            for item in no_data:
                no_data_dict[item] = 0

            resource_ps['count'].update(no_data_dict)

        resource_types = df[df['resource'] != 'No Data'][['label', 'resource']]
        session = df[df['resource'] != 'No Data']['session']
        resource_types['resource'] = session + ' ' + resource_types['resource']
        resource_types = resource_types.rename(columns={'resource': 'count'})
        resources_types_df = resource_types.groupby(
            'label')['count'].apply(list)
        resource_types = resource_types.groupby('label').count()
        resource_types['list'] = resources_types_df
        resource_types = resource_types.to_dict()

        # Code for bbrc validator

        resource_processing = []

        for resource in self.resources_bbrc['resources_bbrc']:

            if resource[3] != 0:
                if 'HasUsableT1' in resource[3]:
                    resource_processing.append([
                        resource[0],
                        resource[1],
                        resource[2],
                        True,
                        resource[3]['HasUsableT1']['has_passed'],
                        resource[3]['version']])
                else:
                    resource_processing.append([
                        resource[0],
                        resource[1],
                        resource[2],
                        True,
                        'No Data',
                        resource[3]['version']])
            else:
                resource_processing.append([
                    resource[0],
                    resource[1],
                    resource[2],
                    'No Data',
                    'No Data',
                    'No Data'])

        df = pd.DataFrame(
            resource_processing,
            columns=[
                'Project',
                'Session',
                'bbrc exists',
                'Archiving Valid',
                'Has Usable T1',
                'version'])

        df = df.groupby('Project').get_group(self.project_id)

        usable_t1 = df[df['Session'] != 'No Data'][[
            'Has Usable T1', 'Session']]
        usable_t1 = usable_t1.rename(columns={'Session': 'count'})
        usable_t1_df = usable_t1.groupby('Has Usable T1')['count'].apply(list)
        usable_t1 = usable_t1.groupby('Has Usable T1').count()
        usable_t1['list'] = usable_t1_df
        usable_t1 = usable_t1.to_dict()

        archiving_valid = df[df['Session'] != 'No Data'][[
            'Archiving Valid', 'Session']]
        archiving_valid = archiving_valid.rename(columns={'Session': 'count'})
        archiving_valid_df = archiving_valid.groupby(
            'Archiving Valid')['count'].apply(list)
        archiving_valid = archiving_valid.groupby('Archiving Valid').count()
        archiving_valid['list'] = archiving_valid_df
        archiving_valid = archiving_valid.to_dict()

        version = df[df['Session'] != 'No Data'][[
            'version', 'Session']]
        version = version.rename(columns={'Session': 'count'})
        archiving_valid_df = version.groupby(
            'version')['count'].apply(list)
        version = version.groupby('version').count()
        version['list'] = archiving_valid_df
        version = version.to_dict()

        bbrc_exists = df[df['Session'] != 'No Data'][[
            'bbrc exists', 'Session']]
        bbrc_exists = bbrc_exists.rename(columns={'Session': 'count'})
        archiving_valid_df = bbrc_exists.groupby(
            'bbrc exists')['count'].apply(list)
        bbrc_exists = bbrc_exists.groupby('bbrc exists').count()
        bbrc_exists['list'] = archiving_valid_df
        bbrc_exists = bbrc_exists.to_dict()

        return {'Resources/Session': resource_ps,
                'Resource Types': resource_types,
                'UsableT1': usable_t1,
                'Archiving Validator': archiving_valid,
                'Version Distribution': version,
                'BBRC validator': bbrc_exists}
