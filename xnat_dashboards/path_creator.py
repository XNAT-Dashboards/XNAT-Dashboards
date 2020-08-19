pickle_path = ''
dashboard_config_path = ''

"""
Use to set the path of pickle and configuration file globally
that will be used by different part of code.

Set method are used when downloading the data or starting the server
get method are used in different parts of code to get the path details.
"""


def set_pickle_path(path):

    global pickle_path
    pickle_path = path


def get_pickle_path():

    return pickle_path


def set_dashboard_config_path(path):

    global dashboard_config_path
    dashboard_config_path = path


def get_dashboard_config_path():

    return dashboard_config_path
