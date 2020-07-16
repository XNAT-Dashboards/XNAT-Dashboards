import sys
import pickle
from os.path import dirname, abspath
from datetime import datetime
sys.path.insert(0, dirname(dirname(abspath(__file__))))
from pyxnat_interface import data_fetcher


class SaveToPk:

    username = ''
    coll_users_data = None
    coll_users = None

    def __init__(self, username, password, server, ssl):

        self.username = username
        self.fetcher = data_fetcher.Fetcher(username, password, server, ssl)

    def __save_to_db(self, info):

        try:
            date_time = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
            with open(
                'pickles/users_data/' + self.username + '.pickle',
                    'wb') as handle:

                pickle.dump(
                    {'username': self.username,
                     'time_date': date_time,
                     'info': info},
                    handle,
                    protocol=pickle.HIGHEST_PROTOCOL)

            print("Saved")
        except Exception:
            print(Exception.with_traceback())
            return 1000

    def save_data(self):

        info = self.fetcher.fetch_all()

        if type(info) != int:
            self.__save_to_db(info)
            return 0
        else:
            return info

    def save_user(self, username, password, server, ssl):

        with open('pickles/users/' + username + '.pickle', 'wb') as handle:
            pickle.dump(
                {'username': username,
                 'password': password,
                 'server': server,
                 'ssl': ssl},
                handle,
                protocol=pickle.HIGHEST_PROTOCOL)

    def save_resources(self, username, password, server, ssl):

        fetcher_long = data_fetcher.FetcherLong(
            username,
            password,
            server,
            ssl)

        resources_bbrc_validator = fetcher_long.get_experiment_resources()

        with open(
                'pickles/resources/' + username + 'bbrc.pickle',
                'wb') as handle:

            pickle.dump({
                'username': username,
                'resources_bbrc': resources_bbrc_validator},
                handle, protocol=pickle.HIGHEST_PROTOCOL)
