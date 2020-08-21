pickle_path = ''
dashboard_config_path = ''


def set_pickle_path(path):
    """Set the pickle path to be used globally.

    Args:
        path (str): Path to the pickle file
    """
    global pickle_path
    pickle_path = path


def get_pickle_path():
    """Use to fetch the global pickle path

    Returns:
        str: Path to the pickle file
    """
    return pickle_path


def set_dashboard_config_path(path):
    """Set the config path to be used globally.

    Args:
        path (str): Path to the config file
    """
    global dashboard_config_path
    dashboard_config_path = path


def get_dashboard_config_path():
    """Use to fetch the global config path

    Returns:
        str: Path to the config file
    """
    return dashboard_config_path
