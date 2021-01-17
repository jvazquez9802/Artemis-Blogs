from datetime import datetime
from flask import current_app
from app import db, login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as sr

@login_manager.user_loader
def load_user(blogger_id):
    return Blogger.query.get(int(blogger_id))

class Blogger(db.Model, UserMixin): 
    id = db.Column(db.Integer,primary_key=True)
    user_name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False) 
    password = db.Column(db.String(100), nullable=False) 
    profile_image_file = db.Column(db.String(50), nullable=False, default='default_profile.jpg') 
    created_date = db.Column(db.DateTime, default=datetime.utcnow) 
    posts = db.relationship('Post', backref='author', lazy=True)
    blog = db.relationship('Blog', backref='author', lazy=True) 
    
    def get_reset_token(self, expires_sec=1800):
        s = sr(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = sr(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return Blogger.query.get(user_id)
    
    def __repr__(self):
        return f"Blogger('{self.user_name},'{self.email}','{self.profile_image_file}')"

class Blog(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    blog_name = db.Column(db.String(100), nullable=False)
    phrase = db.Column(db.String(120),nullable=True, default=None) 
    about = db.Column(db.Text, nullable=True, default=None)
    cover_image_file = db.Column(db.String(50), nullable=False, default='default_cover.png')  
    created_date = db.Column(db.DateTime, default=datetime.utcnow) 
    user_id =  db.Column(db.Integer, db.ForeignKey('blogger.id'), nullable=False)
    posts = db.relationship('Post', backref='publications', lazy=True) 
    
    
    def __repr__(self):
        return f"Blog('{self.blog_name},'{self.phrase}','{self.about}','{self.cover_image_file}')"

class Post(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False) 
    description = db.Column(db.Text(), nullable=False) 
    content = db.Column(db.Text, nullable=False) 
    labels = db.Column(db.String(100))
    created_date = db.Column(db.DateTime, default=datetime.utcnow) 
    updated_date = db.Column(db.DateTime, default=datetime.utcnow) 
    user_id =  db.Column(db.Integer, db.ForeignKey('blogger.id'))
    blog_id =  db.Column(db.Integer, db.ForeignKey('blog.id'))
    
    def __repr__(self):
        return f"Post('{self.title},'{self.description}','{self.labels}','{self.post_image}','{self.created_date}','{self.updated_date}')"
    