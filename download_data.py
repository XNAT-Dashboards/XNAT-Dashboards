from xnat_dashboards.pyxnat_interface import pickle_saver
from xnat_dashboards import path_creator
import os
import argparse


ap = argparse.ArgumentParser()
ap.add_argument(
    "-i", "--cfg", type=str,
    help="Path to pyxnat configuration file")
ap.add_argument(
    "-o", "--pickle", type=str,
    help="Path where the pickle file will be created")

args = vars(ap.parse_args())

if __name__ == "__main__":
    # Add path to the pickle file
    path_creator.set_pickle_path(
        os.path.abspath(args['pickle']))

    # if true is given as an argument, it will skip the downloading
    # of resourceS Default is false
    pickle_saver.PickleSaver(args['cfg'], True)
