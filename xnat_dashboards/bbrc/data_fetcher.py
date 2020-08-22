from tqdm import tqdm
import pyxnat
import json


class Fetcher:

    def __init__(self, config):

        selector = pyxnat.Interface(config=config)

        self.selector = selector

    def __del__(self):
        """Fetcher destructor
        Disconnect from the server after pyxnat object is destroyed
        """
        print("Disconnected")
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

            BBRC_VALIDATOR = self.selector.select.experiment(
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
