# Define the application directory
import os

"""
Set server specific variable here.

Change both the secret key before using the web app in public
urls.
"""

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

DASHBOARD_CONFIG_PATH = ''

PICKLE_PATH = ''
