from pustak_bhandar import db, login_manager
from flask_login import UserMixin

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
        return f"User('{self.username}', '{self.email}, '{self.image}'')"
    
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=False, unique=True)
    author = db.Column(db.String(20), nullable=False, unique=True)
    genre = db.Column(db.String(20), nullable=False)
    cover_image = db.Column(db.String(20), nullable=False, unique=True)
    links = db.Column(db.String(60), nullable=False, unique=True)
    
# class Article(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(40), nullable=False, unique=True)
#     description = db.Column(db.String(150), nullable=False, unique=True)
#     cover_image = db.Column(db.String(20), nullable=False, unique=True)
#     date_created = db.Column(db.String(20), nullable=False, unique=True)