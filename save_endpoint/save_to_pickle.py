import sys
import pickle
from os.path import dirname, abspath
from datetime import datetime
sys.path.insert(0, dirname(dirname(abspath(__file__))))
from pyxnat_interface import data_fetcher


class SaveToPk:

    coll_users_data = None
    coll_users = None
    fetcher = None

    def __init__(self, username, password, server, ssl):

        self.server = server
        self.fetcher = data_fetcher.Fetcher(
            username, password, server, ssl)
        self.save_to_PK()

    def save_to_PK(self):

        data_pro_sub_exp_sc = self.fetcher.fetch_all()
        data_res = self.fetcher.get_resources()
        data_res_bbrc = self.fetcher.get_experiment_resources()

        with open(
                'pickles/data/general.pickle',
                'wb') as handle:

            pickle.dump(
                {
                    'server': self.server,
                    'info': data_pro_sub_exp_sc,
                    'resources': data_res,
                    'resources_bbrc': data_res_bbrc
                },
                handle, protocol=pickle.HIGHEST_PROTOCOL)

        longitudnal_data = self.longitudnal_data_processing(
            data_pro_sub_exp_sc, data_res
        )

        user_data = {}

        with open(
                'pickles/data/general_longitudnal.pickle', 'rb') as handle:
            user_data = pickle.load(handle)

            if self.server != user_data['server']:
                print("Wrong server")
                return -1

        with open(
                'pickles/data/general_longitudnal.pickle',
                'wb') as handle:

            if user_data == {}:
                pickle.dump(
                    user_data.update({
                        'server': self.server,
                        'longitudnal_data': longitudnal_data
                    }),
                    handle, protocol=pickle.HIGHEST_PROTOCOL)
            else:
                pickle.dump(
                    user_data.update({
                        'longitudnal_data': longitudnal_data
                    }),
                    handle, protocol=pickle.HIGHEST_PROTOCOL)

    def longitudnal_data_processing(self, data_pro_sub_exp_sc, data_res):

        # Normal data processing
        longitudnal_data = {}

        now = datetime.now()
        dt = now.strftime("%d/%m/%Y")

        projects_number = {'list': {dt: []}}
        subjects_number = {'list': {dt: []}}
        experiments_number = {'list': {dt: []}}
        scans_number = {'list': {dt: []}}

        projects_number['count'] = {dt: len(data_pro_sub_exp_sc['projects'])}
        subjects_number['count'] = {dt: len(data_pro_sub_exp_sc['subjects'])}
        experiments_number['count'] =\
            {dt: len(data_pro_sub_exp_sc['experiments'])}
        scans_number['count'] = {dt: len(data_pro_sub_exp_sc['scans'])}

        for project in data_pro_sub_exp_sc['projects']:
            projects_number['list'][dt].append(project['id'])

        for subject in data_pro_sub_exp_sc['subjects']:
            subjects_number['list'][dt].append(subject['ID'])

        for experiment in data_pro_sub_exp_sc['experiments']:
            experiments_number['list'][dt].append(experiment['ID'])

        for scan in data_pro_sub_exp_sc['scans']:
            scans_number['list'][dt].append(scan['ID'])

        # Resource data processing

        resource_number = {'list': {dt: []}}

        for resource in data_res:
            if resource[2] != 'No Data':
                resource_number['list'][dt].append(
                    str(resource[1]) + '  ' + str(resource[2]))

        resource_number['count'] = {dt: len(resource_number['list'][dt])}

        longitudnal_data['project'] = projects_number
        longitudnal_data['subject'] = subjects_number
        longitudnal_data['experiment'] = experiments_number
        longitudnal_data['scan'] = scans_number
        longitudnal_data['resource'] = resource_number

        return longitudnal_data
