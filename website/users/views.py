#USERS-Views
from flask import render_template, request, Blueprint, flash, redirect, url_for
from website.users.forms import SignupForm, LoginForm, UpdateUserForm
from flask_login import login_user, current_user, logout_user, login_required
from website import db
from website.models import User, BlogPost
from website.users.picture_handler import add_profile_pic



users = Blueprint('users', __name__)

#Nothing just a logout function that when the logout button has been clicked, it will logged out the current_user
@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("core.index"))



@users.route('/sign-up', methods = ['GET','POST'])
def sign_up():
    form = SignupForm()

    #If the user validated on submission. It will create a User data which is the model from the database
    if form.validate_on_submit():
        user = User(name = form.name.data,
                username = form.username.data,
                email = form.email.data,
                password = form.password1.data,)
        db.session.add(user)
        db.session.commit()
        #Up to this. This db syntax only mean that we are going to save the data from the form into the database

        flash('Thanks for registration!')

        #Redirecting the user to the login form so they can login
        return redirect(url_for("users.login"))

    #Returning the form because it is needed on the template
    return render_template('sign-up.html',form = form)


@users.route('/login', methods = ['GET','POST'])
def login():
    form = LoginForm()

    #If the user is valid. And all the information is valid
    if form.validate_on_submit():

        #This will check if the email that the user input on the form is on the database
        user = User.query.filter_by(email = form.email.data).first()
        if user.check_password(form.password.data) and user is not None:
        #This will check the password from the database if the input password from the form and the database match
        #check_password is a function that you created on the models.py. It means the function will check
        #if the input password and the form is correct.

            #if all the information above turns out to be true it will login the user
            #The user parameter here are the user that are initialize on the top when checking the email
            login_user(user)


            flash("You have been logged in successfully!")

            #This will check the next action that the user will do.
            #It will check if it's valid or not, then if not it will just return on the core.index, that basically is the homepage
            next = request.args.get('next')
            if next == None or not next[0]=='/':
                next = url_for('core.index')
            return redirect(next)
            #Up to this

    #returning the form because it is needed on the template        
    return render_template('login.html',form = form)


#This are the endpoint on viewing the account of the user, that will show a form consist of his information
@users.route('/account', methods = ['GET','POST'])
@login_required
#This are the route for viewing the account of the user. And give him an option to update his info
def account():
    form = UpdateUserForm()
    if form.validate_on_submit():
        print(form)
        
        #This is the logic for updating the profile picture and some of his information
        #This part of the logic means if the user uploaded a picture on the form
        #This will only activate if there's a data on the Form
        if form.picture.data:

            #current_user is just a syntax of login manager.
            #This only mean that we are grabbing the user username and save it on username variable
            username = current_user.username

            #After the username has been added. It will pass the username and the data of the picture into pic variable
            #add_profile_pic function will now be activate, and get all those data.
            #add_profile_pic is a function on picture_handler.py
            pic = add_profile_pic(form.picture.data,username)

            #Now after the pic has been done, we are now going to set the profile picture of the current_user into the pic variable
            #profile_image is an attribute of your model in the database model.
            current_user.profile_image = pic

        #This are the remaining form that are on the UpdateUserForm which contain of username and email
        #The data from the top is just the profile.
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('User account has been updated!')
        return redirect(url_for("users.account"))

    #Self explanation.    
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    
    #This are the default image of the user if he don't upload an image on the form
    profile_image = url_for('static', filename = 'profile_pics/'+current_user.profile_image)
    
    #profile_image has been a parameter because we needed that on the page
    return render_template("account.html", profile_image = profile_image, form = form)


@users.route("/<username>")
def user_posts(username):
    
    #This will allow us to cycle thru the users blogpost.
    #If the user has multiple blogpost. This will limit how many page can you see at the screen
    page = request.args.get('page', 1, type = int)

    #This is how we get the username of the user that will allow us view the post of that certain username
    #404 means when a certain user want to manually type what would be the username on the endpoint
    #if it turns out to have a wrong spelling, it will return a 404 error
    user = User.query.filter_by(username=username).first_or_404()

    #This will help us to grab the blogpost of the user
    #We use author because that is what we back reference on how the user handle its own blogpost on the models
    #That is why you query the author for that blog post
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page, per_page=5)
    return render_template('user_blog_posts.html', blog_posts=blog_posts, user=user)
