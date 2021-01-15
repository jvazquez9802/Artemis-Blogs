from flask import render_template, url_for, redirect, request, flash
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm
from app.models import Blogger, Blog, Post
from flask_login import login_user, logout_user, current_user, login_required

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', blogs = Blog.query.all())
@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Blogger.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Welcome {user.user_name}','success')
            return redirect(next_page) if next_page else redirect (url_for('home'))
        else:   
            flash('Login failed, check the fields','danger')
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    flash('You logged out','warning')
    return redirect(url_for('home'))
    
@app.route("/myblog", methods=['GET','POST'])
@login_required
def myblog():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.user_name = form.user_name.data
        current_user.email = form.email.data
        
        current_user.blog[0].blog_name = form.blog_name.data
        current_user.blog[0].phrase = form.phrase.data
        current_user.blog[0].about = form.about.data
        
        db.session.commit()
        flash('Information updated.','success')
        return redirect(url_for('myblog'))
    elif request.method == 'GET':
        form.user_name.data = current_user.user_name
        form.email.data = current_user.email
        
        form.blog_name.data = current_user.blog[0].blog_name
        form.phrase.data = current_user.blog[0].phrase
        form.about.data = current_user.blog[0].about
    image_file = url_for('static',filename='profile_pics/'+ current_user.profile_image_file)
    image_cover =  url_for('static',filename='cover_pics/'+ current_user.blog[0].cover_image_file)
    return render_template('profile.html', image_file=image_file, image_cover=image_cover, form=form)
