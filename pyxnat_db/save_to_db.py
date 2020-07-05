from pymongo import MongoClient
import sys
import json
from os.path import dirname, abspath
from datetime import datetime
sys.path.insert(0, dirname(dirname(abspath(__file__))))
from pyxnat_api import get_info


class SaveToDb:

    username = ''
    coll_users_data = None
    coll_users = None

    def __init__(self, username, password, server, ssl, test):
        # Connecting to MySQL server at localhost using PyMySQL DBAPI

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
            client = MongoClient(db_json['url'])
            db = client[db_json['db']]

        self.coll_users_data = db['users_data']
        self.coll_users = db['users']
        self.username = username
        self.info = get_info.GetInfo(username, password, server, ssl)

    def __save_to_db(self, info, project_list):

        try:
            date_time = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
            self.coll_users_data.insert({'username': self.username,
                                         'date:time': date_time,
                                         'info': info,
                                         'project_list': project_list},
                                        check_keys=False)
            print("Saved")
        except Exception:
            print(Exception.with_traceback())

    def save_data(self):

        info = self.info.get_info()
        project_list = self.info.get_project_list()
        self.__save_to_db(info, project_list)

    def save_user(self, username, password, server, ssl):

        users = self.coll_users
        users.insert({'username': username,
                      'password': password,
                      'server': server,
                      'ssl': ssl})
