from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField, ValidationError, TextAreaField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, URL
from flask_wtf.file import FileField, FileAllowed
from pustak_bhandar.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')
    
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')
    
class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    genre = StringField('Genre', validators=[DataRequired()])
    cover_image = FileField('Book Image', validators=[FileAllowed(['jpg', 'png']), DataRequired()])
    link = StringField('Link', validators=[DataRequired(), URL()])
    date_published = DateField('Published Date', format='%Y-%m-%d')
    submit = SubmitField('Add Book')
    
class ArticleForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    cover_image = FileField('Article Image', validators=[FileAllowed(['jpg', 'png']), DataRequired()])
    date_written = DateField('Date Written', validators=[DataRequired( )])
    submit = SubmitField('Add Article')