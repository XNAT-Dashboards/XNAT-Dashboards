import sys
import pickle
from os.path import dirname, abspath
sys.path.insert(0, dirname(dirname(abspath(__file__))))
from pyxnat_interface import data_fetcher


class SaveToPk:

    coll_users_data = None
    coll_users = None
    fetcher_long = None
    fetcher = None

    def __init__(self, username, password, server, ssl):

        self.server = server
        self.save_to_PK(username, password, server, ssl)

    def save_to_PK(self, username, password, server, ssl):

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
