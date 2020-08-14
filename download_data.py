from xnat_dashboards.save_endpoint import save_to_pickle
from xnat_dashboards import path_creator
import os


path_creator.set_pickle_path(
    os.path.abspath('xnat_dashboards/pickles/data/general.pickle'))

save_to_pickle.SaveToPk('central.cfg', True)
