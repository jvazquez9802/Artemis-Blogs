from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.models import Blogger, Post, Blog
from app.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RecoverForm, ResetPasswordForm
from app.users.utils import save_picture, send_reset_email, save_cover

from flask import Blueprint

users = Blueprint('users',__name__)


@users.route("/blog/<int:id>/show")
def show_blog(id):
    blog=Blog.query.get_or_404(id)
    image_file = url_for('static',filename='profile_pics/'+ blog.author.profile_image_file)
    image_cover =  url_for('static',filename='cover_pics/'+ blog.cover_image_file)
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(author=blog.author).order_by(Post.created_date.desc()).paginate(page=page, per_page=5)
    return render_template('show_blog.html', blog=blog, image_file=image_file, image_cover=image_cover, posts=posts)

@users.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Blogger(user_name = form.user_name.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        user = Blogger.query.filter_by(email=form.email.data).first()
        blog = Blog(blog_name=form.blog_name.data, user_id=user.id)
        db.session.add(blog)
        db.session.commit()
        flash(f'Successful registration! welcome {form.user_name.data}','success')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)

@users.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Blogger.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Welcome {user.user_name}','success')
            return redirect(next_page) if next_page else redirect (url_for('main.home'))
        else:   
            flash('Login failed, check the fields','danger')
    return render_template('login.html', form=form)

@users.route("/logout")
def logout():
    logout_user()
    flash('You logged out','warning')
    return redirect(url_for('main.home'))


@users.route("/myblog", methods=['GET','POST'])
@login_required
def myblog():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.profile_image_file = picture_file
        if form.cover.data:
            cover_file = save_cover(form.cover.data)
            current_user.blog[0].cover_image_file = cover_file
            
        current_user.user_name = form.user_name.data
        current_user.email = form.email.data
        
        current_user.blog[0].blog_name = form.blog_name.data
        current_user.blog[0].phrase = form.phrase.data
        current_user.blog[0].about = form.about.data
        
        db.session.commit()
        flash('Blog updated.','success')
        return redirect(url_for('users.myblog'))
    elif request.method == 'GET':
        form.user_name.data = current_user.user_name
        form.email.data = current_user.email
        
        form.blog_name.data = current_user.blog[0].blog_name
        form.phrase.data = current_user.blog[0].phrase
        form.about.data = current_user.blog[0].about
    else:
        flash('update failed, check the fields','danger')
    image_file = url_for('static',filename='profile_pics/'+ current_user.profile_image_file)
    image_cover =  url_for('static',filename='cover_pics/'+ current_user.blog[0].cover_image_file)
   
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(author=current_user).order_by(Post.created_date.desc()).paginate(page=page, per_page=5)
    return render_template('profile.html', image_file=image_file, image_cover=image_cover, form=form, posts = posts) 

   
@users.route("/reset_password", methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RecoverForm()
    if form.validate_on_submit():
        user = Blogger.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email to reset your password was sent.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', form=form)

@users.route("/reset_password/<token>", methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = Blogger.verify_reset_token(token)
    if user is None:
        flash('Expired or invalid token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Password updated','success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', form=form)
