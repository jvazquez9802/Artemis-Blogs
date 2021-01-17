from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os

app = Flask(__name__)

app.config['SECRET_KEY']  = '52b67e7deddf113d0126e9deb2df9bf9'
app.config['SQLALCHEMY_DATABASE_URI'] ='postgres://nplokbysjhkrpa:bd51e5d48632f1d679c2226677bffb9fc32b216bcb759188cc84dab390cbf260@ec2-34-202-5-87.compute-1.amazonaws.com:5432/dfe1brss7i94f4'
#app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql+psycopg2://postgres:admin@localhost:5433/Artemis_blogs'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False
app.config['MAIL_SERVER'] ='smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME']  = 'ArtemisBlogsNoreply'
app.config['MAIL_PASSWORD']  = '1234567asdfgh*'

db=SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail(app)
 
from app.users.routes import users
from app.posts.routes import posts
from app.main.routes import main
from app.errors.handlers import errors
app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)
app.register_blueprint(errors)
db.create_all()
    
    