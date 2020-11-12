import pyxnat
import pyxnat.core.errors as pyxnat_errors
import socket
from tqdm import tqdm
import logging
import urllib3
import json

# Logging format
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
# Remove warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Fetcher:
    """ This class fetches data from XNAT instance
        Different methods are provided for fetching data from XNAT instance,
        Class takes path to configuration file for creating pyxnat Interface
        Object.
        Args:
            path (String): Path to pyxnat configuration file.
        Attributes:
            selector: Pyxnat Interface object used in whole class for
                calling different methods of pyxnat
    """

    # Initializing the central interface object in the constructor
    def __init__(self, config):

        selector = pyxnat.Interface(config=config)

        self.selector = selector

    # Disconnect with the instance
    def __del__(self):
        """Fetcher destructor
        Disconnect from the server after pyxnat object is destroyed
        """
        logging.info("Disconnected from XNAT instance")
        self.selector.disconnect()

    def get_instance_details(self):
        """Fetches all project details from XNAT instance
        Uses pyxnat methods to fetch all the details of projects, subjects
        experiments, scans present in the instance
        Returns:
            dict/int: **If no connection error is present, it returns
            a dictionary else an integer.**
            Dict with keys as **Projects**, **subjects**, **experiments**
            and **scans** that are present on instance.\n
            **Project** key contains information of each project.\n
            **Subject** key contains information of each subject that is
            age, gender, handedness, id, project which they belong.\n
            **Experiment** key contains information of each experiment
            with ID, Project which they belong, subject to which
            they belong, experiment type.\n
            **Scan** key contains information of each scan with
            ID, Project which they belong, subject to which
            they belong, scan type, scan quality, experiments in
            which they belong.\n
            **500** Error in url\n
            **401** Error in password or username\n
            **191912** remote host is not verifiable\n
            **1** Connection can't be established\n
        """
        try:
            projects = self.selector.select('xnat:projectData').all().data

            subjects = self.selector.get(
                '/data/subjects',
                params={'columns': 'ID,project,handedness,'
                                   'age,gender'}).json()['ResultSet']['Result'] \

            self.experiments = self.selector.array.experiments(
                experiment_type='',
                columns=['subject_ID', 'date']).data

            scans = self.selector.array.scans(
                columns=['xnat:imageScanData/quality',
                         'xnat:imageScanData/type']).data

        except pyxnat_errors.DatabaseError as dbe:
            if str(dbe).find('500') != -1:
                # 500 represent error in url or uri
                return 500
            elif str(dbe).find('401') != -1:
                # 401 represent error in login details
                return 401
        except socket.error as se:
            if str(se).find('SSL') != -1:
                # If verification enable and host unable to verify
                return 191912
            else:
                # Wrong URL Connection can't be established
                return 1

        all_data = {}

        all_data['projects'] = projects
        all_data['subjects'] = subjects
        all_data['experiments'] = self.experiments
        all_data['scans'] = scans

        return all_data

    def get_resources(self, experiments):

        resources = []
        resources_bbrc = []

        # For each experiments fetch all the resources associated with it
        for exp in tqdm(experiments):
            # -------------------- RESOURCES--------------------------------#
            res = self.selector._get_json('{}/{}'.format(exp['URI'], 'resources'))
            if len(res) == 0:
                resources.append([exp['project'], exp['ID'], 'No Data', 'No Data'])
            else:
                for r in res:
                    resources.append([exp['project'], exp['ID'], r['xnat_abstractresource_id'], r['label']])

            # -------------------- BBRC RESOURCES--------------------------------#
            # BBRC_VALIDATOR
            bbrc_validator = self.selector.select.experiment(exp['ID']).resource('BBRC_VALIDATOR')
            if bbrc_validator.exists:
                resources_bbrc.append([exp['project'], exp['ID'], True,
                                       self.tests_resource(bbrc_validator, 'ArchivingValidator')])
            else:
                resources_bbrc.append([exp['project'], exp['ID'], False, 0])
            # FREESURFER
            # fs = self.selector.select.experiment(exp['ID']).resource('FREESURFER6')
            # if fs.exists:
            #     resources_bbrc.append('True')
            #     try:
            #         log_file = list(fs.files('*recon-all.log'))[0]
            #         log_content = self.selector.get(log_file._uri).text
            #         target_str = '#@#%# recon-all-run-time-hours '
            #         time_diff = log_content[log_content.find(target_str) + len(target_str):].split()[0]
            #         resources_bbrc.append(time_diff)
            #     except IndexError:
            #         resources_bbrc.append(None)
            # else:
            #     resources_bbrc.append(None)

        return resources, resources_bbrc

    def tests_resource(self, res, name):

        try:
            j = [e for e in list(res.files('{}*.json'.format(name)))][0]
            j = json.loads(res._intf.get(j._uri).text)
            return j
        except IndexError:
            return 0
