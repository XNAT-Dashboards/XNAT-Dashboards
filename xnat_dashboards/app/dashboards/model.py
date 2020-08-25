import pickle
from xnat_dashboards import config


def load_users_data(server):
    """Opens pickle file to be used the the dashboard
    controller.

    Args:
        server (str): URL of the server where user is
            is registered.

    Returns:
        dict/None: If server details are mistaching it returns
        None else returns the details from pickle as a dict.
    """
    try:
        with open(
                config.PICKLE_PATH, 'rb') as handle:
            user_data = pickle.load(handle)
        if user_data['server'] != server:
            return None
    except FileNotFoundError:
        print(
            "pickle file not found on path: ", config.PICKLE_PATH)
        return None

    return user_data
