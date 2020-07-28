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


def user_role_config(username):

    with open('utils/roles_config.json') as json_file:
        config = json.load(json_file)

    if username in config['user roles']:
        if config['user roles'][username] == 'forbidden':
            return False
        else:
            return config
    else:
        return config


def load_users_data_pk(server):

    try:
        with open(
                'pickles/users_data/general.pickle', 'rb') as handle:
            user_data = pickle.load(handle)

        if user_data['server'] != server:
            return None
    except FileNotFoundError:
        return None

    return user_data


def load_resources_pk(server):

    try:
        with open('pickles/resources/general.pickle', 'rb') as handle:
            resources = pickle.load(handle)
        if resources['server'] != server:
            return None
    except FileNotFoundError:
        return None

    return resources


def load_resources_bbrc_pk(server):

    try:
        with open(
                'pickles/resources/generalbbrc.pickle',
                'rb') as handle:

            resources_bbrc = pickle.load(handle)
        if resources_bbrc['server'] != server:
            return None
    except FileNotFoundError:
        return None

    return resources_bbrc
