# Import flask and template operators
from flask import Flask, redirect, url_for
from dashboards.app.controllers import auth, db


# Define the WSGI application object
app = Flask(__name__)

# Configuration
app.config.from_object('dashboards.config')


# Set the redirecting route for dashboard
@app.route('/')
def login():
    return redirect(url_for('auth.login'))


app.register_blueprint(db)
app.register_blueprint(auth)
