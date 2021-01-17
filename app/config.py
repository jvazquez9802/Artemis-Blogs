import os

class Config():
   SECRET_KEY  = '52b67e7deddf113d0126e9deb2df9bf9'
   SQLALCHEMY_DATABASE_URI =='postgres://topxanpmuaxcln:b9a9c39ec3975ca2f9441c283540639c55d561dda6811255899c2c1f60468e68@ec2-52-204-20-42.compute-1.amazonaws.com:5432/dc1nb2aikf25ip'
   SQLALCHEMY_TRACK_MODIFICATIONS =False
   MAIL_SERVER ='smtp.googlemail.com'
   MAIL_PORT = 587
   MAIL_USE_TLS = True
   MAIL_USERNAME  = os.environ.get('USER_GMAIL')
   MAIL_PASSWORD  = os.environ.get('PASSWORD_GMAIL')
   