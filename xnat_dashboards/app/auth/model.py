import json
from pyxnat import Interface
from xnat_dashboards import path_creator


# Function to check if user exist
def user_exists(username, password, server, ssl):

    exists = Interface(
        user=username, password=password, server=server, verify=(not ssl))\
            .select.projects().get()

    # If user exists then exists lengths will be more than 0
    if len(exists) > 0:
        return len(exists)
    else:
        return []


# Get user role config file
def user_role_config(username):

    with open(path_creator.get_dashboard_config_path()) as json_file:
        config = json.load(json_file)['roles_config']

    # If user role exist
    if username in config['user roles']:
        if config['user roles'][username] == 'forbidden':
            return False
        else:  # If user role is forbidden then return False
            return config
    else:  # Default user as guets will be returned
        return config
