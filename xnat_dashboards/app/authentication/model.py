import json
from pyxnat import Interface
from xnat_dashboards import config as config_file


# Function to check if user exist
def user_exists(username, password, server, ssl):
    """Checks whether user exist on XNAT instance.

    Args:
        username (str): Name of user on XNAT instance
        password (str): Password of user on XNAT instance
        server (str): Server url of XNAT instance
        ssl (str): whether to verify remote host

    Returns:
        int/list: If user exist returns an integer else an empty list.
    """
    verify = ssl == 1

    exists = Interface(
        user=username, password=password, server=server, verify=verify)\
        .select.projects().get()

    # If user exists then exists lengths will be more than 0

    return len(exists) if len(exists) > 0 else []


# Get user role config file
def user_role_config(username):
    """Checks whether user roles are assigned in configuration file.

    Args:
        username (str): Username of through which user logged in.

    Returns:
        dict/bool: Dictionary of details to be processed further
        default user role if not assigned is guest, if user
        is assigned a forbidden role then return False
    """
    with open(config_file.DASHBOARD_CONFIG_PATH) as json_file:
        config = json.load(json_file)['roles_config']

    # If user role exist
    if username in config['user roles']:
        if config['user roles'][username] == 'forbidden':
            return False
        else:  # If user role is forbidden then return False
            return config
    else:  # Default user as guets will be returned
        return config


def login_urls():
    """Checks whether user roles are assigned in configuration file.

    Args:
        username (str): Username of through which user logged in.

    Returns:
        dict/bool: Dictionary of details to be processed further
        default user role if not assigned is guest, if user
        is assigned a forbidden role then return False
    """
    with open(config_file.DASHBOARD_CONFIG_PATH) as json_file:
        url_list = json.load(json_file)['login_urls']

    return url_list
