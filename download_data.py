from save_endpoint import save_to_pickle
import json
import argparse


class DownloadData:

    def __init__(self, path):

        self.role = path

    def iter_users(self):

        with open(self.role) as json_file:
            user = json.load(json_file)

        self.save(
            user['username'], user['password'],
            user['server'], user['ssl'])

        print("saved")

    def save(self, username, password, server, ssl):

        save_to_pickle.SaveToPk(username, password, server, ssl)


ap = argparse.ArgumentParser()
ap.add_argument("-p", "--path", type=str, help="Path to user name.json")

args = vars(ap.parse_args())

if __name__ == "__main__":

    download_data_object = DownloadData(args['path'])
    download_data_object.iter_users()
