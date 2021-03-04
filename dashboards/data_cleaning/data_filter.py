import pandas as pd
import os.path as op
from collections import OrderedDict
import dashboards
fp = op.join(op.dirname(dashboards.__file__), '..', 'whitelist.xlsx')


class DataFilter:

    def __init__(self, username, p, role, visible_projects,
                 resources):

        self.visible_projects = visible_projects
        self.username = username
        self.longitudinal_data = p['longitudinal_data']

        projects = [pr for pr in p['projects'] if pr['id'] in visible_projects
                    or "*" in visible_projects]
        experiments = [e for e in p['experiments'] if e['project'] in visible_projects
                       or "*" in visible_projects]
        scans = [s for s in p['scans'] if s['project'] in visible_projects
                 or "*" in visible_projects]
        subjects = [s for s in p['subjects'] if s['project'] in visible_projects
                    or "*" in visible_projects]

        self.data = {}
        self.data['projects'] = projects
        self.data['subjects'] = subjects
        self.data['experiments'] = experiments
        self.data['scans'] = scans

        self.resources = {}
        resources_list = []

        if resources is not None:
            for resource in resources:
                project = resource[0]
                if project not in visible_projects or "*" in visible_projects:
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
        projects_details = self.get_projects_details(self.data['projects'])
        # If some error in connection 1 will be returned and we will
        # not go further
        if not isinstance(projects_details, int):
            stats['Projects'] = projects_details['Number of Projects']
            del projects_details['Number of Projects']
        else:
            return projects_details

        # Pre processing for subject details required
        subjects_details = self.get_subjects_details(self.data['subjects'])
        if subjects_details != 1:
            stats['Subjects'] = subjects_details['Number of Subjects']
            del subjects_details['Number of Subjects']

        # Pre processing experiment details
        experiments_details = self.get_experiments_details(self.data['experiments'])

        if experiments_details != 1:
            stats['Experiments'] = experiments_details['Number of Experiments']
            del experiments_details['Number of Experiments']

        # Pre processing scans details
        scans_details = self.get_scans_details(self.data['scans'])
        if scans_details != 1:
            stats['Scans'] = scans_details['Number of Scans']
            del scans_details['Number of Scans']
            del scans_details['Scans per session']
            del scans_details['Scan Types']

        stat_final = {'Stats': stats}

        ordered_graphs.update(projects_details)
        ordered_graphs.update(subjects_details)
        ordered_graphs.update(experiments_details)
        ordered_graphs.update(scans_details)
        ordered_graphs.update(stat_final)

        resources = self.get_resources_details(self.resources)

        if resources is not None and\
                not isinstance(resources, int) and self.resources != []:

            ordered_graphs.update(resources)

        l_data = self.get_longitudinal_data(self.longitudinal_data)
        ordered_graphs.update(l_data)

        return ordered_graphs

    def get_project_list(self):
        """This is used for creating project list

        Returns:
            list: List of projects
        """
        return self.get_projects_details_specific(self.data['projects'])

    def get_projects_details(self, projects):
        """Method to process all details related to project

        This method process all project details, that are present
        in a list by looping through each project and formatting it.

        Args:
            projects (dict): A list of projects with different information
                of project

        Returns:
            dict: A dict with keys of different keys corresponding to different
            project related graphs, or metrics.

            For each graph this format is used
            {"count": {"x": "y"}, "list": {"x": "list"}}

            "count" represent the count for the x_value and "list" represent
            "Different values" for x_values
        """
        if isinstance(projects, int):
            return projects

        projects_details = {}

        # key id_type is used by frontend to add appropriate urls in frontend
        project_acccess = self.dict_generator_overview(
            projects, 'project_access', 'id', 'access')
        project_acccess['id_type'] = 'project'

        projects_details['Number of Projects'] = len(projects)
        projects_details['Projects'] = project_acccess

        return projects_details

    def get_subjects_details(self, subjects_data):
        """Method to process all details related to Subject

        This method process all subject details, that are present
        in a list by looping through each subject and formatting it.

        Args:
            Subjects (dict): A list of each subject having
                its age, ID, Project ID, handedness, gender.
        Returns:
            dict: A dict with keys of different keys corresponding to different
            subject related graphs, or metrics.

            For each graph this format is used
            {"count": {"x": "y"}, "list": {"x": "list"}}

            "count" represent the count for the x_value and "list" represent
            "Different values" for x_values
        """
        if isinstance(subjects_data, int):
            return subjects_data

        subjects_details = {}

        # Subjects per project information

        subjects_per_project = self.dict_generator_per_view(
            subjects_data, 'project', 'ID', 'spp')
        subjects_per_project['id_type'] = 'subject'

        # Number of subjects information
        subjects_details['Number of Subjects'] = len(subjects_data)
        subjects_details['Subjects'] = subjects_per_project

        return subjects_details

    def get_experiments_details(self, experiments):
        """Method to process all details related to Experiment

        This method process all experiment details, that are present
        in a list by looping through each experiment and formatting it.

        Args:
            experiments (dict): A list of experiment with each
                having its ID, Project ID, experiment type

        Returns:
            dict: A dict with keys of different keys corresponding to different
            experiment related graphs, or metrics.

            For each graph this format is used
            {"count": {"x": "y"}, "list": {"x": "list"}}

            "count" represent the count for the x_value and "list" represent
            "Different values" for x_values
        """
        if isinstance(experiments, int):
            return experiments

        experiments_details = {}

        experiments_details['Number of Experiments'] = len(experiments)

        # Experiments type information

        experiment_type = self.dict_generator_overview(
            experiments, 'xsiType', 'ID', 'xsiType')
        experiment_type['id_type'] = 'experiment'

        experiments_types_per_project = self.dict_generator_per_view_stacked(
            experiments, 'project', 'xsiType', 'ID')
        experiments_types_per_project['id_type'] = 'experiment'

        prop_exp = self.proportion_graphs(
            experiments, 'subject_ID', 'ID', 'Subjects with ', ' experiment(s)')
        prop_exp['id_type'] = 'subject'

        experiments_details['Imaging sessions'] =\
            experiments_types_per_project

        experiments_details['Total amount of sessions'] = experiment_type
        experiments_details['Sessions per subject'] = prop_exp

        return experiments_details

    def get_scans_details(self, scans):
        """Method to process all details related to scan

        This method process all scan details, that are present
        in a list by looping through each scan and formatting it.

        Args:
            scans (dict): A list of scans with each scan
                having its project ID, scan ID, subject ID, experiment ID,
                scan type and scan quality.

        Returns:
            dict: A dict with keys of different keys corresponding to different
            scan related graphs, or metrics.

            For each graph this format is used
            {"count": {"x": "y"}, "list": {"x": "list"}}

            "count" represent the count for the x_value and "list" represent
            "Different values" for x_values
        """
        if isinstance(scans, int):
            return scans

        scan_quality = self.dict_generator_overview(
            scans, 'xnat:imagescandata/quality', 'ID',
            'quality', 'xnat:imagescandata/id')
        scan_quality['id_type'] = 'experiment'

        # Scans type information
        excel = pd.read_excel(fp, engine='openpyxl')
        whitelist = list(excel['scan_type'])
        filtered_scans = []
        for s in scans:
            if s['xnat:imagescandata/type'] in whitelist:
                filtered_scans.append(s)

        type_dict = self.dict_generator_overview(
            filtered_scans, 'xnat:imagescandata/type',
            'ID', 'type', 'xnat:imagescandata/id')
        type_dict['id_type'] = 'experiment'

        prop_scan = self.proportion_graphs(
            scans, 'ID',
            'xnat:imagescandata/id', '', ' scans')
        prop_scan['id_type'] = 'subject'

        scans_details = {}

        scans_details['Scan quality'] = scan_quality
        scans_details['Scan Types'] = type_dict
        scans_details['Scans per session'] = prop_scan
        scans_details['Number of Scans'] = len(scans)

        return scans_details

    def get_projects_details_specific(self, projects):
        """This project process list of all projects.

        This generate list of projects that are visible to user

        Args:
            projects (list): List of projects with there details

        Returns:
            list: List of projects which are visible to user.
        """

        if projects is None:
            return 1

        project_list_all = [project['id'] for project in projects]

        list_data = {}
        list_data['project_list'] = project_list_all

        return list_data

    def get_resources_details(self, resources, project_id=None):
        """Resource processing

        This method process the resources that are saved as in pickle file.
        it generates the required format for each plot.

        Args:
            resources ( list, optional): Each resource have its corresponding
                ID, project ID, label and experiment id and by default
            it will be skipped and no graph of resources will be added.
            project_id (String, optional): For per project view, the project id
                by default it will not return any project details.

        Returns:
            dict/int: If resource exist then a dict with the corresponding data
                else -1.

            For each graph this format is used
            {"count": {"x": "y"}, "list": {"x": "list"}}
        """
        df = pd.DataFrame(resources,
                          columns=['project', 'session', 'resource', 'label'])

        # Resource types
        resource_types = self.dict_generator_resources(df, 'label', 'session')
        resource_types['id_type'] = 'experiment'

        resource_type_ps = self.dict_generator_resources(
            df, 'label', 'session')
        resource_type_ps['id_type'] = 'experiment'

        # Code for number of experiments having common
        # number of resources for each project

        pro_exp_list = [[item[0], item[1]] for item in resources]

        pro_exp_df = pd.DataFrame(
            pro_exp_list, columns=['project', 'session'])

        # Create a Dataframe that have 3 columns where
        # 1st column: project_x will have projects
        # 2nd column: session will have session details
        # 3rd column: project_y will have count of resources
        pro_exp_count = pro_exp_df.groupby('session').count().reset_index()
        project_session = pro_exp_df.drop_duplicates(subset="session")
        resource_count_df = pd.merge(
            project_session, pro_exp_count, on='session')

        resource_count_df['project_y'] = resource_count_df[
            'project_y'].astype(int)

        # Send the above created data from to dict_generator_per_view_stacked
        # This will create the format required for stacked plot
        resource_count_dict = self.dict_generator_per_view_stacked(
            resource_count_df, 'project_x', 'project_y', 'session')
        resource_count_dict['id_type'] = 'experiment'
        ordered = OrderedDict(sorted(resource_count_dict['count'].items(), key=lambda x: len(x[0]), reverse=True))
        ordered_ = {a: {str(c)+' Resources/Session': d for c, d in b.items()} for a, b in ordered.items()}
        resource_count_dict_ordered = {'count': ordered_, 'list': resource_count_dict['list']}

        return {
            'Resources per type': resource_types,
            'Resources per session': resource_count_dict_ordered}

    def get_longitudinal_data(self, l_data):
        return {'Resources (over time)': {'count': l_data}}

    def proportion_graphs(self, data, property_x, property_y, prefix, suffix):

        data_list = [[item[property_x], item[property_y]] for item in data]

        # Create a data frame
        df = pd.DataFrame(data_list, columns=['per_view', 'count'])

        # Group by property property_x as per_view and count
        df_proportion = df.groupby(
            'per_view', as_index=False).count().groupby('count').count()

        # Use count to group by property x
        df_proportion['list'] = df.groupby(
            'per_view', as_index=False).count().groupby(
                'count')['per_view'].apply(list)

        # Add prefix and suffix to count for easy understanding
        # Eg. Number of subject with 1 experiments
        # Here prefix is Number of subject with and suffix is experiments
        # and count is 1
        df_proportion.index = prefix + df_proportion.index.astype(str) + suffix

        return df_proportion.rename(columns={'per_view': 'count'}).to_dict()

    def dict_generator_resources(self, df, x_name, y_name):
        """Generate a dictionary from the data frame of resources
        in the format required for graphs

        Args:
            df (Datafrmae): A dataframe of resources
            x_name (Str): The name which will be on X axis of graph
            y_name (Str): The name which will be on Y axis of graph

        Returns:
            Dict: For each graph this format is used
            {"count": {"x": "y"}, "list": {"x": "list"}}
        """

        data = df[df[y_name] != 'No Data'][[
            x_name, y_name]]
        data = data.rename(columns={y_name: 'count'})
        data_df = data.groupby(
            x_name)['count'].apply(list)
        data = data.groupby(x_name).count()
        data['list'] = data_df
        data_dict = data.to_dict()

        return data_dict

    def dict_generator_overview(
            self, data, property_x, property_y, x_new, extra=None):
        """Generate a dictionary from the data list of project, subjects,
        experiments and scans in the format required for graphs.

        Args:
            data (list): List of projects or subjects or exp or scans
            property_x (str): The name which will be on X axis of graph
            property_y (str): The name which will be on Y axis of graph
            x_new (str): The new name which will be shown on X axis of graph
            extra (str, optional): Add another value to be concatenated
                in x_axis, when click on graph occurs. Useful when
                the x_axis values are not unique and by default will not
                be used for concatenation.

        Returns:
            Dict: For each graph this format is used
            {"count": {"x": "y"}, "list": {"x": "list"}}
        """

        property_list = []
        property_none = []

        for item in data:
            if item[property_x] != '':
                if extra is None:
                    property_list.append([item[property_x], item[property_y]])
                else:
                    property_list.append(
                        [
                            item[property_x],
                            item[property_y] + '/' + item[extra]])
            else:
                if extra is None:
                    property_none.append(item[property_y])
                else:
                    property_none.append(item[property_y] + '/' + item[extra])

        property_df = pd.DataFrame(
            property_list, columns=[x_new, 'count'])

        property_df_series = property_df.groupby(
            x_new)['count'].apply(list)
        property_final_df = property_df.groupby(x_new).count()
        property_final_df['list'] = property_df_series
        property_dict = property_final_df.to_dict()

        if len(property_none) != 0:
            property_dict['count'].update({'No Data': len(property_none)})
            property_dict['list'].update({'No Data': property_none})

        return property_dict

    def dict_generator_per_view(
            self, data, property_x, property_y, x_new):
        """Generate a dictionary from the data list of subjects,
        experiments and scans in the format required for graphs.
        The generated data is only for single project.

        Args:
            data (list): List of projects or subjects or exp or scans
            property_x (str): The name which will be on X axis of graph
            property_y (str): The name which will be on Y axis of graph
            x_new (str): The new name which will be shown on X axis of graph

        Returns:
             Dict: For each graph this format is used
                {"count": {"x": "y"}, "list": {"x": "list"}}
        """
        per_list = [[item[property_x], item[property_y]] for item in data]

        per_df = pd.DataFrame(per_list, columns=[x_new, 'count'])
        per_df_series = per_df.groupby(x_new)['count'].apply(list)
        per_df = per_df.groupby(x_new).count()
        per_df['list'] = per_df_series

        per_view = per_df.to_dict()

        return per_view

    def dict_generator_per_view_stacked(
            self, data, property_x, property_y, property_z):
        """Generate dict format that is used by plotly for stacked graphs view,
        data like project details, scan, experiments, subject as field

        property_x and property_y are used to group by the pandas data frame
        and both are used on x axis values while property_z is used on y axis.
        Args:
            data (list): List of data project, subject, scan and experiments
            property_x (str): The name which will be on X axis of graph
            property_y (str): The name which will be on X axis of graph
            property_z (str): The name which will be on Y axis of graph

        Returns:
            dict:{count:{prop_x:{prop_y:prop_z_count}},
            list:{prop_x:{prop_y:prop_z_list}}
            }
        """
        if isinstance(data, list):

            per_list = [[
                item[property_x], item[property_y],
                item[property_z]] for item in data]

            per_df = pd.DataFrame(
                per_list, columns=[property_x, property_y, property_z])
        else:
            per_df = data

        per_df_series = per_df.groupby(
            [property_x, property_y])[property_z].apply(list)

        per_df = per_df.groupby([property_x, property_y]).count()
        per_df['list'] = per_df_series

        dict_tupled = per_df.to_dict()

        dict_output_list = {}
        for item in dict_tupled['list']:
            dict_output_list[item[0]] = {}

        for item in dict_tupled['list']:
            dict_output_list[
                item[0]].update({item[1]: dict_tupled['list'][item]})

        dict_output_count = {}

        for item in dict_tupled[property_z]:
            dict_output_count[item[0]] = {}

        for item in dict_tupled[property_z]:
            dict_output_count[
                item[0]].update({item[1]: dict_tupled[property_z][item]})

        return {'count': dict_output_count, 'list': dict_output_list}


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
        data (list): list of project, subjects, exp., scans
        project_id (str): ID of project in per project view.
        role (str): role of the user.
        project_visible (list): list of projects that is visible
        resources (list, optional): List of resources and by default
            it will be skipped and no graph of resources will be added.
    """

    def __init__(self, username, p, project_id, role,
                 project_visible, resources=None):

        # self.formatter_object_per_project = dfo.FormatterPP(
        #     project_id)
        self.project_id = project_id
        self.data = p
        self.project_visible = project_visible
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
        projects_details = self.get_projects_details(self.data['projects'])

        # Pre processing for subject details required
        subjects_details = self.get_subjects_details(self.data['subjects'])

        if subjects_details != 1:
            stats['Subjects'] = subjects_details['Number of Subjects']
            del subjects_details['Number of Subjects']

        # Pre processing experiment details
        experiments_details = self.get_experiments_details(self.data['experiments'])

        if experiments_details != 1:
            stats['Experiments'] = experiments_details['Number of Experiments']
            del experiments_details['Number of Experiments']
            del experiments_details['Total amount of sessions']
            if 'Sessions types/Project' in experiments_details:
                del experiments_details['Sessions types/Project']

        # Pre processing scans details
        scans_details = self.get_scans_details(self.data['scans'])

        if scans_details != 1:
            stats['Scans'] = scans_details['Number of Scans']
            del scans_details['Number of Scans']

        stat_final = {'Stats': stats}

        ordered_graphs.update({'Project details': projects_details})
        ordered_graphs.update(subjects_details)
        ordered_graphs.update(experiments_details)
        ordered_graphs.update(scans_details)
        ordered_graphs.update(stat_final)

        return ordered_graphs

    def get_projects_details(self, projects):
        """Takes the project information and perform operation that
        are required for displaying details specific to the project.

        Args:
            projects (list): List of projects

        Returns:
            dict: Information of project formatted for better view.
        """
        # Returns data for per project view

        project_dict = {}

        for project in projects:

            if project['id'] == self.project_id:
                project_dict = project

        project_details = {}

        project_details['Owner(s)'] = project_dict['project_owners']\
            .split('<br/>')

        project_details['Collaborator(s)'] = project_dict['project_collabs']\
            .split('<br/>')
        if project_details['Collaborator(s)'][0] == '':
            project_details['Collaborator(s)'] = ['------']

        project_details['member(s)'] = project_dict['project_members']\
            .split('<br/>')
        if project_details['member(s)'][0] == '':
            project_details['member(s)'] = ['------']

        project_details['user(s)'] = project_dict['project_users']\
            .split('<br/>')
        if project_details['user(s)'][0] == '':
            project_details['user(s)'] = ['------']

        project_details['last_accessed(s)'] =\
            project_dict['project_last_access'].split('<br/>')

        project_details['insert_user(s)'] = project_dict['insert_user']

        project_details['insert_date'] = project_dict['insert_date']
        project_details['access'] = project_dict['project_access']
        project_details['name'] = project_dict['name']

        project_details['last_workflow'] =\
            project_dict['project_last_workflow']

        return project_details

    def get_subjects_details(self, subjects):
        """Calls the parent class method for processing the subjects
        details and removing extra information for per project view.

        Args:
            subjects (list): List of subjects.

        Returns:
            dict: For each graph this format is used
            {"count": {"x": "y"}, "list": {"x": "list"}}
        """
        subjects_data = []

        for subject in subjects:
            if subject['project'] == self.project_id:
                subjects_data.append(subject)

        # Using code from the parent class for processing
        subjects_details = super().get_subjects_details(subjects_data)
        # Delete Subject/Project plot as this is present in counter of
        # per project view
        del subjects_details['Subjects']

        return subjects_details

    def get_experiments_details(self, experiments_data):
        """Calls the parent class method for processing the experiment
        details and removing extra information for per project view.

        Args:
            experiments_data (list): List of experiments.

        Returns:
            dict: For each graph this format is used
            {"count": {"x": "y"}, "list": {"x": "list"}}
        """
        experiments = []

        for experiment in experiments_data:
            if experiment['project'] == self.project_id:
                experiments.append(experiment)

        # Using code from the parent class for processing
        experiments_details = super().get_experiments_details(experiments)
        del experiments_details['Imaging sessions']

        return experiments_details

    def get_scans_details(self, scans_data):
        """Calls the parent class method for processing the scan
        details and removing extra information for per project view.

        Args:
            scans_data (list): List of experiments.

        Returns:
            dict: For each graph this format is used
            {"count": {"x": "y"}, "list": {"x": "list"}}
        """
        scans = []

        for scan in scans_data:
            if scan['project'] == self.project_id:
                scans.append(scan)

        # Using code from the parent class for processing
        scans_details = super().get_scans_details(scans)

        return scans_details

    def get_resources_details(self, resources=None):
        """Calls the parent class method for processing the resource
        details and removing extra information for per project view.

        Args:
            resources (list, optional): List of resources and by default
            it will be skipped and no graph of resources will be added.
        Returns:
            dict/int: If no resource data present then return -1 else
            For each graph this format is used
            {"count": {"x": "y"}, "list": {"x": "list"}}
        """
        if resources is None:
            return None

        # Using code from the parent class for processing
        resources_out = super().get_resources_details(
            resources, self.project_id)

        if not isinstance(resources_out, int):
            if 'Resources per session' in resources_out:
                del resources_out['Resources per session']

        return resources_out
