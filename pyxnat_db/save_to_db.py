from pymongo import MongoClient
import sys
from os.path import dirname, abspath
from datetime import datetime
sys.path.insert(0, dirname(dirname(abspath(__file__))))
from pyxnat_api import get_info


class SaveToDb:

    username = ''
    coll = None

    def __init__(self, username, password, server, ssl):
        # Connecting to MySQL server at localhost using PyMySQL DBAPI
        client = MongoClient("mongodb+srv://testUser:testPassword@cluster0.x38yt.gcp.mongodb.net/xnat_dashboards?retryWrites=true&w=majority")
        db = client['xnat_dashboards']
        self.coll = db['users_data']
        self.username = username
        self.info = get_info.GetInfo(username, password, server, ssl)

    def __save_to_db(self, info, project_list):
        try:
            date_time = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
            self.coll.insert({'username':self.username,'date:time':date_time, 'info':info,'project_list': project_list}, check_keys=False)
            print("Saved")
        except Exception:
            print(Exception.with_traceback())

    def save(self):
        info = self.info.get_info()
        project_list = self.info.get_project_list()
        self.__save_to_db(info, project_list)
