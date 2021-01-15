from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(blogger_id):
    return Blogger.query.get(int(blogger_id))

class Blogger(db.Model, UserMixin): 
    id = db.Column(db.Integer,primary_key=True)
    user_name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False) 
    password = db.Column(db.String(100), nullable=False) 
    profile_image_file = db.Column(db.String(30), nullable=False, default='default_profile.jpg') 
    created_date = db.Column(db.DateTime, default=datetime.utcnow) 
    updated_date = db.Column(db.DateTime, default=datetime.utcnow) 
    posts = db.relationship('Post', backref='author', lazy=True)
    blog = db.relationship('Blog', backref='author', lazy=True) 
    
    def __repr__(self):
        return f"Blogger('{self.user_name},'{self.email}','{self.profile_image_file}')"

class Blog(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    blog_name = db.Column(db.String(20), nullable=False)
    phrase = db.Column(db.String(120),nullable=True, default=None) 
    about = db.Column(db.String(250), nullable=True, default=None)
    cover_image_file = db.Column(db.String(30), nullable=False, default='default_cover.jpg')  
    created_date = db.Column(db.DateTime, default=datetime.utcnow) 
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id =  db.Column(db.Integer, db.ForeignKey('blogger.id'), nullable=False)
    posts = db.relationship('Post', backref='publications', lazy=True) 
    
    
    def __repr__(self):
        return f"Blog('{self.blog_name},'{self.phrase}','{self.about}','{self.cover_image_file}')"

class Post(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False) 
    description = db.Column(db.String(150), nullable=False) 
    content = db.Column(db.Text, nullable=False) 
    labels = db.Column(db.String(100))
    post_image = db.Column(db.String(30), nullable=False, default='default_post.jpg') 
    created_date = db.Column(db.DateTime, default=datetime.utcnow) 
    updated_date = db.Column(db.DateTime, default=datetime.utcnow) 
    user_id =  db.Column(db.Integer, db.ForeignKey('blogger.id'))
    blog_id =  db.Column(db.Integer, db.ForeignKey('blog.id'))
    
    def __repr__(self):
        return f"Post('{self.title},'{self.description}','{self.labels}','{self.post_image}','{self.created_date}','{self.updated_date}')"
    