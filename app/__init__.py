# Import flask and template operators
from flask import Flask, redirect
from app.dashboards.controllers import dashboards
from app.auth.controllers import auth

# Define the WSGI application object
app = Flask(__name__)


# Set the redirecting route for dashboard
@app.route('/')
def stats():
    return redirect('auth/login')


# Configurations
app.config.from_object('config')

app.register_blueprint(dashboards)
app.register_blueprint(auth)
