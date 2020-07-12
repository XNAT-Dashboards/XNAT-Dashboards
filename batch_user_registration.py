from save_endpoint import save_to_pickle, save_to_db
import json
from tqdm import tqdm
import argparse


class BatchUserRegistration:

    user_registration_path = ''
    db = None

    def __init__(self, path, db):

        self.user_registration_path = path
        self.db = db

    def iter_users(self):

        with open(self.user_registration_path) as json_file:
            users = json.load(json_file)

        status_report_dict = {}

        for user in tqdm(users):

            if self.db:
                status = self.__save_to_DB(
                            user['username'],
                            user['password'],
                            user['server'],
                            bool(user['ssl']))
            else:
                print(user['ssl'])
                print(type(user['ssl']))
                print(bool(user['ssl']))
                status = self.__save_to_PK(
                            user['username'],
                            user['password'],
                            user['server'],
                            bool(user['ssl']))

            if status == 401:
                sr = 'Error in username or password'
            elif status == 500:
                sr = 'Error in URI extra /'
            elif status == 191912:
                sr = 'Remote host not verified'
            elif status == 1:
                sr = 'Wrong URL'
            else:
                sr = 'Saved'

            status_report_dict[user['username']] = sr

        self.__report_saver(status_report_dict)

    def __save_to_DB(self, username, password, server, ssl):

        db_saver = save_to_db.SaveToDb(
            username,
            password,
            server,
            ssl,
            False)

        return db_saver.save_data()

    def __save_to_PK(self, username, password, server, ssl):
        print('pk', str(ssl))
        print('type', type(ssl))
        pk_saver = save_to_pickle.SaveToPk(
            username,
            password,
            server,
            ssl)

        return pk_saver.save_data()

    def __report_saver(self, status_report_dict):

        with open('utils/fetching_report.json', 'w') as json_file:
            json.dump(status_report_dict, json_file)


ap = argparse.ArgumentParser()
ap.add_argument("-p", "--path", type=str, help="Path to user details.json")
ap.add_argument(
    "-db", "--db", type=str,
    help="endpoint save to db or as pickle type  if db press y else n ")

args = vars(ap.parse_args())

if __name__ == "__main__":

    if args['db'] == 'y':
        db = True
    else:
        db = False

    batch_object = BatchUserRegistration(args['path'], db)
    batch_object.iter_users()
