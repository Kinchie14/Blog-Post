#USERS-Views
from flask import render_template, request, Blueprint, flash, redirect, url_for
from website.users.forms import SignupForm, LoginForm, UpdateUserForm
from flask_login import login_user, current_user, logout_user, login_required
from website import db
from website.models import User, BlogPost
from website.users.picture_handler import add_profile_pic



users = Blueprint('users', __name__)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("core.index"))



@users.route('/sign-up', methods = ['GET','POST'])
def sign_up():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(name = form.name.data,
                username = form.username.data,
                email = form.email.data,
                password1 = form.password1.data,
                password2 = form.password2.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registration!')
        return redirect(url_for("users.login"))

    return render_template('sign-up.html',form = form)


@users.route('/login', methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()



    return render_template('login.html',form = form)