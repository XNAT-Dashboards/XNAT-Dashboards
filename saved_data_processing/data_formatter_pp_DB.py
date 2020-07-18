import pandas as pd


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

            resources_pp = df.groupby(['project']).get_group(self.project_id)
            del resources_pp['project']

        except KeyError:

            return -1

        resources_ps_df = resources_pp[[
            'session', 'resource']][resources_pp[
                'resource'] != 'No Data'].groupby('session').count()

        resource_ps = resources_ps_df.to_dict()['resource']

        no_data = resources_pp[resources_pp[
            'label'] == 'No Data']['session'].to_list()

        if len(no_data) != 0:

            no_data_dict = {}
            for item in no_data:
                no_data_dict[item] = 0

            resource_ps.update(no_data_dict)

        resources_types = resources_pp.groupby(
            'label').count()['resource'].to_dict()

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

        HasUsableT1 = df.groupby('Has Usable T1').count()['Session'].to_dict()
        HasArchivingValidator = df.groupby(
            'Archiving Valid').count()['Session'].to_dict()
        version_dist = df.groupby('version').count()['Session'].to_dict()
        bbrc_exists = df.groupby('bbrc exists').count()['Session'].to_dict()

        return {'Resources/Session': resource_ps,
                'Resource Types': resources_types,
                'UsableT1': HasUsableT1,
                'Archiving Validator': HasArchivingValidator,
                'Version Distribution': version_dist,
                'BBRC validator': bbrc_exists}
