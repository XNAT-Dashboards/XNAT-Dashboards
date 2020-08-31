from tqdm import tqdm
import pyxnat
import json
import logging
import urllib3


# Logging format
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
# Remove warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Fetcher:

    """
    This class is used for fetching resources that are present on
    BBRC XNAT instances.

    Args:
        path (String): Path to pyxnat configuration file.

    Attributes:
        selector: Pyxnat Interface object used in whole class for
            calling different methods of pyxnat
    """

    def __init__(self, config):

        selector = pyxnat.Interface(config=config)

        self.selector = selector

    def __del__(self):
        """Fetcher destructor
        Disconnect from the server after pyxnat object is destroyed
        """
        logging.info("Disconnected from XNAT instance")
        self.selector.disconnect()

    def get_resource(self, experiments):
        """Method specific to BBRC XNAT instance

        Special resource BBRC_Validator contains information
        of different test that are done on experiments. Loop through
        each experiment check if BBRC validator resource exist, if
        exist then check for archiving validator using test method.
        If archiving validator exist then save the json fetched from validator
        as dict with information of tests. If don't exist then use 'No Data' as
        an identifier.

        Freesurfer log file contains details for how log it ran on an
        experiment. That is also fetched for creating plots.

        Args:
            experiments (list): Gets the list of experiments with thier IDs
            used for fetching resources

        Returns:
            2D list: Each row of this have experiment id its corresponding
            project id, Whether BBRC data exist and Archiving details as dict
            if exists
        """
        # Get the list of all experiments
        resource_bbrc_validator = []

        for exp in tqdm(experiments):

            session_details = []
            # Check whether 'BBRC Validator' type resource exists
            # for the experiment

            BBRC_VALIDATOR = self.selector.select.experiment(
                exp['ID']).resource('BBRC_VALIDATOR')
            exists = BBRC_VALIDATOR.exists()
            # If exist then further process and check whether archiving
            # validator exist if exist then get the test json and if not
            # exists then Index error will be thrown and place 0 instead
            if exists:
                try:
                    session_details = [
                        exp['project'],
                        exp['ID'],
                        exists,
                        self.tests_resource(
                            BBRC_VALIDATOR, 'ArchivingValidator')]
                except IndexError:
                    session_details = [exp['project'], exp['ID'], exists, 0]
            else:
                session_details = [
                    exp['project'], exp['ID'], exists, 0]

            # Fetching free surfer details

            fs = self.selector.select.experiment(
                exp['ID']).resource('FREESURFER6')

            fs_exists = fs.exists()
            session_details.append(fs_exists)

            if fs_exists:
                try:
                    log_file = list(fs.files('*recon-all.log'))[0]
                    log_content = self.selector.get(log_file._uri).text
                    # Fetch the index of time using this string + its length
                    target_str = '#@#%# recon-all-run-time-hours '
                    index = log_content.find(target_str)
                    target = index+len(target_str)
                    # Some log files have 'recon-all -s' after time and
                    # some log files have 'Info:' after time.
                    # If 'Info:' exist then use this index else 'recon-all'
                    target_end_second = log_content.find('recon-all -s')
                    target_end_first = log_content.find(
                        'INFO: touching notification file')
                    if target_end_first == -1:
                        time_diff = log_content[target:target_end_second]
                    else:
                        time_diff = log_content[target:target_end_first]
                    session_details.append(time_diff)
                except IndexError:
                    session_details.append(None)
            else:
                session_details.append(None)

            resource_bbrc_validator.append(session_details)

        return resource_bbrc_validator

    def tests_resource(self, res, name):
        """BBRC specifc test

        This method process the json fetched from resource and convert
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
