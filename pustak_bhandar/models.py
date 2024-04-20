from pustak_bhandar import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(40), nullable=False)
    image = db.Column(db.String(20), nullable=False, default='default.jpg')
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}, '{self.image}')"
    
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=False, unique=True)
    author = db.Column(db.String(20), nullable=False, unique=True)
    description = db.Column(db.String(2000), nullable=False)
    genre = db.Column(db.String(20), nullable=False)
    image_data = db.Column(db.LargeBinary, nullable=False)
    links = db.Column(db.String(200), nullable=False)
    date_published = db.Column(db.Date, nullable=False)
    
    def __repr__(self):
        return f"Book('{self.title}', '{self.author}', '{self.genre}', '{self.date_written}')"
    
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=False, unique=True)
    author = db.Column(db.String(20), nullable=False, unique=True)
    description = db.Column(db.String(150), nullable=False, unique=True)
    image_data = db.Column(db.LargeBinary, nullable=False)
    date_created = db.Column(db.Date, nullable=False)
    
    def __repr__(self):
        return f"Article('{self.title}', '{self.description}', '{self.date_created}')"