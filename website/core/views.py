#CORE-Views
from website.models import BlogPost
from flask import render_template, request, Blueprint

core = Blueprint('core', __name__)

@core.route('/')
def index():
    #This will allow us to cycle thru the users blogpost.
    #If the user has multiple blogpost. This will limit how many page can you see at the screen
    page = request.args.get('page', 1, type = int)
    blog_posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page= page, per_page = 5)
    return render_template('index.html', blog_posts = blog_posts)

@core.route('/info')
def info():
    return render_template('info.html')

