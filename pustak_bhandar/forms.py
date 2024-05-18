from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField, ValidationError, TextAreaField, DateField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, URL, NumberRange
from flask_wtf.file import FileField, FileAllowed
from pustak_bhandar.models import User
from flask_login import current_user

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
    description = TextAreaField('Description', validators=[DataRequired()])
    first_para = TextAreaField('Another Details')
    second_para = TextAreaField('Another Details')
    third_para = TextAreaField('Another Details')
    fourth_para = TextAreaField('Another Details')
    fifth_para = TextAreaField('Another Details')
    genre = StringField('Genre', validators=[DataRequired()])
    cover_image = FileField('Book Image', validators=[FileAllowed(['jpg', 'png']), DataRequired()])
    link = StringField('Link', validators=[DataRequired(), URL()])
    date_published = DateField('Published Date', format='%Y-%m-%d')
    author_name = StringField('Author Name', validators=[DataRequired()])
    about = StringField('About', validators=[DataRequired()])
    image = FileField('Image', validators=[DataRequired()])
    submit = SubmitField('Add Book')
    
class ReviewForm(FlaskForm):
    rating = IntegerField('Rating', validators=[DataRequired(), NumberRange(min=1, max=5)])
    review_text = TextAreaField('Review')
    submit = SubmitField('Submit Review')

class ArticleForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    section1 = StringField('Section 1', validators=[DataRequired()])
    section1_data = TextAreaField('Section1 Data', validators=[DataRequired()])
    section2 = StringField('Section 2')
    section2_data = TextAreaField('Section2 Data')
    section3 = StringField('Section 3')
    section3_data = TextAreaField('Section3 Data')
    section4 = StringField('Section 4')
    section4_data = TextAreaField('Section4 Data')
    section5 = StringField('Section 5')
    section5_data = TextAreaField('Section5 Data')
    conclusion = StringField('Conclusion')
    conclusion_data = TextAreaField('Conclusion Data')
    cover_image = FileField('Article Image', validators=[FileAllowed(['jpg', 'png']), DataRequired()])
    date_written = DateField('Date Written', validators=[DataRequired( )])
    submit = SubmitField('Add Article')
    
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['png', 'jpg'])])
    submit = SubmitField('Update Account')
    
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')