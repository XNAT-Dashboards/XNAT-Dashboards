import pandas as pd
import os.path as op
from collections import OrderedDict
import dashboards


class DataFilter:

    def __init__(self, p, visible_projects):


        projects = [pr for pr in p['projects'] if pr['id'] in visible_projects
                    or "*" in visible_projects]
        experiments = [e for e in p['experiments'] if e['project'] in visible_projects
                       or "*" in visible_projects]
        scans = [s for s in p['scans'] if s['project'] in visible_projects
                 or "*" in visible_projects]
        subjects = [s for s in p['subjects'] if s['project'] in visible_projects
                    or "*" in visible_projects]

        resources = [e for e in p['resources'] if len(e) == 4]

        self.data = {}
        self.data['projects'] = projects
        self.data['subjects'] = subjects
        self.data['experiments'] = experiments
        self.data['scans'] = scans

        fr = [(project, a, b, c) for (project, a, b, c) in resources
              if project not in visible_projects or "*" in visible_projects]

        self.data['longitudinal_data'] = p['longitudinal_data']
        self.data['resources'] = fr

    def reorder_graphs(self):

        stats = {}
        ordered_graphs = {}

        # Preprocessing required in project data for number of projects
        projects_details = self.get_projects_details(self.data['projects'])
        # If some error in connection 1 will be returned and we will
        # not go further
        stats['Projects'] = projects_details['Number of Projects']
        del projects_details['Number of Projects']

        # Pre processing for subject details required
        subjects_details = self.get_subjects_details(self.data['subjects'])
        stats['Subjects'] = subjects_details['Number of Subjects']
        del subjects_details['Number of Subjects']

        # Pre processing experiment details
        experiments_details = self.get_experiments_details(self.data['experiments'])

        stats['Experiments'] = experiments_details['Number of Experiments']
        del experiments_details['Number of Experiments']

        # Pre processing scans details
        scans_details = self.get_scans_details(self.data['scans'])
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

        resources = self.get_resources_details(self.data['resources'])
        ordered_graphs.update(resources)

        d = {'Resources (over time)': {'count': self.data['longitudinal_data']}}
        ordered_graphs.update(d)

        return ordered_graphs

    def get_projects_details(self, projects):
        projects_details = {}

        # key id_type is used by frontend to add appropriate urls in frontend
        project_acccess = self.dict_generator_overview(
            projects, 'project_access', 'id', 'access')
        project_acccess['id_type'] = 'project'

        projects_details['Number of Projects'] = len(projects)
        projects_details['Projects'] = project_acccess

        return projects_details

    def get_subjects_details(self, subjects_data):

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


        columns = ['xnat:imagescandata/quality', 'ID', 'quality',
                   'xnat:imagescandata/id']
        scan_quality = self.dict_generator_overview(scans, *columns)
        scan_quality['id_type'] = 'experiment'

        # Scans type information
        fp = op.join(op.dirname(dashboards.__file__), '..', 'whitelist.xlsx')
        excel = pd.read_excel(fp, engine='openpyxl')
        whitelist = list(excel['scan_type'])

        filtered_scans = [s for s in scans if s['xnat:imagescandata/type'] in whitelist]

        columns = ['xnat:imagescandata/type', 'ID', 'type',
                   'xnat:imagescandata/id']
        type_dict = self.dict_generator_overview(filtered_scans, *columns)
        type_dict['id_type'] = 'experiment'

        prop_scan = self.proportion_graphs(scans, 'ID',
                                           'xnat:imagescandata/id',
                                           '', ' scans')
        prop_scan['id_type'] = 'subject'

        scans_details = {'Scan quality': scan_quality,
                         'Scan Types': type_dict,
                         'Scans per session': prop_scan,
                         'Number of Scans': len(scans)}
        return scans_details

    def get_resources_details(self, resources, project_id=None):

        df = pd.DataFrame(resources,
                          columns=['project', 'session', 'resource', 'label'])

        # Resource types
        resource_types = self.dict_generator_resources(df, 'label', 'session')
        resource_types['id_type'] = 'experiment'

        resource_type_ps = self.dict_generator_resources(
            df, 'label', 'session')
        resource_type_ps['id_type'] = 'experiment'

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

        return {'Resources per type': resource_types,
                'Resources per session': resource_count_dict_ordered}

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
                    i = [item[property_x],
                         item[property_y] + '/' + item[extra]]
                    property_list.append(i)
            else:
                if extra is None:
                    property_none.append(item[property_y])
                else:
                    property_none.append(item[property_y] + '/' + item[extra])

        property_df = pd.DataFrame(property_list, columns=[x_new, 'count'])

        property_df_series = property_df.groupby(x_new)['count'].apply(list)
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

    def dict_generator_per_view_stacked(self, data, property_x, property_y, property_z):
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

        per_df = data

        if isinstance(data, list):
            per_list = [[item[property_x], item[property_y], item[property_z]] for item in data]
            columns = [property_x, property_y, property_z]
            per_df = pd.DataFrame(per_list, columns=columns)

        per_df_series = per_df.groupby([property_x, property_y])[property_z].apply(list)

        per_df = per_df.groupby([property_x, property_y]).count()
        per_df['list'] = per_df_series

        dict_tupled = per_df.to_dict()

        dict_output_list = {}
        for item in dict_tupled['list']:
            dict_output_list[item[0]] = {}

        for item in dict_tupled['list']:
            d = {item[1]: dict_tupled['list'][item]}
            dict_output_list[item[0]].update(d)

        dict_output_count = {}

        for item in dict_tupled[property_z]:
            dict_output_count[item[0]] = {}

        for item in dict_tupled[property_z]:
            d = {item[1]: dict_tupled[property_z][item]}
            dict_output_count[item[0]].update(d)

        return {'count': dict_output_count, 'list': dict_output_list}


class DataFilterPP(DataFilter):
    def __init__(self):
        pass

    def reorder_graphs_pp(self, p, project_id):
        stats = {}

        # Preprocessing required in project data for number of projects
        pd = self.get_projects_details(p['projects'], project_id)

        # Pre processing for subject details required
        sd = self.get_subjects_details(p['subjects'], project_id)

        stats['Subjects'] = sd['Number of Subjects']
        del sd['Number of Subjects']

        # Pre processing experiment details
        ed = self.get_experiments_details(p['experiments'], project_id)

        stats['Experiments'] = ed['Number of Experiments']
        del ed['Number of Experiments']
        del ed['Total amount of sessions']
        if 'Sessions types/Project' in ed:
            del ed['Sessions types/Project']

        # Pre processing scans details
        scd = self.get_scans_details(p['scans'], project_id)
        stats['Scans'] = scd['Number of Scans']
        del scd['Number of Scans']

        stat_final = {'Stats': stats}
        ordered_graphs = {}

        ordered_graphs.update({'Project details': pd})
        ordered_graphs.update(sd)
        ordered_graphs.update(ed)
        ordered_graphs.update(scd)
        ordered_graphs.update(stat_final)
        print(ordered_graphs)

        return ordered_graphs

    def get_projects_details(self, projects, project_id):

        res = {}

        p = [e for e in projects if e['id'] == project_id][0]

        res['Owner(s)'] = p['project_owners'].split('<br/>')

        res['Collaborator(s)'] = p['project_collabs'].split('<br/>')
        if res['Collaborator(s)'][0] == '':
            res['Collaborator(s)'] = ['None']

        res['Member(s)'] = p['project_members'].split('<br/>')
        if res['Member(s)'][0] == '':
            res['Member(s)'] = ['None']

        res['User(s)'] = p['project_users'].split('<br/>')
        if res['User(s)'][0] == '':
            res['User(s)'] = ['None']

        res['last_accessed'] = p['project_last_access'].split('<br/>')

        for e in ['insert_user', 'insert_date', 'project_access', 'name',
                  'project_last_workflow']:
            res[e] = p[e]

        return res

    def get_subjects_details(self, subjects, project_id):
        d = [s for s in subjects if s['project'] == project_id]
        res = super().get_subjects_details(d)
        del res['Subjects']

        return res

    def get_experiments_details(self, experiments, project_id):
        d = [e for e in experiments if e['project'] == project_id]
        res = super().get_experiments_details(d)
        del res['Imaging sessions']

        return res

    def get_scans_details(self, scans, project_id):
        scans = [s for s in scans if s['project'] == project_id]
        res = super().get_scans_details(scans)
        return res

    def get_resources_details(self, resources, project_id):
        res = super().get_resources_details(resources, project_id)
        if 'Resources per session' in res:
            del res['Resources per session']

        return res
