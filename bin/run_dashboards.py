#!/usr/bin/env python

from dashboards.app import app
from dashboards import config
import os
import argparse
from argparse import RawTextHelpFormatter

desc = 'Run the webapp given a previously generated pickle file (yielded by'\
       'download_data.py) and a configuration file (JSON file describing the '\
       'different plots and access rights)'

ap = argparse.ArgumentParser(description=desc,
                             formatter_class=RawTextHelpFormatter)
ap.add_argument('-p', '--pickle', help='Path to pickle', required=True)
ap.add_argument('-c', '--config', help='Path to configuration file',
                required=True)
ap.add_argument('-P', '--port', help='Port number', default=5000)
ap.add_argument('-u', '--url', help='URL for the server', default='localhost')
ap.add_argument('--debug', help='Debug mode', action='store_true',
                default=False)
args = ap.parse_args()


if __name__ == "__main__":
    config.DASHBOARD_CONFIG_PATH = os.path.abspath(args.config)
    config.PICKLE_PATH = os.path.abspath(args.pickle)

    app.run(host=args.url, port=args.port, debug=args.debug)
