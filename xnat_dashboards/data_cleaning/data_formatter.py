import pandas as pd
import re


class Formatter:
    """Formatting Class.

    This class contains method that are used for formatting the data fetched
    from the pickle and sent to DataFilter class

    """
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
        projects_details['Projects Visibility'] = project_acccess

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

        # Subject age information

        age_list = []
        age_none = []

        for subject in subjects_data:
            if subject['age'] != '':
                if int(subject['age']) > 0 and int(subject['age']) < 130:
                    age_list.append([int(subject['age']), subject['ID']])
                else:
                    age_none.append(subject['ID'])
            else:
                age_none.append(subject['ID'])

        age_df = pd.DataFrame(age_list, columns=['age', 'count'])

        age_df['age'] = pd.cut(
            x=age_df['age'],
            bins=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 130],
            labels=['0-10', '10-20', '20-30', '30-40', '40-50', '50-60',
                    '60-70', '70-80', '80-90', '90-100', 'Above_100'])

        age_ranged = age_df.groupby('age')['count'].apply(list)
        age_final_df = age_df.groupby('age').count()
        age_final_df['list'] = age_ranged

        age_range = age_final_df.to_dict()

        age_range['count'].update({'No Data': len(age_none)})
        age_range['list'].update({'No Data': age_none})
        age_range['id_type'] = 'subject'
        # Age end

        # Subject handedness information

        handedness = self.dict_generator_overview(
            subjects_data, 'handedness', 'ID', 'handedness')
        handedness['id_type'] = 'subject'

        # Subject gender information

        gender = self.dict_generator_overview(
            subjects_data, 'gender', 'ID', 'gender')
        gender['id_type'] = 'subject'

        # Subjects per project information

        subjects_per_project = self.dict_generator_per_view(
            subjects_data, 'project', 'ID', 'spp')
        subjects_per_project['id_type'] = 'subject'

        # Number of subjects information
        subjects_details['Number of Subjects'] = len(subjects_data)

        subjects_details['Subjects/Project'] = subjects_per_project
        subjects_details['Age Range'] = age_range
        subjects_details['Gender'] = gender
        subjects_details['Handedness'] = handedness

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

        # Experiments per project information

        experiments_per_project = self.dict_generator_per_view(
            experiments, 'project', 'ID', 'epp')
        experiments_per_project['id_type'] = 'experiment'

        # Experiments type information

        experiment_type = self.dict_generator_overview(
            experiments, 'xsiType', 'ID', 'xsiType')
        experiment_type['id_type'] = 'experiment'

        experiments_types_per_project = self.dict_generator_per_view_stacked(
            experiments, 'project', 'xsiType', 'ID')
        experiments_types_per_project['id_type'] = 'experiment'

        prop_exp = self.proportion_graphs(
            experiments, 'subject_ID', 'ID', 'Subjects with ', ' experiment')
        prop_exp['id_type'] = 'subject'

        experiments_details['Sessions types/Project'] =\
            experiments_types_per_project

        experiments_details['Experiment Types'] = experiment_type
        experiments_details['Experiments/Project'] = experiments_per_project
        experiments_details['Experiments Proportions'] = prop_exp

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

        type_dict = self.dict_generator_overview(
            scans, 'xnat:imagescandata/type',
            'ID', 'type', 'xnat:imagescandata/id')
        type_dict['id_type'] = 'experiment'

        # Scans xsi type information

        xsi_type_dict = self.dict_generator_overview(
            scans, 'xsiType', 'ID', 'xsiType', 'xnat:imagescandata/id')
        xsi_type_dict['id_type'] = 'experiment'

        # Scans per project information

        scans_per_project = self.dict_generator_overview(
            scans, 'project', 'ID', 'spp', 'xnat:imagescandata/id')
        scans_per_project['id_type'] = 'experiment'

        prop_scan = self.proportion_graphs(
            scans, 'xnat:imagesessiondata/subject_id',
            'ID', 'Subjects with ', ' scans')
        prop_scan['id_type'] = 'subject'

        scans_details = {}

        scans_details['Scans Quality'] = scan_quality
        scans_details['Scan Types'] = type_dict
        scans_details['XSI Scan Types'] = xsi_type_dict
        scans_details['Scans/Project'] = scans_per_project
        scans_details['Scans Proportions'] = prop_scan
        scans_details['Number of Scans'] = len(scans)

        return scans_details

    def get_projects_details_specific(self, projects, name):
        """This project process list of all projects.

        This generate list of projects that are visible to user and
        the list of projects owned, collaborated or member.

        Args:
            projects (list): List of projects with there details
            name (String): Name of the user

        Returns:
            list: List of projects which are visible to user.
        """

        if projects is None:
            return 1

        project_list_owned_collab_member = []

        for project in projects:
            project_owner = project['project_owners']
            project_collabs = project['project_collabs']
            project_member = project['project_members']
            user = name

            if project_owner.find(user) != -1\
               or project_collabs.find(user) != -1\
               or project_member.find(user) != -1:
                project_list_owned_collab_member.append(project['id'])

        project_list_all = [project['id'] for project in projects]

        list_data = {}
        list_data['project_list'] = project_list_all
        list_data['project_list_ow_co_me'] = project_list_owned_collab_member

        return list_data

    def get_resources_details(
            self, resources=None, project_id=None):
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

        if resources is None:
            return None

        df = pd.DataFrame(
            resources,
            columns=['project', 'session', 'resource', 'label'])

        if project_id is not None:   # Code for per project view

            try:

                df = df.groupby(['project']).get_group(project_id)

            except KeyError:

                return -1

        df['resource'] = df['resource'].map(
            lambda x: re.sub('<Resource Object>', 'Resource Object', str(x)))

        resource_pp = df[df['resource'] != 'No Data'][['project', 'resource']]
        session = df[df['resource'] != 'No Data']['session']
        resource_pp['resource'] = session + '/' + resource_pp['resource']
        resource_pp = resource_pp.rename(columns={'resource': 'count'})
        resources_pp_df = resource_pp.groupby('project')['count'].apply(list)
        resource_pp = resource_pp.groupby('project').count()
        resource_pp['list'] = resources_pp_df
        resource_pp = resource_pp.to_dict()
        resource_pp['id_type'] = 'experiment'
        res_pp_no_data = df[
            df['resource'] == 'No Data'].groupby('project').count()

        # Creates 2 Dataframe
        # Data frame 1 have project which have resources
        # Data frame 2 have project which don't have resources
        # Subtract dataframe 1 from 2 if dataframe 2 have any project id
        # left then this means project id doesn't have any resource
        no_data_rpp = res_pp_no_data.index.difference(
            resources_pp_df.index).to_list()

        # Remove those project ID
        if len(no_data_rpp) != 0:

            no_data_update = {}

            for item in no_data_rpp:
                no_data_update[item] = 0

            resource_pp['count'].update(no_data_update)

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
            'project_y'].astype(str) + ' Resources/Session'

        # Send the above created data from to dict_generator_per_view_stacked
        # This will create the format required for stacked plot
        resource_count_dict = self.dict_generator_per_view_stacked(
            resource_count_df, 'project_x', 'project_y', 'session')
        resource_count_dict['id_type'] = 'experiment'

        return {
            'Resources/Project': resource_pp,
            'Resource Types': resource_types,
            'Session resource count/Project': resource_count_dict}

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


class FormatterPP(Formatter):
    """Formatting Class for per project view.

    This class contains method that are used for formatting the data fetched
    from the pickle and sent to DataFilter class.

    Args:
        Formatter (Formatter): Inherits formatter class.
        project_id (str): ID of the project, we want to process data.
    """

    # Initializing the central interface object in the constructor
    def __init__(self, project_id):

        self.project_id = project_id

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
        del subjects_details['Subjects/Project']

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
        # Delete Experiments/Project plot as this is present in counter of
        # per project view
        del experiments_details['Experiments/Project']

        # Experiments per subject information

        experiments_per_subject = super().dict_generator_per_view(
            experiments, 'subject_ID', 'ID', 'eps')
        experiments_per_subject['id_type'] = 'experiment'
        experiments_details['Experiments/Subject'] = experiments_per_subject

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
        # Delete Scans/Project plot as this is present in counter of
        # per project view
        del scans_details['Scans/Project']

        # Scans per subject information

        scans_per_subject = super().dict_generator_overview(
            scans, 'xnat:imagesessiondata/subject_id',
            'ID', 'sps', 'xnat:imagescandata/id')
        scans_per_subject['id_type'] = 'experiment'

        scans_details['Scans/Subject'] = scans_per_subject

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
            if 'Resources/Project' in resources_out:
                del resources_out['Resources/Project']
            if 'Session resource count/Project' in resources_out:
                del resources_out['Session resource count/Project']

        return resources_out
