from xnat_dashboards.app import app
from xnat_dashboards import path_creator
import os

# Default path to configuration and pickle files
path_creator.set_dashboard_config_path(
    os.path.abspath('xnat_dashboards/config/dashboard_config.json'))
path_creator.set_pickle_path(
    os.path.abspath('xnat_dashboards/config/general.pickle'))

# Change localhost url or port here
app.run(debug=True)
