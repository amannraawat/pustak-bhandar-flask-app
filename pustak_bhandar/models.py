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
    image_data = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(40), nullable=False)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}, '{self.image_data}')"
    
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=False, unique=True)
    description = db.Column(db.String(2000), nullable=False)
    first_para = db.Column(db.String(1000))
    second_para = db.Column(db.String(1000))
    third_para = db.Column(db.String(1000))
    fourth_para = db.Column(db.String(1000))
    fifth_para = db.Column(db.String(1000))
    genre = db.Column(db.String(20), nullable=False)
    image_data = db.Column(db.LargeBinary, nullable=False)
    links = db.Column(db.String(200), nullable=False)
    date_published = db.Column(db.Date, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    author = db.relationship('Author', backref='book')
    
    def __repr__(self):
        return f"Book('{self.title}', '{self.author}', '{self.genre}', '{self.date_written}')"
    
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    about = db.Column(db.String(1000))
    image_data = db.Column(db.LargeBinary)
    books = db.relationship('Book', backref='writer', lazy=True)
    
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=False, unique=True)
    author = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(150), nullable=False, unique=True)
    section1 = db.Column(db.String(50), unique=True)
    section1_data = db.Column(db.String(1000), unique=True)
    section2 = db.Column(db.String(50), unique=True)
    section2_data = db.Column(db.String(1000), unique=True)
    section3 = db.Column(db.String(50), unique=True)
    section3_data = db.Column(db.String(1000), unique=True)
    section4 = db.Column(db.String(50), unique=True)
    section4_data = db.Column(db.String(1000), unique=True)
    section5 = db.Column(db.String(50), unique=True)
    section5_data = db.Column(db.String(1000), unique=True)
    conclusion = db.Column(db.String(50), unique=True)
    conclusion_data = db.Column(db.String(1000), unique=True)
    image_data = db.Column(db.LargeBinary, nullable=False)
    date_created = db.Column(db.Date, nullable=False)
    
    def __repr__(self):
        return f"Article('{self.title}', '{self.description}', '{self.date_created}')"