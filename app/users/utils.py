import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from app import mail
from flask_login import current_user

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path,'static/profile_pics',picture_fn)
    output_size = (170, 170)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    
    prev_picture = os.path.join(current_app.root_path, 'static/profile_pics', current_user.profile_image_file)
    if os.path.exists(prev_picture) and os.path.basename(prev_picture) != 'default_profile.jpg':
        os.remove(prev_picture)
        
    return picture_fn

def save_cover(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path,'static/cover_pics',picture_fn)
    output_size = (900, 2300)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    
    prev_picture = os.path.join(current_app.root_path, 'static/cover_pics',  current_user.blog[0].cover_image_file)
    if os.path.exists(prev_picture) and os.path.basename(prev_picture) != 'default_cover.png':
        os.remove(prev_picture)
        
    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Resert Request', sender='ArtemisBlogsNoreply@gmail.com', recipients=[user.email])
    msg.body =f'''To reset your password, visit the following link ->
{url_for('users.reset_token', token=token, _external=True)}
    
If you did not make this request then simply ignore this email.
'''
    mail.send(msg)