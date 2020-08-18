import pyxnat
import pyxnat.core.errors as pyxnat_errors
import socket
import json
import warnings
from tqdm import tqdm
warnings.filterwarnings("ignore")


class Fetcher:

    """ This class fetches data from XNAT instance

        Different methods are provided for fetching data from XNAT instance,
        Class takes path to configuration file for creating pyxnat Interface
        Object.

        Args:
            path (String): Path to pyxnat configuration file.

        Attributes:
            SELECTOR: Pyxnat Interface object used in whole class for
                calling different methods of pyxnat
    """

    # Initializing the central interface object in the constructor
    def __init__(self, config):

        SELECTOR = pyxnat.Interface(config=config)

        self.SELECTOR = SELECTOR

    # Disconnect with the instance
    def __del__(self):
        """Fetcher destructor
        Disconnect from the server after pyxnat object is destroyed
        """
        print("Disconnected")
        self.SELECTOR.disconnect()

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
            projects = self.SELECTOR.select('xnat:projectData').all().data

            subjects = self.SELECTOR.get(
                '/data/subjects',
                params={'columns': 'ID,project,handedness,'
                        'age,gender'}).json()['ResultSet']['Result']\

            self.experiments = self.SELECTOR.array.experiments(
                experiment_type='',
                columns=['subject_ID', 'date']).data

            scans = self.SELECTOR.array.scans(
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

        Looping throug each experiments and fetching their corresponding
        resources

        Args:
            experiments (list): Gets the list of experiments with thier IDs
                used for fetching resources

        Returns:
            2D list: Each row of this have resource ID it's corresponding
            experiment id, it's corresponding project id and it's label
        """

        # Method for fetching resources details, get the list of experiments
        resources = []

        # For each experiments fetch all the resources associated with it
        for exp in tqdm(experiments):

            res = self.SELECTOR.select.experiments(exp['ID']).resources()
            res_Arr = []

            # Add resource of different type to res_Arr
            for r in res:
                res_Arr.append(r)

            # If their is a resource associated get it's id and label
            # If empty then use 'No Data'

            if res_Arr == []:
                resources.append(
                    [exp['project'], exp['ID'], 'No Data', 'No Data'])
            else:
                for r in res_Arr:
                    resources.append(
                        [exp['project'], exp['ID'], r.id(), r.label()])

        return resources

    def get_bbrc_resource(self, experiments):
        """Method specific to BBRC XNAT instance

        Special resource BBRC_Validator contains information
        of different test that are done on experiments. Loop through
        each experiment check if BBRC validator resource exist, if
        exist then check for archiving validator using test method.
        If archiving validator exist then save the json fetched from validator
        as dict with information of tests. If don't exist then use 'No Data' as
        an identifier.

        Args:
            experiments (list): Gets the list of experiments with thier IDs
            used for fetching resources

        Returns:
            2D list: Each row of this have experiment id it's corresponding
            project id, Whether BBRC data exist and Archiving details as dict
            if exists
        """
        # Get the list of all experiments
        resource_bbrc_validator = []

        for exp in tqdm(experiments):

            # Check whether 'BBRC Validator' type resource exists
            # for the experiment

            BBRC_VALIDATOR = self.SELECTOR.select.experiment(
                exp['ID']).resource('BBRC_VALIDATOR')
            exists = 'Exists' if BBRC_VALIDATOR.exists() else 'No Exists'

            # If exist then further process and check whether archiving
            # validator exist if exist then get the test json and if not
            # exists then Index error will be thrown and place 0 instead
            if exists:
                try:
                    resource_bbrc_validator.append([
                        exp['project'],
                        exp['ID'],
                        exists,
                        self.tests_resource(
                            BBRC_VALIDATOR, 'ArchivingValidator')])
                except IndexError:
                    resource_bbrc_validator.append(
                        [exp['project'], exp['ID'], exists, 0])
            else:
                resource_bbrc_validator.append([
                    exp['project'], exp['ID'], exists, 0])

        return resource_bbrc_validator

    def tests_resource(self, res, name):
        """BBRC specifc test

        This method proces the json fetched from resource and convert
        it to dictionary

        Args:
            res (Resource): Resource object of pyxnat
            name (String): Name of the validator

        Returns:
            dict: A dictionary of tests
        """
        # Method from pyxnat_bbrc branch. This method get the resource
        # name and fetches the json file associated with the resource

        j = [e for e in list(res.files('{}*.json'.format(name)))][0]
        j = json.loads(res._intf.get(j._uri).text)

        # Return dict with tests details
        return j
