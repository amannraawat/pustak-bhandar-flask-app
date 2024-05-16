from flask import render_template, flash, redirect, url_for, request, Blueprint
from pustak_bhandar.forms import RegistrationForm, LoginForm, BookForm, ArticleForm, UpdateAccountForm
from pustak_bhandar.models import User, Book, Article, Author, Favourite
from pustak_bhandar import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import base64
import secrets, os
from PIL import Image

app.config['UPLOAD_FOLDER'] = 'static/images/book_covers'
errors = Blueprint('errors', __name__)

@app.route('/')
def home():
    book_ids = [1,2,3]
    article_ids = [1,2,3]
    articles = Article.query.filter(Article.id.in_(article_ids)).all()
    books = Book.query.join(Author).filter(Book.id.in_(book_ids)).all()

    for book in books:
        if book.image_data:
            book.image_data = base64.b64encode(book.image_data).decode('utf-8')
            
        if book:
            book.short_description = book.description[:100] + '...' if len(book.description)>100 else book.description
    
    for article in articles:
        if article.image_data:
            article.image_data = base64.b64encode(article.image_data).decode('utf-8')
        
        if article:
            article.short_title = article.title[:24] + '...' if len(article.title)>24 else article.title
            article.short_description = article.description[:50] + '...' if len(article.description)>50 else article.title
    return render_template('index.html', books=books, articles=articles)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/author/<int:author_id>')
def author(author_id):
    author = Author.query.get_or_404(author_id)
    books = Book.query.filter_by(author_id=author_id).all()
    
    if author.image_data:
        author.image_data = base64.b64encode(author.image_data).decode('utf-8')
    
    for book in books:
        if book.image_data:
            book.image_data = base64.b64encode(book.image_data).decode('utf-8')
    
    return render_template('author.html', title='Author', author=author, books=books)

@app.route('/store')
def store():
    page = request.args.get('page', 1, type=int)
    books = Book.query.join(Author).order_by(Book.id.desc()).paginate(page=page, per_page=12)
    
    for book in books:
        if book.image_data:
            book.image_data = base64.b64encode(book.image_data).decode('utf-8')
    
    return render_template('store.html', books=books, title='Store')

@app.route('/add_favourite/<int:book_id>', methods=['POST'])
@login_required
def add_favourite(book_id):
    book=Book.query.get_or_404(book_id)
    user_favourite = Favourite.query.filter_by(user_id=current_user.id, book_id=book.id).first()
    if not user_favourite:
        favourite=Favourite(user_id=current_user.id, book_id=book.id)
        db.session.add(favourite)
        db.session.commit()
        flash('Book added to favourites!', 'success')
    else:
        flash('Book is already in favourites!', 'info')
    return redirect(url_for('home'))

@app.route('/remove_favourite/<int:book_id>', methods=['POST'])
@login_required
def remove_favourite(book_id):
    if current_user.is_authenticated:
        book=Book.query.get_or_404(book_id)
        favourite=Favourite.query.filter_by(user_id=current_user.id, book_id=book_id).first()
        if favourite:
            db.session.delete(favourite)
            db.session.commit()
            flash('Book removed from favourites', 'success')
        else:
            flash('Book is not in favourites', 'info')
    else:
        flash('Please login to remove books from favourites', 'info')
    return redirect(url_for('home'))

@app.route('/favourites')
@login_required
def favourites():
    favourites=Favourite.query.filter_by(user_id=current_user.id).all()
    favourite_books=[favourite.book for favourite in favourites]
    
    for book in favourite_books:
        if book.image_data:
            book.image_data = base64.b64encode(book.image_data).decode('utf-8')
            
    return render_template('favourite.html', favourite_books=favourite_books)

@app.route('/store/<int:book_id>')
@login_required
def single_product(book_id):
    book = Book.query.join(Author).filter(Book.id==book_id).first()
    is_favourite=False
    if not current_user.is_anonymous:
        is_favourite = Favourite.query.filter_by(user_id=current_user.id, book_id=book_id).first()
    
    if book.image_data:
        book.image_data = base64.b64encode(book.image_data).decode('utf-8')
    
    return render_template('single_product.html', book=book, is_favourite=is_favourite)

@app.route('/article')
def article():
    page = request.args.get('page', 1, type=int)
    articles = Article.query.order_by(Article.id.desc()).paginate(page=page, per_page=5)
    
    for article in articles:
        if article.image_data:
            article.image_data = base64.b64encode(article.image_data).decode('utf-8')
        
        if article:
            article.short_description = article.description[:50] + '...' if len(article.description)>50 else article.title
    return render_template('article.html', articles=articles, title='Article')

@app.route('/articel/<int:article_id>')
def single_article(article_id):
    article = Article.query.get_or_404(article_id)
    
    if article.image_data:
        article.image_data = base64.b64encode(article.image_data).decode('utf-8')
        
    return render_template('single_article.html', article=article)

@app.route('/best-sellling-book')
def best_selling():
    return render_template('one_book.html')

@app.route('/add-book', methods=['GET', 'POST'])
@login_required
def add_book():
    id = current_user.id
    if id == 1:
        
        form = BookForm()
    
        if request.method == "POST":
            if form.validate_on_submit():
                author_name = form.author_name.data
            
                author = Author.query.filter_by(name=author_name).first()
                if author is None:
                    author_image=form.image.data
                    image_data = author_image.read()
                    author = Author(name=author_name, about=form.about.data, image_data=image_data)
                    db.session.add(author)
                    db.session.commit()
            
                title = form.title.data
                description = form.description.data
                first_para = form.first_para.data
                second_para = form.second_para.data
                third_para = form.third_para.data
                fourth_para = form.fourth_para.data
                fifth_para = form.fifth_para.data
                genre = form.genre.data
                image_file = form.cover_image.data
                link = form.link.data
                date_published = form.date_published.data
                image_data = image_file.read()
        
                new_book = Book(title=title,
                                description=description, 
                                first_para=first_para, 
                                second_para=second_para, 
                                third_para=third_para, 
                                fourth_para=fourth_para, 
                                fifth_para=fifth_para, 
                                genre=genre, 
                                image_data=image_data, 
                                links=link, 
                                date_published=date_published,
                                author_id=author.id)
                db.session.add(new_book)

                try:
                    db.session.commit()
                    flash('New book is added to the application', 'success')
                    return redirect(url_for('home'))
                except Exception as e:
                    db.session.rollback()
                    print("Error:", e)
                    return "An error occurred while adding data to the database" 
        return render_template('add_book.html', form=form)
    
    else:
        flash('You must be the Admin to access the this page!....', 'info')
        return redirect(url_for('home'))

@app.route('/add-article', methods=['GET', 'POST'])
@login_required
def add_article():
    id = current_user.id
    if id == 1:
        
        form = ArticleForm()
        if form.validate_on_submit():
            title = form.title.data
            author = form.author.data
            description = form.description.data
            section1 = form.section1.data
            section1_data = form.section1_data.data
            section2 = form.section2.data
            section2_data = form.section2_data.data
            section3 = form.section3.data
            section3_data = form.section3_data.data
            section4 = form.section4.data
            section4_data = form.section4_data.data
            section5 = form.section5.data
            section5_data = form.section5_data.data
            conclusion = form.conclusion.data
            conclusion_data = form.conclusion_data.data
            image_file = form.cover_image.data
            date_written = form.date_written.data
        
            image_data = image_file.read()
        
            new_article = Article(title=title,
                                author=author, 
                                description=description, 
                                section1=section1, 
                                section1_data=section1_data, 
                                section2=section2, 
                                section2_data=section2_data,
                                section3=section3, 
                                section3_data=section3_data,
                                section4=section4, 
                                section4_data=section4_data,
                                section5=section5, 
                                section5_data=section5_data,
                                conclusion=conclusion, 
                                conclusion_data=conclusion_data, 
                                image_data=image_data, 
                                date_created=date_written)
            db.session.add(new_article)
            db.session.commit()
            flash('Your article has been added', 'success')
            return redirect(url_for('home'))
        return render_template('add_article.html', form=form)
    
    else:
        flash('You must be the Admin to access the this page!....', 'info')
        return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        username=form.username.data
        email = form.email.data
        
        hash_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=username, email=email, password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.username.data}! You are now able to log in.", "success")
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title='Signup')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', form=form, title='Login')

@app.route('/admin')
@login_required
def admin():
    id = current_user.id
    if id == 1:
        image_file = url_for('static', filename='images/profile_pictures/' + current_user.image_data)
        return render_template('admin.html', title='Admin', image_file=image_file)
    else:
        flash('You must be the Admin to access the Admin page!....', 'info')
        return redirect(url_for('home'))
    
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images/profile_pictures', picture_fn)
    
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    
    i.save(picture_path)
    
    return picture_fn

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
        
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_data = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.picture.data = current_user.image_data
    image_file = url_for('static', filename='images/profile_pictures/' + current_user.image_data)
    return render_template('account.html', image_file=image_file, form=form, title='Account')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.errorhandler(404)
def error_404(error):
    return render_template('404.html'), 404

@app.errorhandler(403)
def error_403(error):
    return render_template('403.htmml'), 403

@app.errorhandler(500)
def error_500(error):
    return render_template('500.html'), 500