from xnat_dashboards.app import app
from xnat_dashboards import path_creator
import os

# Path to configuration and pickle files
path_creator.set_dashboard_config_path(os.path.abspath('xnat_dashboards/config/dashboard_config.json'))
path_creator.set_pickle_path(os.path.abspath('xnat_dashboards/pickles/data/general.pickle'))

'''
Remove from comment if you want to download data as well in pickle, if starting the server
download_data.DownloadData().save(
    'username', 'password', 'server', '')
'''

app.run(debug=True)
