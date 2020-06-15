# Import flask and template operators
from flask import Flask
from app.dashboards.controllers import dashboards
from app.auth.controllers import auth

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

app.register_blueprint(dashboards)
app.register_blueprint(auth)
