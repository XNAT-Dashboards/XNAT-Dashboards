from xnat_dashboards.bbrc import data_formatter


class DataFilter:
    """
    It first filter out the bbrc resources based on project ids
    that should not be visible to user based on role.

    It then sends the data to data formatter which
    format the data then ordering is done using the
    DataFilter

    Args:
        role (str): role of the user.
        project_visible (list): list of projects that is visible
            by default it will show no project details.
        resources_bbrcc (list, optional): List of BBRC resources and by default
            it will be skipped and no graph of BBRC resources will be added.
    """
    def __init__(
            self, role, project_visible=[], resources_bbrc=None):

        self.formatter_object = data_formatter.Formatter()
        if project_visible != []:
            self.project_visible = project_visible[role]
        else:
            self.project_visible = []
        self.resources_preprocessor(resources_bbrc)

    def resources_preprocessor(self, resources_bbrc):
        """
        This is used to filter resources and bbrc resources
        using project ids based on roles assigned to user.
        Args:
            resources_bbrc (list): list of bbrc resources
        Returns:
            dict: bbrc resources that belongs to the
            project that should be visible as per role and user.
        """
        self.resources_bbrc = {}
        resources_bbrc_list = []

        # Loop through each resources and resources bbrc and check its project
        # id present for the role or role containting *

        if resources_bbrc is not None:

            for resource in resources_bbrc:
                if resource[0] not in self.project_visible\
                        or "*" in self.project_visible:
                    resources_bbrc_list.append(resource)

        self.resources_bbrc = resources_bbrc_list

    def graphs_reordering(self):

        """
        This reorder the data as per requirements that is
        if needed user can reorder and then return the dict.

        Returns:
            dict: bbrc resources information that belongs to the
            project should be visible as per role of the user.
        """

        final_json_dict = {}

        resources = data_formatter.Formatter().get_resource_details(
            self.resources_bbrc)

        if resources is not None and\
                not isinstance(resources, int):

            final_json_dict.update(resources)

        return final_json_dict

    def get_overview(self):
        """This sends data back to Graph Generator class present in
        pyxnat interface.

        Returns:
            dict: This returns a dict with all the information regarding
                overview page.
        """
        return self.graphs_reordering()


class DataFilterPP(DataFilter):
    """DataFilterPP processes the for per project view.

    It first checks whether the project should be
    visible to users.
    if it should be visible then further proceed else return
    None.
    Then sends the data to data formatter which
    format the data then ordering is done using the
    DataFilterPP

    Args:
        DataFilter (DataFilter): It inherits DataFilter.
        experiments (list): List of experiments present in project.
        project_id (str): ID of project in per project view.
        role (str): role of the user.
        project_visible (list): list of projects that is visible
        resources_bbrc (list, optional): List of bbrc resources
            and Default as None and by default
            it will be skipped and no graph of resources will be added.
    """

    def __init__(
            self,
            experiments, project_id, role, project_visible=[],
            resources_bbrc=None):

        self.formatter_object_per_project = data_formatter.Formatter()
        if project_visible != []:
            self.project_visible = project_visible[role]
        else:
            self.project_visible = []

        self.experiments = experiments
        self.project_id = project_id
        self.resources_bbrc = resources_bbrc

    def graphs_reordering_pp(self):

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
            Data_name: {other informations to be sent to frontend}}
        """

        final_json_dict = {}

        resources = self.formatter_object_per_project.get_resource_details(
            self.resources_bbrc, self.project_id)

        test_grid = self.formatter_object_per_project.generate_test_grid_bbrc(
            self.resources_bbrc, self.project_id)

        if not isinstance(resources, int) and resources is not None:
            final_json_dict.update(resources)

        diff_dates = self.formatter_object_per_project.diff_dates(
            self.resources_bbrc, self.experiments, self.project_id)

        if diff_dates is not None and diff_dates['count'] != {}:
            final_json_dict.update({'Dates Diff': diff_dates})

        final_json_dict.update({'test_grid': test_grid})

        return final_json_dict

    def get_per_project_view(self):
        """
        This sends the data to Graph per project view by first getting
        data from graph_reordering.

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
