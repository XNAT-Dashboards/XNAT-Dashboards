# Import flask and template operators
from flask import Flask, redirect
from app.dashboards.controllers import dashboards
from app.auth.controllers import auth
from app.init_database import mongo


# Define the WSGI application object
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['MONGO_URI'] = 'mongodb+srv://testUser:testPassword@cluster0.x38yt.gcp.mongodb.net/xnat_dashboards?retryWrites=true&w=majority'
app.config['MONGO_DB'] = 'xnat_dashboards'
mongo.init_app(app)


# Set the redirecting route for dashboard
@app.route('/')
def stats():
    return redirect('auth/login')


# Configurations
app.config.from_object('config')

app.register_blueprint(dashboards)
app.register_blueprint(auth)
