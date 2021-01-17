from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os


app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = '52b67e7deddf113d0126e9deb2df9bf9'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql+psycopg2://postgres:admin@localhost:5433/Artemis_blogs'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER']='smtp.googlemail.com'
app.config['MAIL_PORT']= 587
app.config['MAIL_USE_TLS']= True
app.config['MAIL_USERNAME'] = 'ArtemisBlogsNoreply'
app.config['MAIL_PASSWORD'] = 'asdfgh654321'
mail = Mail(app)

from app.users.routes import users
from app.posts.routes import posts
from app.main.routes import main

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)