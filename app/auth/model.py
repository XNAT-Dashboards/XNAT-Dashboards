import json
from pyxnat_interface import data_fetcher


# Function to check if user exist
def user_exists(username, password, server, ssl):

    exists = data_fetcher.Fetcher(
        username, password, server, ssl).get_projects_details()

    # If user exists then no int will be returned
    if type(exists) == int:
        exists = []
    else:
        exists = 1

    return exists


# Get user role config file
def user_role_config(username):

    with open('utils/roles_config.json') as json_file:
        config = json.load(json_file)

    # If user role exist
    if username in config['user roles']:
        if config['user roles'][username] == 'forbidden':
            return False
        else:  # If user role is forbidden then return False
            return config
    else:  # Default user as guets will be returned
        return config
