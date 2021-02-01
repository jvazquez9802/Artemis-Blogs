from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from app import db
from app.models import Post
from app.posts.forms import PostForm
from datetime import datetime

posts = Blueprint('posts',__name__)


@posts.route("/post/new", methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, description=form.description.data, content=form.content.data,
                    labels=form.labels.data, author=current_user, blog_id=current_user.blog[0].id)
        db.session.add(post)
        db.session.commit()
        flash('Post created.', 'success')
        return redirect(url_for('users.myblog'))
    return render_template('create_post.html', form=form, legend='New Post')



@posts.route("/post/<int:id>")
def show_post(id):
    post=Post.query.get_or_404(id)
    return render_template('show_post.html', post=post)

@posts.route("/post/<int:id>/update", methods=['GET','POST'])
@login_required
def update_post(id):
    post=Post.query.get_or_404(id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.description = form.description.data
        post.labels = form.labels.data
        post.updated_date = datetime.utcnow()
        db.session.commit()
        flash('Post updated!', 'success')
        return redirect(url_for('posts.show_post', id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.description.data = post.description
        form.labels.data = post.labels
    return render_template('create_post.html', form=form, legend='Update Post')
        
@posts.route("/post/<int:id>/delete", methods=['GET','POST'])
@login_required
def delete_post(id):
    post=Post.query.get_or_404(id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted!', 'success')
    return redirect(url_for('users.show_blog', id=current_user.id))

