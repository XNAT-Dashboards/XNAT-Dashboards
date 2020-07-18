from save_endpoint import save_to_pickle, save_to_db
import json
import pickle
from tqdm import tqdm
import argparse


class DownloadResources:

    def __init__(self, path):

        self.user_name = path

    def load_user_pk(self, username):

        try:
            with open('pickles/users/' + username + '.pickle', 'rb') as handle:
                user = pickle.load(handle)
        except FileNotFoundError:
            return None

        return user

    def iter_users(self):

        with open(self.user_name) as json_file:
            users = json.load(json_file)

        for user in tqdm(users):

            user = self.load_user_pk(user)
            if user is not None:
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

        pk_saver.save_resources(username, password, server, ssl)


ap = argparse.ArgumentParser()
ap.add_argument("-p", "--path", type=str, help="Path to user name.json")

args = vars(ap.parse_args())

if __name__ == "__main__":

    download_resource_object = DownloadResources(args['path'])
    download_resource_object.iter_users()
