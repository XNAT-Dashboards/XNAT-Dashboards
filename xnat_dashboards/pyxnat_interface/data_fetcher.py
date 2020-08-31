import pyxnat
import pyxnat.core.errors as pyxnat_errors
import socket
from tqdm import tqdm
import logging
import urllib3


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
                        'age,gender'}).json()['ResultSet']['Result']\

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
        """Fetches resource details of each experiments

        Looping through each experiments and fetching their corresponding
        resources

        Args:
            experiments (list): List of experiments with their IDs
                used for fetching resources

        Returns:
            2D list: Each row of contains resource ID its corresponding
            experiment id, project id and label
        """

        # Method for fetching resources details, get the list of experiments
        resources = []

        # For each experiments fetch all the resources associated with it
        for exp in tqdm(experiments):

            res = self.selector.select.experiments(exp['ID']).resources()
            res_Arr = list(res)

            # If their is a resource associated get  id and label
            # If empty then use 'No Data'

            if res_Arr == []:
                resources.append(
                    [exp['project'], exp['ID'], 'No Data', 'No Data'])
            else:
                for r in res_Arr:
                    resources.append(
                        [exp['project'], exp['ID'], r.id(), r.label()])

        return resources
