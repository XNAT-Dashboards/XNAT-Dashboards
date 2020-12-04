# Import flask and template operators
from flask import Flask, redirect, url_for
from dashboards.app.dashboards.controllers import dashboard
from dashboards.app.authentication.controllers import auth


# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('dashboards.config')


# Set the redirecting route for dashboard
@app.route('/')
def stats():
    return redirect(url_for('auth.login'))


app.register_blueprint(dashboard)
app.register_blueprint(auth)
