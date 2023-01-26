## .website
from flask import Flask
from website.core.views import core
from website.users.views import users



app = Flask(__name__)


app.register_blueprint(core, url_prefix='/')
app.register_blueprint(users, url_prefix='/')