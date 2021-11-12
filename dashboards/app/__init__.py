# Import flask and template operators
from flask import Flask, redirect, url_for
from dashboards.app.dashboards.controllers import db
from dashboards.app.authentication.controllers import auth


# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('dashboards.config')


# Set the redirecting route for dashboard
@app.route('/')
def login():
    return redirect(url_for('auth.login'))


app.register_blueprint(db)
app.register_blueprint(auth)
