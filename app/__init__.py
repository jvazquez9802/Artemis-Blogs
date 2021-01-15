from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = '52b67e7deddf113d0126e9deb2df9bf9'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql+psycopg2://postgres:admin@localhost:5433/Artemis_blogs'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from app import routes