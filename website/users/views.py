#USERS-Views
from flask import render_template, request, Blueprint, flash, redirect, url_for
from website.blogpost.forms import SignupForm, LoginForm

users = Blueprint('users', __name__)

@users.route('/login')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.name.data
        password = form.password.data
    return render_template('login.html',form = form)

@users.route('/sign-up')
def sign_up():
    form = SignupForm()
    if form.validate_on_submit():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password1 = form.password1.data
        password2 = form.password2.data

        #user = User.query.filter_by(email = email).first()
        #if user:
            #flash('The user has already been created', category='error')
            #return redirect(url_for('auth.sign_up'))
        if len(name) < 2:
            flash('The name should be greater than 2 characters', category='error')
            return redirect(url_for('auth.sign_up'))
        elif username < 2:
            flash("Username should be greater than 2 characters", category='error')
            return redirect(url_for('auth.sign_up'))
        elif len(email) < 3:
            flash('Email should be greater than 3 characters', category='error')
            return redirect(url_for('auth.sign_up'))
        elif password1 != password2:
            flash('Password should be the same', category='error')
            return redirect(url_for('auth.sign_up'))
        else:
            pass


    return render_template('sign-up.html',form = form)

