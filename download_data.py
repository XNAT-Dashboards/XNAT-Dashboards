from xnat_dashboards.save_endpoint import save_to_pickle
from xnat_dashboards import path_creator
import os


# Add path to the pickle file
path_creator.set_pickle_path(
    os.path.abspath('xnat_dashboards/pickles/data/general.pickle'))

# if true is given as an argument, it will skip the downloading of resources
# Default is false
save_to_pickle.SaveToPk('central.cfg', True)
