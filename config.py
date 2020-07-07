# Define the application directory
import os
from os import environ


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Statement for enabling the development environment
DEBUG = True

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"

# Disable sorting of keys
JSON_SORT_KEYS = False

# Configuring database
MONGO_DB = 'xnat_dashboards'
MONGO_URI = environ.get('MONGO_URI')
