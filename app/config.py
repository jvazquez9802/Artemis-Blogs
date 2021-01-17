import os

class Config():
   SECRET_KEY  = '52b67e7deddf113d0126e9deb2df9bf9'
   SQLALCHEMY_DATABASE_URI ='postgresql+psycopg2://postgres:admin@localhost:5433/Artemis_blogs'
   SQLALCHEMY_TRACK_MODIFICATIONS =False
   MAIL_SERVER ='smtp.googlemail.com'
   MAIL_PORT = 587
   MAIL_USE_TLS = True
   MAIL_USERNAME  = os.environ.get('USER_GMAIL')
   MAIL_PASSWORD  = os.environ.get('PASSWORD_GMAIL')
   