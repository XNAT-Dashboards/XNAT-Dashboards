import pickle
from datetime import datetime
import os
from xnat_dashboards import path_creator
from xnat_dashboards.pyxnat_interface import data_fetcher


class PickleSaver:
    """Class for saving the fetched data into pickle

        Different methods are provided to save different type of data.
        It can be used to save longitudinal and normal project, subjects,
        experiments, scans and resource data

        Args:
            config (String): Path to pyxnat configuration file.
            skip (Bool, Optional): Whether to skip resources fetching.
                If you don't want to see graphs related to resources.
                Default is to don't skip.
        Attributes:
            Server: Server url to be saved as a key for checking whether
                user belong to server.
            Skip: Used by methods for skipping resource details
    """

    def __init__(self, config, skip=False):

        # skip argument tell that whether to download resources
        # In case you want a quick look of xnat dashboard or you don't want
        # graphs related to resources use skip as True
        self.fetcher = data_fetcher.Fetcher(config=config)
        self.server = self.fetcher.selector._server
        self.skip = skip
        self.save()

    def save(self):
        """Method to save in pickle format

        This method fetches the details from Data Fetcher class methods,
        saves the projects, experiments, scan, subjects, resources saved.

        Returns:
            None: This returns None, Output pickled data file with following
            content.\n
            **Server:** URL of the server.\n
            **info:** Details of project, subject, experiments, scans.\n
            **resources:** Details of resources.\n
            **resource_bbrc:** Test details of resources specific to bbrc.\n
            **longitudinal_data:** Longitudinal Data.\n
        """
        # Fetch all resources, session, scans, projects, subjects
        file_exist = os.path.isfile(path_creator.get_pickle_path())

        # Create a temporary dict for longitudinal data
        user_data = {}

        # File exists then longitudinal data also exist save the longitudinal
        # data in user_data dict

        if file_exist:

            with open(
                    path_creator.get_pickle_path(),
                    'rb') as handle:
                user_data = pickle.load(handle)

                if 'server' in user_data:

                    if self.server != user_data['server']:
                        print(
                            "Server URL present in pickle is "
                            "different form the provided server URL")
                        return -1

        data_pro_sub_exp_sc = self.fetcher.get_instance_details()

        if not self.skip:
            data_res = self.fetcher.get_resources(
                data_pro_sub_exp_sc['experiments'])
            data_res_bbrc = self.fetcher.get_bbrc_resource(
                data_pro_sub_exp_sc['experiments'])

        # Call method for formatting the longitudinal data from raw saved data
        if not self.skip:
            longitudinal_data = self.longitudinal_data_processing(
                data_pro_sub_exp_sc, user_data, data_res
            )
        else:
            longitudinal_data = self.longitudinal_data_processing(
                data_pro_sub_exp_sc, user_data
            )

        # Save all the data to pickle
        with open(
                path_creator.get_pickle_path(),
                'wb') as handle:

            if not self.skip:
                pickle.dump(
                    {
                        'server': self.server,
                        'info': data_pro_sub_exp_sc,
                        'resources': data_res,
                        'resources_bbrc': data_res_bbrc,
                        'longitudinal_data': longitudinal_data
                    },
                    handle, protocol=pickle.HIGHEST_PROTOCOL)
            else:
                pickle.dump(
                    {
                        'server': self.server,
                        'info': data_pro_sub_exp_sc,
                        'longitudinal_data': longitudinal_data
                    },
                    handle, protocol=pickle.HIGHEST_PROTOCOL)

    def longitudinal_data_processing(
            self, data_pro_sub_exp_sc, user_data, data_res=None):
        """This method is use to save longitudinal data.

        This saves longitudinal data of projects, subjects, experiments,
        scans and resources. This is called when user fetches data.
        It takes the date on which the script ran and save the corresponding
        data.

        Args:
            data_pro_sub_exp_sc (dict): This contains dict of projects,
                subjects, experiments and scans
            user_data (dict): This contains dict either empty which tell that
                the script is ran for the first time and non empty meaning
                previous longitudinal data is already present
            data_res (dict, optional): This provide resource details
                if user skip the resource fetching option then defaults
                to None.

        Returns:
            dict:  Longitudinal data if ran first time then only single
            date point else will contains date points of time the
            script was run.
        """
        # Get current time
        now = datetime.now()
        dt = now.strftime("%d/%m/%Y")

        # Create the format of data to be saved
        projects_number = {'list': {dt: []}}
        subjects_number = {'list': {dt: []}}
        experiments_number = {'list': {dt: []}}
        scans_number = {'list': {dt: []}}

        projects_number['count'] = {dt: len(data_pro_sub_exp_sc['projects'])}
        subjects_number['count'] = {dt: len(data_pro_sub_exp_sc['subjects'])}
        experiments_number['count'] =\
            {dt: len(data_pro_sub_exp_sc['experiments'])}

        scans_number['count'] = {dt: len(data_pro_sub_exp_sc['scans'])}

        for project in data_pro_sub_exp_sc['projects']:
            projects_number['list'][dt].append(project['id'])

        for subject in data_pro_sub_exp_sc['subjects']:
            subjects_number['list'][dt].append(subject['ID'])

        for experiment in data_pro_sub_exp_sc['experiments']:
            experiments_number['list'][dt].append(experiment['ID'])

        for scan in data_pro_sub_exp_sc['scans']:
            scans_number['list'][dt].append(scan['ID'])

        # Resource data processing
        if not self.skip:
            resource_number = {'list': {dt: []}}

            for resource in data_res:
                if resource[2] != 'No Data':
                    resource_number['list'][dt].append(
                        str(resource[1]) + '  ' + str(resource[2]))

            resource_number['count'] = {dt: len(resource_number['list'][dt])}

        if user_data == {}:

            # If user_data is {} then this is the first time data
            # is being fetched thus create empty dict with normal formatting

            user_data['Projects'] = {'list': {}, 'count': {}}
            user_data['Subjects'] = {'list': {}, 'count': {}}
            user_data['Experiments'] = {'list': {}, 'count': {}}
            user_data['Scans'] = {'list': {}, 'count': {}}
            user_data['Resources'] = {'list': {}, 'count': {}}

        else:

            # Data is already present and use the longitudinal data from
            # the file and update the details of current data
            user_data = user_data['longitudinal_data']

        user_data['Projects']['list'].update(projects_number['list'])
        user_data['Subjects']['list'].update(subjects_number['list'])
        user_data['Experiments']['list'].update(experiments_number['list'])
        user_data['Scans']['list'].update(scans_number['list'])

        user_data['Projects']['count'].update(projects_number['count'])
        user_data['Subjects']['count'].update(subjects_number['count'])
        user_data['Experiments']['count'].update(
            experiments_number['count'])
        user_data['Scans']['count'].update(scans_number['count'])

        if not self.skip:
            user_data['Resources']['count'].update(resource_number['count'])

        '''
        Returns the formatted data
        {
            'Graph Name': {
                'count': {'date': 'counted_value'},
                'list': {'date': 'list_of_counted_values'}
            }
        }
        '''
        return user_data
