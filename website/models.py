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

    posts = db.relationship('BlogPost', backref='author', lazy = True)

    def __init__(self,email,username,password,name):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.name = name
    
    def check_password(self, password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"Username: {self.username}. Name {self.name}"

class BlogPost(db.Model):
    users = db.relationship(User)
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(140), nullable = False)
    text = db.Column(db.Text, nullable = False)


    def __init__(self, title, text, user_id):
        self.title = title
        self.text = text
        self.user_id = user_id

    def __repr__(self):
        return f"Post ID: {self.id} -- Date: {self.date} -- Title: {self.title}"
