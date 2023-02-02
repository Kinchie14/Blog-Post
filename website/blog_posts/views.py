from flask import Blueprint, render_template, url_for, flash, request, redirect, abort
from flask_login import current_user, login_required
from website import db
from website.models import BlogPost
from website.blog_posts.forms import BlogPostForm


blog_posts = Blueprint('blog_posts', __name__)

@blog_posts.route('/create', methods=['GET', 'POST'])
@login_required
#The route for creating a blogpost with a form
def create_post():
    form = BlogPostForm()

    if form.validate_on_submit():
        #If the form has been validated, it will get the following data from the form and save it from the BlogPost database
        blog_post = BlogPost(title = form.title.data,
                                text = form.text.data,
                                user_id = current_user.id)

        db.session.add(blog_post)
        db.session.commit()
        #Up to here

        flash('Blog Post has been Created')
        return redirect(url_for('core.index'))
    return render_template('create_post.html', form = form)

@blog_posts.route('/<int:blog_post_id>')
def blog_post(blog_post_id):
    #This route will show the blogpost of a certain user after the title, or the button has been clicked on the index page
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    return render_template('blog_post.html', title=blog_post.title,
                                            date = blog_post.date,
                                            post = blog_post)


@blog_posts.route('/<int:blog_post_id>/update', methods=['GET', 'POST'])
@login_required
#This are the route for the user that has been validated and he wanted to update his blog.
def update(blog_post_id):
    #Querying the BlogPost on the database and saving it into blog_post variable
    blog_post = BlogPost.query.get_or_404(blog_post_id)

    #This are the logic for looking on the id of the current user
    if blog_post.author != current_user:
        abort(403)


    form = BlogPostForm()

    #Logic if the form has been validated
    if form.validate_on_submit():
        blog_post.title = form.title.data
        blog_post.text = form.text.data
        db.session.commit()
        flash('Blog Post has been Updated')
        return redirect(url_for('blog_posts.blog_post', blog_post_id = blog_post.id))
    
    #If the user is not the current author, he can only see the title and text of the blog
    elif request.method == 'GET':
        form.title.data = blog_post.title
        form.text.data = blog_post.text
    
    return render_template('create_post.html', title = 'Updating', form = form)


@blog_posts.route('/<int:blog_post_id>/delete', methods=['POST'])
@login_required
#Route for deleting a blogpost on the database
def delete_post(blog_post_id):
    #Querying the blogpost and saving it on blog_post variable
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    #Logic for checking the id of the user before commiting the changes on the database
    if blog_post.author != current_user:
        abort(403)
    db.session.delete(blog_post)
    db.session.commit()
    #up to here
    flash('Blog Post has been Deleted')
    return redirect(url_for('core.index'))