from pyxnat import Interface


class Fetcher:

    SELECTOR = None
    stats = {}

    # Initializing the central interface object in the constructor
    def __init__(self, name, password, instance_url):

        SELECTOR = Interface(server=instance_url, user=name, password=password)

        self.SELECTOR = SELECTOR
        self.get_projects_details()
        self.get_subjects_details()

    def get_projects_details(self):

        try:
            print("Processing............")
            projects = self.SELECTOR.select('xnat:projectData').all().data
        except Exception:
            print("ERROR : Unable to connect to the database")
            self.stats['get_subjects_details'] = None
            return None

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

        self.stats['get_projects_details'] = project_details

    def get_subjects_details(self):

        try:
            print("Processing............")
            subjects = self.SELECTOR.select('xnat:subjectData').all().data
        except Exception:
            print("ERROR : Unable to connect to the database")
            self.stats['get_subjects_details'] = None
            return None

        # Subject_details is a dictionary which will add details of
        # all subjects to the global stats dictionary

        subjects_details = {}
        subjects_per_project = {}

        for subject in subjects:

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

            subject_details = {}

            if(subject['handedness_text'] == ''):
                subject_details['handedness_text'] = 'U'
            else:
                subject_details['handedness_text'] = subject['handedness_text']

            if(subject['gender_text'] == ''):
                subject_details['gender_text'] = 'U'
            else:
                subject_details['gender_text'] = subject['gender_text']

            if(subject['project'] in subjects_per_project):
                subjects_per_project[subject['project']] =\
                    subjects_per_project[subject['project']] + 1
            else:
                subjects_per_project[subject['project']] = 1

            subjects_details[subject['xnat_col_subjectdatalabel']] =\
                subject_details

        subjects_details['number_of_subjects'] = len(subjects_details)

        self.stats['get_project_details'] = subjects_details
        self.stats['subjects_per_project'] = subjects_per_project

    def get_experiments_details(self):

        experiments = self.SELECTOR.array.experiments(
                                            experiment_type='',
                                            columns=['subject_ID']).data

        experiments_details = {}

        experiments_details['number_of_experiments'] = len(experiments)

        experiments_per_project = {}

        for item in experiments:
            if(item['project'] in experiments_per_project):
                experiments_per_project[item['project']] = \
                    experiments_per_project[item['project']] + 1
            else:
                experiments_per_project[item['project']] = 1

        experiment_type = {}

        for item in experiments:
            if(item['xsiType'] in experiment_type):
                experiment_type[item['xsiType']] = \
                    experiment_type[item['xsiType']] + 1
            else:
                experiment_type[item['xsiType']] = 1

        experiments_per_subject = {}

        for item in experiments:
            if(item['subject_ID'] in experiments_per_subject):
                experiments_per_subject[item['subject_ID']] = \
                    experiments_per_subject[item['subject_ID']] + 1
            else:
                experiments_per_subject[item['subject_ID']] = 1

        experiments_details['experiments_per_subject'] = experiments_per_subject
        experiments_details['experiment_types'] = experiment_type
        experiments_details['experiment_per_project'] = experiments_per_project

        self.stats['get_experiments_details'] = experiments_details
