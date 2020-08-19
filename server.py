from xnat_dashboards.app import app
from xnat_dashboards import path_creator
import os
import argparse


ap = argparse.ArgumentParser()
ap.add_argument(
    "-p", "--pickle", type=str,
    help="Path to saved pickle file")
ap.add_argument(
    "-c", "--config", type=str,
    help="Path to configuration file")
args = vars(ap.parse_args())


if __name__ == "__main__":

    if args['pickle'] is None or args['config'] is None:
        print("Please provide path to both pickle and config file")
    else:
        # Path to configuration and pickle files
        path_creator.set_dashboard_config_path(
            os.path.abspath(args['config']))
        path_creator.set_pickle_path(
            os.path.abspath(args['pickle']))
        # Change localhost url or port here
        app.run(debug=True)
