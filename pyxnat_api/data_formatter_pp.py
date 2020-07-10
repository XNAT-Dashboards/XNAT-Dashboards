from collections import Counter, OrderedDict
from pyxnat_api import data_fetcher_pp
import numpy as np


class Formatter:

    project_id = None

    # Initializing the central interface object in the constructor
    def __init__(self, username, password, server, ssl, project_id):

        self.fetcher = data_fetcher_pp.Fetcher(
            username, password, server, ssl)
        self.project_id = project_id

    def get_projects_details(self):

        project_dict_list =\
            self.fetcher.get_project_details(self.project_id)

        if type(project_dict_list) == int:
            return project_dict_list
        else:
            project_dict = project_dict_list[0]

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

        subjects_data = self.fetcher.get_subjects_details(self.project_id)

        if type(subjects_data) == int:
            return subjects_data

        subjects_details = {}

        # Subject age information
        no_age_data_counter = 0
        age = []
        for item in subjects_data:
            if item['age'] != '':
                age.append(int(item['age']))
            else:
                no_age_data_counter = no_age_data_counter + 1

        # Create bins and their labels
        bins = np.arange(11) * 10 + 10
        age_range_bins = dict(Counter(np.digitize(age, bins)))

        age_range_od = OrderedDict()
        for key, value in sorted(age_range_bins.items()):
            if key != 11:
                age_range_od[str(key * 10) + '-' + str(key * 10 + 10)] =\
                    int(value)
            else:
                age_range_od['100+'] = int(value)

        age_range = dict(age_range_od)
        age_range.update({"No Age Data": no_age_data_counter})

        # Subject handedness information

        handedness = dict(Counter([item['handedness']
                          if item['handedness'] != ''
                          else
                          "No Data"
                          for item in subjects_data]))

        # Subject gender information

        gender = dict(Counter([item['gender'][0].upper()
                      if item['gender'] != ''
                      else
                      "No Data"
                      for item in subjects_data]))

        # Number of subjects information
        subjects_details['Number of Subjects'] = len(subjects_data)

        subjects_details['Age Range'] = age_range
        subjects_details['Gender'] = gender
        subjects_details['Handedness'] = handedness

        return subjects_details

    def get_experiments_details(self):

        experiments = self.fetcher.get_experiments_details(
            self.project_id)

        if type(experiments) == int:
            return experiments

        experiments_details = {}

        experiments_details['Number of Experiments'] = len(experiments)

        # Experiments type information

        experiment_type = dict(Counter([item['xsiType']
                               if item['xsiType'] != ''
                               else
                               "No Data"
                               for item in experiments]))

        # Experiments per subject information

        experiments_per_subject = dict(Counter([item['subject_ID']
                                       if item['subject_ID'] != ''
                                       else
                                       "No Data"
                                       for item in experiments]))

        experiments_details['Experiments/Subject'] = experiments_per_subject
        experiments_details['Experiment Types'] = experiment_type

        return experiments_details

    def get_scans_details(self):

        scans = self.fetcher.get_scans_details(self.project_id)

        if type(scans) == int:
            return scans

        scans_details = {}

        scan_quality = dict(Counter([item['xnat:imagescandata/quality']
                            if item['xnat:imagescandata/quality'] != ''
                            else
                            "No Data"
                            for item in scans]))
        # Scans type information

        type_dict = dict(Counter([item['xnat:imagescandata/type']
                         if item['xnat:imagescandata/type'] != ''
                         else
                         "No Data"
                         for item in scans]))

        # Scans xsi type information

        xsi_type_dict = dict(Counter([item['xsiType']
                             if item['xsiType'] != ''
                             else
                             "No Data"
                             for item in scans]))

        # Scans per subject information

        scans_per_subject = dict(Counter(
            [item['xnat:imagesessiondata/subject_id']
                if item['xnat:imagesessiondata/subject_id'] != ''
                else "No Data" for item in scans]))

        scans_details['Scans Quality'] = scan_quality
        scans_details['Scan Types'] = type_dict
        scans_details['XSI Scan Types'] = xsi_type_dict
        scans_details['Scans/Subject'] = scans_per_subject
        scans_details['Number of Scans'] = len(scans)

        return scans_details
