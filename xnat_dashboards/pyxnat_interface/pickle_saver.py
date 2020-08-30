import pickle
from datetime import datetime
import os
import logging
from xnat_dashboards import config as config_file
from xnat_dashboards.bbrc import data_fetcher as data_fetcher_b
from xnat_dashboards.pyxnat_interface import data_fetcher

# Logging format
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


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

    def __init__(self, config):

        # skip argument tell that whether to fetch information from resources
        # In case you want a quick look of xnat dashboard or you don't want
        # graphs related to resources use skip as True
        self.fetcher = data_fetcher.Fetcher(config=config)
        self.fetcher_bbrc = data_fetcher_b.Fetcher(config=config)
        self.server = self.fetcher.selector._server

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
        file_exist = os.path.isfile(config_file.PICKLE_PATH)

        # Create a temporary dict for longitudinal data
        user_data = {}

        # File exists then longitudinal data also exist save the longitudinal
        # data in user_data dict

        if file_exist:

            with open(
                    config_file.PICKLE_PATH,
                    'rb') as handle:
                user_data = pickle.load(handle)

                if 'server' in user_data:

                    if self.server != user_data['server']:
                        logging.error(
                            "Server URL present in pickle is "
                            "different form the provided server URL")
                        return 1

        logging.info(
            "Fetching projects, subjects, experiments, and scans data")
        data_pro_sub_exp_sc = self.fetcher.get_instance_details()

        logging.info("Fetching resources")

        data_res = self.fetcher.get_resources(
            data_pro_sub_exp_sc['experiments'])

        # Check if bbrc resource label exist if they exist then
        # set the bbrc flag as True and fetch resource data else don't

        bbrc_flag = False
        for resource in data_res:
            if resource[3] == 'BBRC_VALIDATOR':
                logging.info(
                    "BBRC Validator resources found fetching BBRC resources")
                bbrc_flag = True
                break

        if bbrc_flag:
            logging.info("Fetching BBRC resources")
            extra_resources = self.fetcher_bbrc.get_resource(
                data_pro_sub_exp_sc['experiments'])
        else:
            extra_resources = None

        logging.info("Processing longitudinal data")
        # Call method for formatting the longitudinal data from raw saved data
        longitudinal_data = self.longitudinal_data_processing(
            data_pro_sub_exp_sc, user_data, data_res
        )

        # Save all the data to pickle
        with open(
                config_file.PICKLE_PATH,
                'wb') as handle:

            pickle.dump(
                {
                    'server': self.server,
                    'info': data_pro_sub_exp_sc,
                    'resources': data_res,
                    'extra_resources': extra_resources,
                    'longitudinal_data': longitudinal_data
                },
                handle, protocol=pickle.HIGHEST_PROTOCOL)

        logging.info(
            "Pickle file successfully saved at: "
            +
            str(config_file.PICKLE_PATH))

    def longitudinal_data_processing(
            self, data_pro_sub_exp_sc, user_data, data_res):
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
                to None and no resources data will be added in pickle.

        Returns:
            dict:  Longitudinal data if ran first time then only single
            date point else will contains date points of time the
            script was run.
        """
        # Get current time
        now = datetime.now()
        dt = now.strftime("%d/%m/%Y")

        l_data = {}

        if 'longitudinal_data' in user_data:
            l_data = user_data['longitudinal_data']

        graph_names = ['Projects', 'Subjects', 'Experiments', 'Scans']
        key_names = ['projects', 'subjects', 'experiments', 'scans']

        for id in range(0, len(graph_names)):

            graph_number = {'list': {dt: []}}
            graph_number['count'] = {
                dt: len(data_pro_sub_exp_sc[key_names[id]])}

            for graph in data_pro_sub_exp_sc[key_names[id]]:
                if key_names[id] == 'projects':
                    graph_number['list'][dt].append(graph['id'])
                else:
                    graph_number['list'][dt].append(graph['ID'])

            if user_data == {}:
                l_data[graph_names[id]] = {
                    'list': graph_number['list'],
                    'count': graph_number['count']}
            else:
                l_data[graph_names[id]]['list'].update(graph_number['list'])
                l_data[graph_names[id]]['count'].update(graph_number['count'])

        resource_number = {'list': {dt: []}}

        for resource in data_res:
            if resource[2] != 'No Data':
                resource_number['list'][dt].append(
                    str(resource[1]) + '  ' + str(resource[2]))

        resource_number['count'] = {dt: len(resource_number['list'][dt])}

        if user_data == {}:
            l_data['Resources'] = {
                'list': resource_number['list'],
                'count': resource_number['count']}
        else:
            l_data['Resources']['list'].update(resource_number['list'])
            l_data['Resources']['count'].update(resource_number['count'])

        '''
        Returns the formatted data
        {
            'Graph Name': {
                'count': {'date': 'counted_value'},
                'list': {'date': 'list_of_counted_values'}
            }
        }
        '''
        return l_data
