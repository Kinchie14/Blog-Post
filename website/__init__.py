## .website
from flask import Flask
import os
from os import path
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager


#Fixed
db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'asdasdas'
    #Location of the database.
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)


    #Managing the login of the users
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    #Up to this. This are fixed

    #Importing the database from models.py
    from .models import User, BlogPost

    #Initializing the database
    create_database(app)


    #Registering the blueprints of the website
    from website.core.views import core
    from website.users.views import users
    from website.errorpage.errorhandler import error_pages
    from website.blog_posts.views import blog_posts

    app.register_blueprint(core)
    app.register_blueprint(users)
    app.register_blueprint(error_pages)
    app.register_blueprint(blog_posts)
    #Up to this

    return app


#Creating the function for the database. This is fixed
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!')

