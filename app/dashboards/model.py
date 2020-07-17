import pickle
import json


def load_user_pk(username):

    try:
        with open('pickles/users/' + username + '.pickle', 'rb') as handle:
            user = pickle.load(handle)
    except FileNotFoundError:
        return None

    return user


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
