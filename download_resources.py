from save_endpoint import save_to_pickle, save_to_db
import json
from tqdm import tqdm
import argparse


class DownloadResources:

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

        pk_saver = save_to_pickle.SaveToPk(
            username,
            password,
            server,
            ssl)

        pk_saver.save_data()
        pk_saver.save_resources()

    def __save_to_DB(self, username, password, server, ssl, test):

        db_saver = save_to_db.SaveToDb(
            username,
            password,
            server,
            ssl,
            True)

        db_saver.save_data()
        db_saver.save_resources()


ap = argparse.ArgumentParser()
ap.add_argument("-p", "--path", type=str, help="Path to user name.json")

args = vars(ap.parse_args())

if __name__ == "__main__":

    download_resource_object = DownloadResources(args['path'])
    download_resource_object.iter_users()
