import socket
import pandas as pd
import re


class Formatter:

    projects = None
    subjects = None
    experiments = None
    name = None
    resources_bbrc = None
    resources = None
    scans = None

    # Initializing the central interface object in the constructor
    def __init__(self, username, info, resources=None, resources_bbrc=None):

        self.name = username
        self.projects = info['projects']
        self.subjects = info['subjects']
        self.experiments = info['experiments']
        self.scans = info['scans']
        self.resources = resources
        self.resources_bbrc = resources_bbrc

    def get_projects_details(self):

        projects = self.projects

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

    def get_subjects_details(self):

        subjects_data = self.subjects

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

        # Subjects per project information

        spp_list = []

        for subject in subjects_data:
            spp_list.append([subject['project'], subject['ID']])

        spp_df = pd.DataFrame(spp_list, columns=['spp', 'count'])
        spp_df_series = spp_df.groupby('spp')['count'].apply(list)
        spp_df = spp_df.groupby('spp').count()
        spp_df['list'] = spp_df_series
        subjects_per_project = spp_df.to_dict()

        # Number of subjects information
        subjects_details['Number of Subjects'] = len(subjects_data)

        subjects_details['Subjects/Project'] = subjects_per_project
        subjects_details['Age Range'] = age_range
        subjects_details['Gender'] = gender
        subjects_details['Handedness'] = handedness

        return subjects_details

    def get_experiments_details(self):

        experiments = self.experiments

        if type(experiments) == int:
            return experiments

        experiments_details = {}

        experiments_details['Number of Experiments'] = len(experiments)

        # Experiments per project information

        epp_list = []

        for experiment in experiments:
            epp_list.append([experiment['project'], experiment['ID']])

        epp_df = pd.DataFrame(epp_list, columns=['epp', 'count'])
        epp_df_series = epp_df.groupby('epp')['count'].apply(list)
        epp_df = epp_df.groupby('epp').count()
        epp_df['list'] = epp_df_series
        experiments_per_project = epp_df.to_dict()

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
        experiments_details['Experiments/Project'] = experiments_per_project

        return experiments_details

    def get_scans_details(self):

        scans = self.scans

        if type(scans) == int:
            return scans

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

        # Scans per project information

        spp_list = []

        for scan in scans:
            spp_list.append([scan['project'], scan['ID']])

        spp_df = pd.DataFrame(spp_list, columns=['spp', 'count'])
        spp_df_series = spp_df.groupby('spp')['count'].apply(list)
        spp_df = spp_df.groupby('spp').count()
        spp_df['list'] = spp_df_series
        scans_per_project = spp_df.to_dict()

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

        scans_details = {}

        scans_details['Scans Quality'] = scan_quality
        scans_details['Scan Types'] = type_dict
        scans_details['XSI Scan Types'] = xsi_type_dict
        scans_details['Scans/Project'] = scans_per_project
        scans_details['Scans/Subject'] = scans_per_subject
        scans_details['Number of Scans'] = len(scans)

        return scans_details

    def get_projects_details_specific(self):

        try:
            projects = self.projects
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

    def get_resources_details(self):

        resources = self.resources
        resources_bbrc = self.resources_bbrc

        if resources is None:
            return None

        df = pd.DataFrame(
            resources['resources'],
            columns=['project', 'session', 'resource', 'label'])

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

        resource_types = df[df['resource'] != 'No Data'][['label', 'resource']]
        session = df[df['resource'] != 'No Data']['session']
        resource_types['resource'] = session + ' ' + resource_types['resource']
        resource_types = resource_types.rename(columns={'resource': 'count'})
        resources_types_df = resource_types.groupby(
            'label')['count'].apply(list)
        resource_types = resource_types.groupby('label').count()
        resource_types['list'] = resources_types_df
        resource_types = resource_types.to_dict()

        resource_processing = []

        for resource in resources_bbrc['resources_bbrc']:

            if resource[3] != 0:
                if 'HasUsableT1' in resource[3]:
                    resource_processing.append([
                        resource[0],
                        resource[1],
                        resource[2],
                        'Exists',
                        resource[3]['HasUsableT1']['has_passed'],
                        resource[3]['version']])
                else:
                    resource_processing.append([
                        resource[0],
                        resource[1],
                        resource[2],
                        'Not Exists',
                        'No Data',
                        resource[3]['version']])
            else:
                resource_processing.append([
                    resource[0],
                    resource[1],
                    resource[2],
                    'Not Exists',
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

        return {'Resources/Project': resource_pp,
                'Resource Types': resource_types,
                'UsableT1': usable_t1,
                'Archiving Validator': archiving_valid,
                'Version Distribution': version,
                'BBRC validator': bbrc_exists}
