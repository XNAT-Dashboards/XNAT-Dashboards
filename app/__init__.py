# Import flask and template operators
from flask import Flask, redirect, url_for
from app.dashboards.controllers import dashboards
from app.auth.controllers import auth


# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')


# Set the redirecting route for dashboard
@app.route('/')
def stats():
    return redirect(url_for('auth.login_DB'))


app.register_blueprint(dashboards)
app.register_blueprint(auth)
