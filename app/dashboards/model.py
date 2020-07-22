import pickle
import json
import socket
from pyxnat_interface import data_fetcher
import pyxnat.core.errors as pyxnat_errors


def user_exists(username, password, server, ssl):

    try:
        exists = len(list(data_fetcher.Fetcher(
            username, password, server, ssl).SELECTOR.select.projects()))

        return exists

    except pyxnat_errors.DatabaseError as dbe:
        if str(dbe).find('500') != -1:
            # 500 represent error in url or uri
            return [500]
        elif str(dbe).find('401') != -1:
            # 401 represent error in login details
            return [401]
    except socket.error as se:
        if str(se).find('SSL') != -1:
            # If verification enable and host unable to verify
            return [191912]
        else:
            # Wrong URL Connection can't be established
            return [1]


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
