#!/usr/bin/env python


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

ap.add_argument(
    "-skip", "--skip", type=bool,
    help="Skip resources download if you want to a"
    " take quick look of xnat dashboards",
    default=False)

args = vars(ap.parse_args())

if __name__ == "__main__":
    # Add path to the pickle file

    if args['pickle'] is None or args['config'] is None:
        print(
            "Please provide path, to both pickle and"
            "xnat configuraion file")
    else:
        path_creator.set_pickle_path(
            os.path.abspath(args['pickle']))

        # if true is given as an argument, it will skip the downloading
        # of resourceS Default is false
        pickle_saver.PickleSaver(args['cfg'], args['skip'])
