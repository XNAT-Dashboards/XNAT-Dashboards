from pyxnat import Interface


class Fetcher:

    SELECTOR = None

    # Initializing the central interface object in the constructor
    def __init__(self, name, password, instance_url):

        SELECTOR = Interface(server=instance_url, user=name, password=password)

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

        for project in projects:

            '''
            Looping through each project and create a dictonary that will add
            details like:
            Number of MR, PET and CT present in project to project_details.

            project_details is another dictionary which will have above
            information for each project and will add into the projects_details
            dictionary with the key of project as ID
            '''

            project_details = {}

            if(project['proj_mr_count'] == ''):
                project_details['proj_mr_count'] = 0
            else:
                project_details['proj_mr_count'] =\
                    int(project['proj_mr_count'])

            if(project['proj_ct_count'] == ''):
                project_details['proj_ct_count'] = 0
            else:
                project_details['proj_ct_count'] =\
                    int(project['proj_ct_count'])

            if(project['proj_pet_count'] == ''):
                project_details['proj_pet_count'] = 0
            else:
                project_details['proj_pet_count'] =\
                    int(project['proj_pet_count'])

            projects_details[project['id']] = projects_details

        projects_details['number_of_projects'] = len(projects)
        projects_details['project_mr_ct_pet'] = project_details

        return projects_details

    def get_subjects_details(self):

        try:
            print("Processing............")
            projectList = self.SELECTOR.get('/data/subjects',
                                        params= {'columns':['project']})\
                                        .json()['ResultSet']['Result']

            handednessList = self.SELECTOR.get('/data/subjects',
                                        params= {'columns':['handedness']})\
                                        .json()['ResultSet']['Result']

            ageList = self.SELECTOR.get('/data/subjects',
                                        params = {'columns':['age']})\
                                        .json()['ResultSet']['Result']

            genderList = self.SELECTOR.get('/data/subjects',
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

        subjects_details['age'] = []
        for item in ageList:

            if(item['age'] != ''):
                subjects_details['age'].append(item['age'])

        # Subject handedness information

        subjects_details['handedness'] = []
        for item in handednessList:

            if(item['handedness'] != ''):
                subjects_details['handedness'].append(item['handedness'])

        # Subject gender information

        subjects_details['gender'] = []
        for item in genderList:

            if(item['gender'] != ''):
                subjects_details['gender'].append(
                    item['gender'].lower()[:1])

        # Number of subjects information

        subjects_details['number_of_subjects'] = len(projectList)

        # Subjects per project information

        subjects_per_project = {}

        for item in projectList:
            if(item['project'] in subjects_per_project):
                subjects_per_project[item['project']] = \
                    subjects_per_project[item['project']] + 1
            else:
                subjects_per_project[item['project']] = 1

        subjects_details['subjects_per_project'] = subjects_per_project

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

        usable_scans = 0
        unusable_scans = 0

        for item in scans:
            if(item['xnat:imagescandata/quality'] == 'usable'):
                usable_scans = usable_scans+1
            else:
                unusable_scans = unusable_scans + 1

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

        scans_details['usable_scans'] = usable_scans
        scans_details['unusable_scans'] = unusable_scans
        scans_details['scan_types'] = type_dict
        scans_details['xsi_scan_types'] = xsi_type_dict
        scans_details['scans_per_project'] = scans_per_project
        scans_details['scans_per_subject'] = scans_per_subject
        scans_details['scans_per_experiment'] = scans_per_experiment
        scans_details['number_of_scans'] = len(scans)

        return scans_details
