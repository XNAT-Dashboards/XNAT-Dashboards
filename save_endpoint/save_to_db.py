from pymongo import MongoClient
import sys
import json
from os.path import dirname, abspath
from datetime import datetime
sys.path.insert(0, dirname(dirname(abspath(__file__))))
from pyxnat_interface import data_fetcher


class SaveToDb:

    username = ''
    coll_users_data = None
    coll_users = None

    def __init__(self, username, password, server, ssl, test):
        # Connecting to MongoDB using PyMongo

        try:
            with open('utils/db_config.json') as json_file:
                db_json = json.load(json_file)
        except OSError:
            print("db_json not found")
            exit(1)

        if test:
            client = MongoClient(db_json['test_url'])
            db = client[db_json['test_db']]
        else:
            client = MongoClient([db_json['url']])
            db = client[db_json['db']]

        self.coll_users_data = db['users_data']
        self.coll_users = db['users']
        self.coll_resources = db['resources']
        self.username = username
        self.fetcher = data_fetcher.Fetcher(username, password, server, ssl)

    def __save_to_db(self, info):

        try:
            date_time = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
            self.coll_users_data.insert({'username': self.username,
                                         'date:time': date_time,
                                         'info': info},
                                        check_keys=False)
            print("Saved")
        except Exception:
            print(Exception.with_traceback())

    def save_data(self):

        info = self.fetcher.fetch_all()

        if type(info) != int:
            self.__save_to_db(info)
            return 0
        else:
            return info

    def save_user(self, username, password, server, ssl):

        users = self.coll_users
        users.insert({'username': username,
                      'password': password,
                      'server': server,
                      'ssl': ssl})

    def save_resources(self, username, password, server, ssl):

        fetcher_long = data_fetcher.FetcherLong(
            username,
            password,
            server,
            ssl)

        resources = fetcher_long.get_resources()
        self.coll_resources.insert(
            {'username': username, 'resources': resources})

        exp_resources = fetcher_long.get_experiment_resources()

        self.coll_resources.insert(
            {'username': username + 'bbrc', 'resources': exp_resources})
