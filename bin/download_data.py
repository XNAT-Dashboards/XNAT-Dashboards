#!/usr/bin/env python


from xnat_dashboards.pyxnat_interface import pickle_saver
from xnat_dashboards import config as config_file
import os
import logging
import argparse


ap = argparse.ArgumentParser()
ap.add_argument(
    "-i", "--cfg", type=str,
    help="Path to pyxnat configuration file Example:"
    " path/dashboard_config.json")
ap.add_argument(
    "-o", "--pickle", type=str,
    help="Path where the pickle file will be created."
    " Example: path/test.pickle")

args = vars(ap.parse_args())

if __name__ == "__main__":
    # Add path to the pickle file

    if args['pickle'] is None or args['cfg'] is None:
        logging.error(
            "   Please provide path to both pickle and "
            "xnat configuration file")
    else:
        config_file.PICKLE_PATH = os.path.abspath(args['pickle'])

        # if true is given as an argument, it will skip the fetching
        # of resources Default is false
        pickle_saver.PickleSaver(os.path.abspath(args['cfg']))
