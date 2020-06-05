from pyxnat_connection import data_fetcher


class GetInfo:

    fetcher_object = None

    def __init__(self, user, password, server):

        self.fetcher_object = data_fetcher.Fetcher(user,
                                                   password,
                                                   server)

    def __preprocessor(self):

        '''
        This preprocessor makes the final dictionary with each key representing
        a graph.
        In return data each key and value pair represent a graph.
        If the key and value doesn't represent a graph further processing will
        be done.
        In the current case only 4 key and value pair have this structure:
        Number of projects
        Number of subjects
        Number of experiments
        Number of scans

        Return type of this function is a single dictionary with each key and
        value pair representing graph.
        '''

        stats = {}
        # preprocessing required in project data for number of projects
        projects_details = self.fetcher_object.get_projects_details()
        stats['Projects'] = projects_details['number_of_projects']
        del projects_details['number_of_projects']

        # Pre processing for subject details required
        subjects_details = self.fetcher_object.get_subjects_details()
        stats['Subjects'] = subjects_details['number_of_subjects']
        del subjects_details['number_of_subjects']

        # No need in pre processing experiment details
        experiments_details = self.fetcher_object.get_experiments_details()
        stats['Experiments'] = experiments_details['number_of_experiments']
        del experiments_details['number_of_experiments']

        # No need in pre processing scans details
        scans_details = self.fetcher_object.get_scans_details()
        stats['Scans'] = scans_details['number_of_scans']
        del scans_details['number_of_scans']

        stat_final = {'Stats': stats}

        final_json_dict = {}

        final_json_dict.update(stat_final)
        final_json_dict.update(projects_details)
        final_json_dict.update(subjects_details)
        final_json_dict.update(experiments_details)
        final_json_dict.update(scans_details)

        # Final dictionary which will act as a json file
        return final_json_dict

    def get_info(self):

        return self.__preprocessor()
