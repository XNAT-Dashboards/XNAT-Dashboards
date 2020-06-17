# Import flask dependencies
from flask import Blueprint, request, redirect,\
                  render_template, session, url_for

# Define the blueprint: 'auth', set its url prefix: app.url/auth
auth = Blueprint('auth', __name__, url_prefix='/auth')


# Set the route and accepted methods
@auth.route('/login/', methods=['GET', 'POST'])
def stats():

    if(request.method == 'POST'):

        user_detail = request.form
        session['user_d'] = user_detail
        return redirect(url_for("dashboards.stats"))

    else:

        return render_template('auth/login.html')
