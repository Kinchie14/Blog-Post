from website import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime




class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    profile_image = db.Column(db.String(64), nullable = False, default = 'default_profile.jpeg')
    username = db.Column(db.String(64), unique = True, index = True)
    email = db.Column(db.String(64), unique = True, index = True)
    name = db.Column(db.String(64), unique = True, index = True)
    password_hash = db.Column(db.String(64))

    #The relationship between the User and the Blogpost. It is saved in posts variable
    posts = db.relationship('BlogPost', backref='author', lazy = True)


    #This will save every variable of the User.
    #Missing, what is the purpsoe!!
    def __init__(self,email,username,password,name):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.name = name
    
    #This will check the if the hashing password and the password inputted by the user will be the same
    def check_password(self, password):
        return check_password_hash(self.password_hash,password)

    #This will return string regarding the Username and the Name of the user
    #What is the usage
    def __repr__(self):
        return f"Username: {self.username}. Name {self.name}"


class BlogPost(db.Model):
    #This is the relation of the user and the BlogPost. This will connect the two.
    #It is saved in users variable
    users = db.relationship(User)

    #BlogPost are saving the ID of the user in variable name user_id for later use.
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(140), nullable = False)
    text = db.Column(db.Text, nullable = False)

    #This are saving every data of the blogpost into self variable
    def __init__(self, title, text, user_id):
        self.title = title
        self.text = text
        self.user_id = user_id

    #This return a string regarding the id of the post, the data of post, and the title of the post
    def __repr__(self):
        return f"Post ID: {self.id} -- Date: {self.date} -- Title: {self.title}"
