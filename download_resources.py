from pyxnat_interface import data_fetcher
import json
import pickle
import argparse


class DownloadData:

    def __init__(self, path):

        self.role = path

    def iter_users(self):

        with open(self.role) as json_file:
            user = json.load(json_file)

        self.__save_to_PK(
            user['username'], user['password'],
            user['server'], user['ssl'])

        print("saved")

    def __save_to_PK(self, username, password, server, ssl):

        fetcher = data_fetcher.Fetcher(username, password, server, ssl)
        fetcher_long = data_fetcher.FetcherLong(
            username, password, server, ssl)

        data_pro_sub_exp_sc = fetcher.fetch_all()
        data_res = fetcher_long.get_resources()
        data_res_bbrc = fetcher_long.get_experiment_resources()

        with open(
                'pickles/data/general.pickle',
                'wb') as handle:

            pickle.dump(
                {
                    'server': server,
                    'info': data_pro_sub_exp_sc,
                    'resources': data_res,
                    'resources_bbrc': data_res_bbrc
                },
                handle, protocol=pickle.HIGHEST_PROTOCOL)


ap = argparse.ArgumentParser()
ap.add_argument("-p", "--path", type=str, help="Path to user name.json")

args = vars(ap.parse_args())

if __name__ == "__main__":

    download_data_object = DownloadData(args['path'])
    download_data_object.iter_users()
