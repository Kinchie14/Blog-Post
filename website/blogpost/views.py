from flask import Blueprint, render_template, url_for, flash, request, redirect
from flask_login import current_user, login_required
from website import db
from website.models import BlogPost
from website.blogpost.forms import BlogPostForm


blogpost = Blueprint('blogpost', __name__)

@blogpost.route('/create', methods=['GET', 'POST'])
@login_required
def createpost():
    form = BlogPostForm()

    if form.validate_on_submit():
        blog_post = BlogPost(title = form.title.data,
                                text = form.text.data,
                                user_id = current_user.id)

        db.session.add(blog_post)
        db.session.commit()
        flash('Blog Post has been Created')
        return redirect(url_for('core.index'))
    return render_template('create_post.html', form = form)

@blogpost.route('/<int:blog_post_id>')
def blog_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    return render_template('blog_post.html', title=blog_post.title,
    date = blog_post.date,
    post = blog_post)


@blogpost.route('/<int:blog_post_id/update', methods=['GET', 'POST'])
@login_required
def update(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)

    if blog_post.author != current_user:
        abort(403)
    form = BlogPostForm()

    if form.validate_on_submit():
        blog_post.title = form.title.data
        blog_post.text = form.text.data
        db.session.commit()
        flash('Blog Post has been Updated')
        return redirect(url_for('blogpost.blog_post', blog_post_id = blog_post.id))
    elif request.method == 'GET':
        form.title.data = blog_post.title
        form.text.data = blog_post.text
    
    return render_template('create_post.html', title = 'Updating', form = form)

@blogpost.route('/<int:blog_post_id/delete', methods=['GET', 'POST'])
@login_required
def delete_post(blog_post_id):

    blog = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        abort(403)
    db.session.delete(blog_post)
    db.session.commit()
    flash('Blog Post has been Deleted')
    return redirect(url_for('core.index'))