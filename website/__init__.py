## .website
from flask import Flask
from website.core.views import core
from website.users.views import users
from website.errorpage.errorhandler import error_pages



app = Flask(__name__)


app.register_blueprint(core, url_prefix='/')
app.register_blueprint(users, url_prefix='/')
app.register_blueprint(error_pages, url_prefix='/')