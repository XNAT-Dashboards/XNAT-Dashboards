#!/usr/bin/env python

from xnat_dashboards.app import app
from xnat_dashboards import path_creator
import os
import socket
import argparse

"""
This file is used for starting the server it takes 2 file paths
first the is the dashboard configuration file and the second
is the pickle file that needs to be downloaded first from the
download data file. This file won't be present when using
the pypi xnat_dashboards package.
"""

ap = argparse.ArgumentParser()
ap.add_argument(
    "-p", "--pickle", type=str,
    help="Path to saved pickle file")
ap.add_argument(
    "-c", "--config", type=str,
    help="Path to configuration file")
args = vars(ap.parse_args())

ap.add_argument(
    "-port", "--port", type=int,
    help="Port number", default=5000)

ap.add_argument(
    "-url", "--url", type=str,
    help="URL for the server", default='localhost')

ap.add_argument(
    "-debug", "--debug", type=bool,
    help="Activate debugger", default=False)

args = vars(ap.parse_args())


if __name__ == "__main__":

    if args['pickle'] is None or args['config'] is None:
        print(
            "Please provide path, name to both pickle and"
            "dashboard configuraion file")
    else:
        # Path to configuration and pickle files
        path_creator.set_dashboard_config_path(
            os.path.abspath(args['config']))
        path_creator.set_pickle_path(
            os.path.abspath(args['pickle']))
        # Change localhost url or port here

    try:
        print(args['port'])
        app.run(host=args['url'], port=args['port'], debug=args['debug'])
    except socket.gaierror:
        print("Wrong server url provided to run the application")
    except PermissionError:
        print(
            "Port number is not correct please check whether "
            "port number is an integer")
