from pyxnat_api import data_formatter_pp


class GetInfo:

    def __init__(self, user, password, server, ssl, project_id):

        self.formatter_object_pp = data_formatter_pp.Formatter(
            user,
            password,
            server,
            ssl,
            project_id)

    def __preprocessor_pp(self, project_id):

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
        projects_details = self.formatter_object_pp.get_projects_details()
        print(projects_details)
        # If some error in connection 1 will be returned and we will
        # not go further
        if type(projects_details) != int:
            sessionDetails = projects_details['Total Sessions']
            del projects_details['Total Sessions']
        else:
            return projects_details

        # Pre processing for subject details required
        subjects_details = self.formatter_object_pp.get_subjects_details()

        if subjects_details != 1:
            stats['Subjects'] = subjects_details['Number of Subjects']
            del subjects_details['Number of Subjects']

        # Pre processing experiment details
        experiments_details = self.formatter_object_pp.\
            get_experiments_details()

        if experiments_details != 1:
            stats['Experiments'] = experiments_details['Number of Experiments']
            del experiments_details['Number of Experiments']

        stats['Sessions'] = sessionDetails

        # Pre processing scans details
        scans_details = self.formatter_object_pp.\
            get_scans_details()

        if scans_details != 1:
            stats['Scans'] = scans_details['Number of Scans']
            del scans_details['Number of Scans']

        stat_final = {'Stats': stats}

        final_json_dict.update({
            'Imaging Sessions': projects_details['Imaging Sessions']})
        del projects_details['Imaging Sessions']
        final_json_dict.update({'Project details': projects_details})
        final_json_dict.update(subjects_details)
        final_json_dict.update(experiments_details)
        final_json_dict.update(scans_details)
        final_json_dict.update(stat_final)

        '''
        returns a nested dict
        {
            Graph1_name : { x_axis_values, y_axis_values},
            Graph2_name : { x_axis_values, y_axis_values},
            Graph3_name : { x_axis_values, y_axis_values},
            Graph4_name : { x_axis_values, y_axis_values},
        }
        '''

        return final_json_dict

    def get_pp_view(self, project_id):
        pp = self.__preprocessor_pp(project_id)
        print(pp)
        return pp
