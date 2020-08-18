from xnat_dashboards.pyxnat_interface import pickle_saver
from xnat_dashboards import path_creator
import os


# Add path to the pickle file
path_creator.set_pickle_path(
    os.path.abspath('xnat_dashboards/config/general.pickle'))

# if true is given as an argument, it will skip the downloading of resources
# Default is false
pickle_saver.PickleSaver('xnat_dashboards/config/central.cfg', True)
