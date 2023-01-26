#USERS-Views

from flask import render_template, request, Blueprint

users = Blueprint('users', __name__)

@users.route('/login')
def login():
    return render_template('login.html')

@users.route('/sign-up')
def sign_up():
    return render_template('sign-up.html')

