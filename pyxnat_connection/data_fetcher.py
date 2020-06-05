from pyxnat import Interface


class Fetcher:

    SELECTOR = None

    # Initializing the central interface object in the constructor
    def __init__(self, name, password, server):

        SELECTOR = Interface(server=server, user=name, password=password)

        self.SELECTOR = SELECTOR

    def get_projects_details(self):

        try:
            print("Processing............")
            projects = self.SELECTOR.select('xnat:projectData').all().data
        except Exception:
            print("ERROR : Unable to connect to the database")
            return 1

        # Projects_details is a dictionary which will add details of all
        # projects to the global stats dictionary

        projects_details = {}
        projects_mr_pet_ct = {'project_mr_count': 0,
                              'project_ct_count': 0,
                              'project_pet_count': 0}

        for project in projects:

            '''
            Looping through each project and create a dictonary that will add
            details like:
            Number of MR, PET and CT present in project to project_details.

            project_details is another dictionary which will have above
            information for each project and will add into the projects_details
            dictionary with the key of project as ID
            '''

            if(project['proj_mr_count'] == ''):
                projects_mr_pet_ct['project_mr_count'] =\
                    projects_mr_pet_ct['project_mr_count']\
                    + 0
            else:
                projects_mr_pet_ct['project_mr_count'] =\
                    projects_mr_pet_ct['project_mr_count']\
                    + int(project['proj_mr_count'])

            if(project['proj_pet_count'] == ''):
                projects_mr_pet_ct['project_pet_count'] =\
                    projects_mr_pet_ct['project_pet_count']\
                    + 0
            else:
                projects_mr_pet_ct['project_pet_count'] =\
                    projects_mr_pet_ct['project_pet_count']\
                    + int(project['proj_pet_count'])

            if(project['proj_ct_count'] == ''):
                projects_mr_pet_ct['project_ct_count'] =\
                    projects_mr_pet_ct['project_ct_count'] \
                    + 0
            else:
                projects_mr_pet_ct['project_ct_count'] =\
                    projects_mr_pet_ct['project_ct_count']\
                    + int(project['proj_ct_count'])

        projects_details['number_of_projects'] = len(projects)
        projects_details['project_mr_pet_ct'] = projects_mr_pet_ct

        return projects_details

    def get_subjects_details(self):

        try:
            print("Processing............")
            project_list = self.SELECTOR.get('/data/subjects',
                                        params= {'columns':['project']})\
                                        .json()['ResultSet']['Result']

            handedness_list = self.SELECTOR.get('/data/subjects',
                                        params= {'columns':['handedness']})\
                                        .json()['ResultSet']['Result']

            age_list = self.SELECTOR.get('/data/subjects',
                                        params = {'columns':['age']})\
                                        .json()['ResultSet']['Result']

            gender_list = self.SELECTOR.get('/data/subjects',
                                        params={'columns':['gender']})\
                                        .json()['ResultSet']['Result']
        except Exception:
            print("ERROR : Unable to connect to the database")
            return 1

        # Subject_details is a dictionary which will add details of
        # all subjects to the global stats dictionary

        subjects_details = {}

        '''
        Looping through each subject and create a dictonary that will
        add details like Number of left,right and unknown handed subjects,
        gender of each subjects

        project_details is another dictionary which will have above
        information for each project and will add into the projects_details
        dictionary with the key of project as ID

        This also add a dictionary data showing number of
        subjects per project
        '''

        # Subject age information

        age_range = {'10': 0,
                     '20': 0,
                     '30': 0,
                     '40': 0,
                     '50': 0,
                     '60': 0,
                     '70': 0,
                     '80': 0,
                     '90': 0,
                     '100': 0,
                     '100 above': 0}

        for item in age_list:

            if(item['age'] == ''):
                continue
            elif(int(item['age']) <= 10):
                age_range['10'] = age_range['10'] + 1
            elif(int(item['age']) <= 20):
                age_range['20'] = age_range['20'] + 1
            elif(int(item['age']) <= 30):
                age_range['30'] = age_range['30'] + 1
            elif(int(item['age']) <= 40):
                age_range['40'] = age_range['40'] + 1
            elif(int(item['age']) <= 50):
                age_range['50'] = age_range['50'] + 1
            elif(int(item['age']) <= 60):
                age_range['60'] = age_range['60'] + 1
            elif(int(item['age']) <= 70):
                age_range['70'] = age_range['70'] + 1
            elif(int(item['age']) <= 80):
                age_range['80'] = age_range['80'] + 1
            elif(int(item['age']) <= 90):
                age_range['90'] = age_range['90'] + 1
            elif(int(item['age']) <= 100):
                age_range['100'] = age_range['100'] + 1
            else:
                age_range['100 above'] = age_range['100 above'] + 1

        # Subject handedness information

        handedness = {'Right': 0, 'Left': 0, 'Ambidextrous': 0}

        for item in handedness_list:

            if(item['handedness'] == ''):
                continue
            if(item['handedness'] == 'right'):
                handedness['Right'] = handedness['Right'] + 1
            elif(item['handedness'] == 'left'):
                handedness['Left'] = handedness['Left'] + 1
            else:
                handedness['Ambidextrous'] = handedness['Ambidextrous'] + 1
        # Subject gender information

        gender = {'Male': 0, 'Female': 0}

        for item in gender_list:

            if(item['gender'] == ''):
                continue
            if(item['gender'].lower()[:1] == 'm'):
                gender['Male'] = gender['Male'] + 1
            else:
                gender['Female'] = gender['Female'] + 1

        # Subjects per project information

        subjects_per_project = {}

        for item in project_list:
            if(item['project'] in subjects_per_project):
                subjects_per_project[item['project']] = \
                    subjects_per_project[item['project']] + 1
            else:
                subjects_per_project[item['project']] = 1

        # Number of subjects information
        subjects_details['number_of_subjects'] = len(project_list)

        subjects_details['subjects_per_project'] = subjects_per_project
        subjects_details['age_range'] = age_range
        subjects_details['gender'] = gender
        subjects_details['handedness'] = handedness

        return subjects_details

    def get_experiments_details(self):

        '''
        Using array method to get the experiment information present on XNAT.

        This will add a get_experiment_details key in stats dictionary
        which will have details of number of experiments, experiment per
        project, type of experiment, experiment per subjects.
        '''
        try:
            experiments = self.SELECTOR.array.experiments(
                                            experiment_type='',
                                            columns=['subject_ID']).data
        except Exception:
            return 1

        experiments_details = {}

        experiments_details['number_of_experiments'] = len(experiments)

        # Experiments per project information

        experiments_per_project = {}

        for item in experiments:
            if(item['project'] in experiments_per_project):
                experiments_per_project[item['project']] = \
                    experiments_per_project[item['project']] + 1
            else:
                experiments_per_project[item['project']] = 1

        # Experiments type information

        experiment_type = {}

        for item in experiments:
            if(item['xsiType'] in experiment_type):
                experiment_type[item['xsiType']] = \
                    experiment_type[item['xsiType']] + 1
            else:
                experiment_type[item['xsiType']] = 1

        # Experiments per subject information

        experiments_per_subject = {}

        for item in experiments:
            if(item['subject_ID'] in experiments_per_subject):
                experiments_per_subject[item['subject_ID']] = \
                    experiments_per_subject[item['subject_ID']] + 1
            else:
                experiments_per_subject[item['subject_ID']] = 1

        experiments_details['experiments_per_subject'] = experiments_per_subject
        experiments_details['experiment_types'] = experiment_type
        experiments_details['experiments_per_project'] = experiments_per_project

        return experiments_details

    def get_scans_details(self):

        '''
        Using array method to get the scans information present on XNAT.

        This will add a get_scans_details key in stats dictionary
        which will have details of number of scans, scans per subject,
        scans per project, scans per experimetn, type of experiment,
        scan quality (usable or unusable), xsi type of scan.
        '''
        try:
            scans = self.SELECTOR.array.scans(
                columns=['xnat:imageScanData/quality',
                         'xnat:imageScanData/type'])
        except Exception:
            return 1

        scan_quality = {'usable_scans': 0, 'unusable_scans': 0}

        for item in scans:
            if(item['xnat:imagescandata/quality'] == 'usable'):
                scan_quality['usable_scans'] = scan_quality['usable_scans']+1
            else:
                scan_quality['unusable_scans'] =\
                                    scan_quality['unusable_scans'] + 1

        scans_details = {}

        # Scans type information

        type_dict = {}

        for item in scans:
            if(item['xnat:imagescandata/type'] in type_dict):
                type_dict[item['xnat:imagescandata/type']] =\
                        type_dict[item['xnat:imagescandata/type']] + 1
            else:
                type_dict[item['xnat:imagescandata/type']] = 1

        # Scans xsi type information

        xsi_type_dict = {}

        for item in scans:
            if(item['xsiType'] in xsi_type_dict):
                xsi_type_dict[item['xsiType']] = \
                                    xsi_type_dict[item['xsiType']] + 1
            else:
                xsi_type_dict[item['xsiType']] = 1

        # Scans per project information

        scans_per_project = {}

        for item in scans:
            if(item['project'] in scans_per_project):
                scans_per_project[item['project']] = \
                        scans_per_project[item['project']] + 1
            else:
                scans_per_project[item['project']] = 1

        # Scans per subject information

        scans_per_subject = {}

        for item in scans:
            if(item['xnat:imagesessiondata/subject_id'] in scans_per_subject):
                scans_per_subject[item['xnat:imagesessiondata/subject_id']] = \
                    scans_per_subject[item['xnat:imagesessiondata/subject_id']] + 1
            else:
                scans_per_subject[item['project']] = 1

        # Scans per experiment information

        scans_per_experiment = {}

        for item in scans:
            if(item['ID'] in scans_per_subject):
                scans_per_experiment[item['ID']] = \
                    scans_per_experiment[item['ID']] + 1
            else:
                scans_per_experiment[item['ID']] = 1

        scans_details['scans_quality'] = scan_quality
        scans_details['scan_types'] = type_dict
        scans_details['xsi_scan_types'] = xsi_type_dict
        scans_details['scans_per_project'] = scans_per_project
        scans_details['scans_per_subject'] = scans_per_subject
        scans_details['scans_per_experiment'] = scans_per_experiment
        scans_details['number_of_scans'] = len(scans)

        return scans_details
