from xnat_dashboards.data_cleaning import data_formatter


class DataFilter:
    """
    It first filter out the data based on project ids
    that should not be visible to user based on role.

    It then sends the data to data formatter which
    format the data, then ordering is done using the
    DataFilter

    Args:
        username (str): Username
        pro_sub_exp_sc (list): list of project, subjects, exp., scans
        role (str): role of the user.
        project_visible (list): list of projects that is visible
            by default it will show no project details.
        resources (list, optional): List of resources and by default
            it will be skipped and no graph of resources will be added.
    """
    def __init__(
            self, username, pro_sub_exp_sc, role, project_visible=[],
            resources=None):

        self.formatter_object = data_formatter.Formatter()
        if project_visible != []:
            self.project_visible = project_visible[role]
        else:
            self.project_visible = []
        self.username = username
        self.filter_projects(pro_sub_exp_sc, resources)

    def filter_projects(self, info_f, resources):
        """This methods filters project, subject, scans,
        experiments and resources using project ids based
        on roles assigned to user.

        Args:
            info_f (dict): dict of projects, subjects, experiments and
                scans.
        Returns:
            dict: resources belonging to the project that
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

        self.pro_sub_exp_sc = {}

        self.pro_sub_exp_sc['projects'] = projects
        self.pro_sub_exp_sc['subjects'] = subjects
        self.pro_sub_exp_sc['experiments'] = experiments
        self.pro_sub_exp_sc['scans'] = scans

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

    def reorder_graphs(self):

        """
        This reorder the data as per requirements ie.
        if needed user can reorder and then return the dict.

        Returns:
            dict: information belonging to the
            project that should be visible as per role and user.
        """

        stats = {}
        ordered_graphs = {}

        # Preprocessing required in project data for number of projects
        projects_details = self.formatter_object.get_projects_details(
            self.pro_sub_exp_sc['projects'])
        # If some error in connection 1 will be returned and we will
        # not go further
        if not isinstance(projects_details, int):
            stats['Projects'] = projects_details['Number of Projects']
            del projects_details['Number of Projects']
        else:
            return projects_details

        # Pre processing for subject details required
        subjects_details = self.formatter_object.get_subjects_details(
            self.pro_sub_exp_sc['subjects'])
        if subjects_details != 1:
            stats['Subjects'] = subjects_details['Number of Subjects']
            del subjects_details['Number of Subjects']

        # Pre processing experiment details
        experiments_details = self.formatter_object.get_experiments_details(
            self.pro_sub_exp_sc['experiments'])

        if experiments_details != 1:
            stats['Experiments'] = experiments_details['Number of Experiments']
            del experiments_details['Number of Experiments']

        # Pre processing scans details
        scans_details = self.formatter_object.get_scans_details(
            self.pro_sub_exp_sc['scans'])
        if scans_details != 1:
            stats['Scans'] = scans_details['Number of Scans']
            del scans_details['Number of Scans']

        stat_final = {'Stats': stats}

        ordered_graphs.update(projects_details)
        ordered_graphs.update(subjects_details)
        ordered_graphs.update(experiments_details)
        ordered_graphs.update(scans_details)
        ordered_graphs.update(stat_final)

        resources = self.formatter_object.get_resources_details(
            self.resources)

        if resources is not None and\
                not isinstance(resources, int) and self.resources != []:

            ordered_graphs.update(resources)

        return ordered_graphs

    def get_project_list(self):
        """This is used for creating project list

        Returns:
            list: List of projects
        """
        return self.formatter_object.get_projects_details_specific(
            self.pro_sub_exp_sc['projects'], self.username)


class DataFilterPP(DataFilter):
    """DataFilterPP processes the for per project view.

    It first checks whether the project should be
    visible to users.
    Then sends the data to data formatter which
    format the data then ordering is done using the
    DataFilterPP

    Args:
        DataFilter (DataFilter): It inherits DataFilter.
        username (str): Username
        pro_sub_exp_sc (list): list of project, subjects, exp., scans
        project_id (str): ID of project in per project view.
        role (str): role of the user.
        project_visible (list): list of projects that is visible
        resources (list, optional): List of resources and by default
            it will be skipped and no graph of resources will be added.
    """

    def __init__(
            self,
            username,
            pro_sub_exp_sc, project_id, role, project_visible=[],
            resources=None):

        self.formatter_object_per_project = data_formatter.FormatterPP(
            project_id)
        self.pro_sub_exp_sc = pro_sub_exp_sc
        if project_visible != []:
            self.project_visible = project_visible[role]
        else:
            self.project_visible = []

        self.resources = resources
        self.username = username
        self.project_id = project_id

    def reorder_graphs_pp(self):

        """
        This preprocessor makes the dictionary with each key being
        used to create plots or other frontend stats.

        This checks which information to be sent to frontend per project
        view.

        return:
            dict: Data each key and value pair represent a graph.
            If the key and value doesn't represent a graph further
            processing will be done.

            {Graph1_name : { count:{x_axis_values: y_axis_values},
                            list:{x_axis_values: y_list} },
            Data_name: {other project view data to be sent to frontend}}
        """

        stats = {}
        ordered_graphs = {}

        # Preprocessing required in project data for number of projects
        projects_details = self.formatter_object_per_project.\
            get_projects_details(self.pro_sub_exp_sc['projects'])

        # Pre processing for subject details required
        subjects_details = self.formatter_object_per_project.\
            get_subjects_details(self.pro_sub_exp_sc['subjects'])

        if subjects_details != 1:
            stats['Subjects'] = subjects_details['Number of Subjects']
            del subjects_details['Number of Subjects']

        # Pre processing experiment details
        experiments_details = self.formatter_object_per_project.\
            get_experiments_details(self.pro_sub_exp_sc['experiments'])

        if experiments_details != 1:
            stats['Experiments'] = experiments_details['Number of Experiments']
            del experiments_details['Number of Experiments']
            if 'Sessions types/Project' in experiments_details:
                del experiments_details['Sessions types/Project']

        # Pre processing scans details
        scans_details = self.formatter_object_per_project.\
            get_scans_details(self.pro_sub_exp_sc['scans'])

        if scans_details != 1:
            stats['Scans'] = scans_details['Number of Scans']
            del scans_details['Number of Scans']

        stat_final = {'Stats': stats}

        ordered_graphs.update({'Project details': projects_details})
        ordered_graphs.update(subjects_details)
        ordered_graphs.update(experiments_details)
        ordered_graphs.update(scans_details)
        ordered_graphs.update(stat_final)

        if self.project_id in self.project_visible\
                or "*" in self.project_visible:
            return ordered_graphs
        else:
            return None
