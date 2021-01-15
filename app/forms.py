from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from app.models import Blogger
    
class RegistrationForm(FlaskForm):
    user_name = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    blog_name = StringField('Blog Name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password',  validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    def validate_user_name(self, user_name):
        user = Blogger.query.filter_by(user_name=user_name.data).first()
        if user:
            raise ValidationError('Username already in use')
    
    def validate_email(self, email):
        email = Blogger.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('An account is already assigned to this email address')
    
class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',  validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
class UpdateAccountForm(FlaskForm):
    user_name = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    blog_name = StringField('Blog Name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    phrase = StringField('Favorite Phrase',
                                validators=[DataRequired(), Length(min=2, max=20)])
    about = TextField('About me',
                                validators=[DataRequired(), Length(min=2)])
    picture = FileField('Update Blog Picture', validators=[FileAllowed(['jpg', 'png'])])
    cover = FileField('Update Blog Cover', validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Update')
        
    def validate_user_name(self, user_name):
        if user_name.data != current_user.user_name:
            user = Blogger.query.filter_by(user_name=user_name.data).first()
            if user:
                raise ValidationError('Name already in use')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            email = Blogger.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('That email is taken.')
        
        
    