## .website
from flask import Flask
from website.core.views import core
from website.users.views import users
from website.errorpage.errorhandler import error_pages
import os


app = Flask(__name__)


app.config['SECRET_KEY'] = 'mysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


app.register_blueprint(core, url_prefix='/')
app.register_blueprint(users, url_prefix='/')
app.register_blueprint(error_pages, url_prefix='/')