from xnat_dashboards.data_cleaning import data_formatter


class DataFilter:
    """
    It first filter out the data based on project ids
    that should not be visible to user based on role.

    It then sends the data to data formatter which
    format the data then ordering is done using the
    GetInfo

    Args:
        username (str): Username
        info (list): list of project, subjects, exp., scans
        role (str): role of the user.
        project_visible (list): list of projects that is visible
            by default it will show no project details.
        resources (list, optional): List of resources and by default
            it will be skipped and no graph of resources will be added.
    """
    def __init__(
            self, username, info, role, project_visible=[],
            resources=None):

        self.formatter_object = data_formatter.Formatter()
        if project_visible != []:
            self.project_visible = project_visible[role]
        else:
            self.project_visible = []
        self.username = username
        self.filter_projects(info, resources)

    def filter_projects(self, info_f, resources):
        """This methods filters project, subject, scans and
        experiments based on project id that should be visible
        to user.

        Args:
            info_f (dict): dict of projects, subjects, experiments and
                scans.
        Returns:
            dict: resources that belongs to the project that
                should be visible as per role and user.
        """
        # Method to restrict access to projects details
        # based on role of the user

        projects_f = info_f['projects']
        subjects_f = info_f['subjects']
        experiments_f = info_f['experiments']
        scans_f = info_f['scans']

        scans = []
        experiments = []
        subjects = []
        projects = []

        # Loop through each project and check id with each
        # id present for the role or role containting *
        for project in projects_f:
            if project['id'] in self.project_visible\
                    or "*" in self.project_visible:
                projects.append(project)

        # Loop through each subjects, experiments, scans and check it's project
        # id present for the role or role containting *
        for experiment in experiments_f:
            if experiment['project'] in self.project_visible\
                    or "*" in self.project_visible:
                experiments.append(experiment)

        for scan in scans_f:
            if scan['project'] in self.project_visible\
                    or "*" in self.project_visible:
                scans.append(scan)

        for subject in subjects_f:
            if subject['project'] in self.project_visible\
                    or "*" in self.project_visible:
                subjects.append(subject)

        self.info = {}

        self.info['projects'] = projects
        self.info['subjects'] = subjects
        self.info['experiments'] = experiments
        self.info['scans'] = scans

        self.resources = {}
        resources_list = []

        # Loop through each resources and check it's project
        # id present for the role or role containting *

        if resources is not None:

            for resource in resources:
                if resource[0] not in self.project_visible\
                        or "*" in self.project_visible:
                    resources_list.append(resource)

        self.resources = resources_list

    def graphs_reordering(self):

        """
        This reorder the data as per requirements.

        Returns:
            dict: data information that belongs to the
            project that should be visible as per role and user.
        """

        stats = {}
        final_json_dict = {}

        # Preprocessing required in project data for number of projects
        projects_details = self.formatter_object.get_projects_details(
            self.info['projects'])
        # If some error in connection 1 will be returned and we will
        # not go further
        if type(projects_details) != int:
            stats['Projects'] = projects_details['Number of Projects']
            del projects_details['Number of Projects']
        else:
            return projects_details

        # Pre processing for subject details required
        subjects_details = self.formatter_object.get_subjects_details(
            self.info['subjects'])
        if subjects_details != 1:
            stats['Subjects'] = subjects_details['Number of Subjects']
            del subjects_details['Number of Subjects']

        # Pre processing experiment details
        experiments_details = self.formatter_object.get_experiments_details(
            self.info['experiments'])

        if experiments_details != 1:
            stats['Experiments'] = experiments_details['Number of Experiments']
            del experiments_details['Number of Experiments']

        # Pre processing scans details
        scans_details = self.formatter_object.get_scans_details(
            self.info['scans'])
        if scans_details != 1:
            stats['Scans'] = scans_details['Number of Scans']
            del scans_details['Number of Scans']

        stat_final = {'Stats': stats}

        final_json_dict.update(projects_details)
        final_json_dict.update(subjects_details)
        final_json_dict.update(experiments_details)
        final_json_dict.update(scans_details)
        final_json_dict.update(stat_final)

        resources = self.formatter_object.get_resources_details(
            self.resources)

        if resources is not None and\
                type(resources) != int and self.resources != []:

            final_json_dict.update(resources)

        return final_json_dict

    def get_project_list(self):
        """This is used for creating project list

        Returns:
            list: List of projects
        """
        return self.formatter_object.get_projects_details_specific(
            self.info['projects'], self.username)

    def get_info(self):
        """This sends data back to Graph Generator class.

        Returns:
            dict: This returns a dict with all the information regarding
                overview page.
        """
        return self.graphs_reordering()


class DataFilterPP(DataFilter):
    """DataFilterPP processes the for per project view.

    It first checks whether the project should be
    visible to users.
    Then sends the data to data formatter which
    format the data then ordering is done using the
    DataFilterPP

    Args:
        GetInfo (GetInfo): It inherits GetInfo.
        username (str): Username
        info (list): list of project, subjects, exp., scans
        project_id (str): ID of project in per project view.
        role (str): role of the user.
        project_visible (list): list of projects that is visible
        resources (list, optional): List of resources and by default
            it will be skipped and no graph of resources will be added.
    """

    def __init__(
            self,
            username,
            info, project_id, role, project_visible=[],
            resources=None):

        self.formatter_object_per_project = data_formatter.FormatterPP(
            project_id)
        self.info = info
        if project_visible != []:
            self.project_visible = project_visible[role]
        else:
            self.project_visible = []

        self.resources = resources
        self.username = username
        self.project_id = project_id

    def graphs_reordering_pp(self):

        """
        This preprocessor makes the final dictionary with each key being
        a part in graph view or a data view.

        This checks which information to be sent to frontend per project
        view.

        return:
            dict: Data each key and value pair represent a graph.
            If the key and value doesn't represent a graph further
            processing will be done.

            {Graph1_name : { count:{x_axis_values: y_axis_values},
                            list:{x_axis_values: y_list} },
            Data_name: {other informations to be sent to frontend}}
        """

        stats = {}
        final_json_dict = {}

        # Preprocessing required in project data for number of projects
        projects_details = self.formatter_object_per_project.\
            get_projects_details(self.info['projects'])

        # Pre processing for subject details required
        subjects_details = self.formatter_object_per_project.\
            get_subjects_details(self.info['subjects'])

        if subjects_details != 1:
            stats['Subjects'] = subjects_details['Number of Subjects']
            del subjects_details['Number of Subjects']

        # Pre processing experiment details
        experiments_details = self.formatter_object_per_project.\
            get_experiments_details(self.info['experiments'])

        if experiments_details != 1:
            stats['Experiments'] = experiments_details['Number of Experiments']
            del experiments_details['Number of Experiments']
            if 'Sessions types/Project' in experiments_details:
                del experiments_details['Sessions types/Project']

        # Pre processing scans details
        scans_details = self.formatter_object_per_project.\
            get_scans_details(self.info['scans'])

        if scans_details != 1:
            stats['Scans'] = scans_details['Number of Scans']
            del scans_details['Number of Scans']

        stat_final = {'Stats': stats}

        final_json_dict.update({'Project details': projects_details})
        final_json_dict.update(subjects_details)
        final_json_dict.update(experiments_details)
        final_json_dict.update(scans_details)
        final_json_dict.update(stat_final)

        return final_json_dict

    def get_per_project_view(self):
        """
        This sends the data to Graph per project view by first getting
        data from pre processor.

        return:
            dict/None: It sends dict if the project have information,
            if project don't have any information it will be None is set
            by default.

            {Graph1_name : { count:{x_axis_values: y_axis_values},
                            list:{x_axis_values: y_list} },
            Data_name: {other informations to be sent to frontend}}
        """
        # Checks if the project should be visible to user with the role

        if self.project_id in self.project_visible\
                or "*" in self.project_visible:
            return self.graphs_reordering_pp()
        else:
            return None
