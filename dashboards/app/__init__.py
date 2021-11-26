# Import flask and template operators
from flask import Flask, redirect, url_for
from dashboards.app import controllers as c


# Define the WSGI application object
app = Flask(__name__)

# Configuration
app.config.from_object('dashboards.config')


# Set the redirecting route for dashboard
@app.route('/')
def login():
    return redirect(url_for('dashboards.login'))


app.register_blueprint(c.app)
