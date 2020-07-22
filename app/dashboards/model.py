import pickle
import json
from pyxnat_interface import data_fetcher


def user_exists(username, password, server, ssl):

    exists = data_fetcher.Fetcher(
        username, password, server, ssl).get_projects_details()

    if type(exists) == int:
        exists = []
    else:
        exists = 1

    return exists


def user_role_exist(username):

    with open('utils/user_roles.json') as json_file:
        user = json.load(json_file)

    if username in user:
        return user[username]
    else:
        return False


def load_users_data_pk(username):

    try:
        with open(
                'pickles/users_data/' + username + '.pickle', 'rb') as handle:
            user_data = pickle.load(handle)

    except FileNotFoundError:
        return None

    return user_data


def load_resources_pk(username):

    try:
        with open('pickles/resources/' + username + '.pickle', 'rb') as handle:
            resources = pickle.load(handle)

    except FileNotFoundError:
        return None

    return resources


def load_resources_bbrc_pk(username):

    try:
        with open(
                'pickles/resources/' + username + 'bbrc.pickle',
                'rb') as handle:

            resources_bbrc = pickle.load(handle)

    except FileNotFoundError:
        return None

    return resources_bbrc


def graph_descriptor():

    try:
        with open('utils/graph_descriptor.json') as json_file:
            descriptor = json.load(json_file)
    except OSError:
        print("graph_type.json file not found run graph_generator")
        exit(1)

    return descriptor
