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
        final_json_dict = {}

        # Preprocessing required in project data for number of projects
        projects_details = self.fetcher_object.get_projects_details()
        # If some error in connection 1 will be returned and we will
        # not go further
        if(projects_details != 1):
            stats['Projects'] = projects_details['number_of_projects']
            del projects_details['number_of_projects']
            final_json_dict.update(projects_details)

        # Pre processing for subject details required
        subjects_details = self.fetcher_object.get_subjects_details()
        if(subjects_details != 1):
            stats['Subjects'] = subjects_details['number_of_subjects']
            del subjects_details['number_of_subjects']
            final_json_dict.update(subjects_details)

        # Pre processing experiment details
        experiments_details = self.fetcher_object.get_experiments_details()
        if(experiments_details != 1):
            stats['Experiments'] = experiments_details['number_of_experiments']
            del experiments_details['number_of_experiments']
            final_json_dict.update(experiments_details)

        # Pre processing scans details
        scans_details = self.fetcher_object.get_scans_details()
        if(scans_details != 1):
            stats['Scans'] = scans_details['number_of_scans']
            del scans_details['number_of_scans']
            final_json_dict.update(scans_details)

        stat_final = {'Stats': stats}

        final_json_dict.update(stat_final)

        return final_json_dict

    def get_info(self):

        return self.__preprocessor()
