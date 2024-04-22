from flask import render_template, flash, redirect, url_for, request
from pustak_bhandar.forms import RegistrationForm, LoginForm, BookForm, ArticleForm
from pustak_bhandar.models import User, Book, Article
from pustak_bhandar import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import base64

app.config['UPLOAD_FOLDER'] = 'static/images/book_covers'

@app.route('/')
def home():
    book_ids = [1,2,3]
    article_ids = [1,2,3]
    articles = Article.query.filter(Article.id.in_(article_ids)).all()
    books = Book.query.filter(Book.id.in_(book_ids)).all()
    
    for book in books:
        if book.image_data:
            book.image_data = base64.b64encode(book.image_data).decode('utf-8')
    
    for article in articles:
        if article.image_data:
            article.image_data = base64.b64encode(article.image_data).decode('utf-8')
        
        if article:
            article.short_title = article.title[:24] + '...' if len(article.title)>24 else article.title
            article.short_description = article.description[:50] + '...' if len(article.description)>50 else article.title
    return render_template('index.html', books=books, articles=articles)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/store')
def store():
    page = request.args.get('page', 1, type=int)
    books = Book.query.order_by(Book.id.desc()).paginate(page=page, per_page=2)
    
    for book in books:
        if book.image_data:
            book.image_data = base64.b64encode(book.image_data).decode('utf-8')
    
    return render_template('store.html', books=books)

@app.route('/store/<int:book_id>')
def single_product(book_id):
    book = Book.query.get(book_id)
    
    if book.image_data:
        book.image_data = base64.b64encode(book.image_data).decode('utf-8')
    
    return render_template('single_product.html', book=book)

@app.route('/article')
def article():
    articles = Article.query.all()
    
    short_array = []
    for article in articles:
        short_description = article.description[:100] + '...' if len(article.description) > 200 else article.description 
        if article.image_data:
            article.image_data = base64.b64encode(article.image_data).decode('utf-8')
            short_array.append((article.id, article.title, article.author, short_description, article.image_data, article.date_created))
    return render_template('article.html', articles=short_array)

@app.route('/articel/<int:article_id>')
def single_article(article_id):
    article = Article.query.get_or_404(article_id)
    
    if article.image_data:
        article.image_data = base64.b64encode(article.image_data).decode('utf-8')
        
    return render_template('single_article.html', article=article)

@app.route('/best-sellling-book')
def best_selling():
    return render_template('one_book.html')

# def save_picture(form_picture):
#     random_hex = secrets.token_hex(8)
#     _, f_ext = os.path.splitext(form_picture.filename)
#     picture_fn = random_hex + f_ext
#     picture_path = os.path.join(app.root_path, 'static/images/book_covers', picture_fn)
#     form_picture.save(picture_path)
    
    # return picture_fn

@app.route('/add-book', methods=['GET', 'POST'])
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        title = form.title.data
        author = form.author.data
        description = form.description.data
        genre = form.genre.data
        image_file = form.cover_image.data
        link = form.link.data
        date_published = form.date_published.data
        
        image_data = image_file.read()
        
        new_book = Book(title=title, author=author, description=description, genre=genre, image_data=image_data, links=link, date_published=date_published)
        db.session.add(new_book)
        db.session.commit()
        flash('Your book has been added', 'success')
        return redirect(url_for('home'))
    return render_template('add_book.html', form=form)

@app.route('/add-article', methods=['GET', 'POST'])
def add_article():
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
        
        new_article = Article(title=title, author=author, description=description, section1=section1, section1_data=section1_data, section2=section2, section2_data=section2_data,section3=section3, section3_data=section3_data,section4=section4, section4_data=section4_data,section5=section5, section5_data=section5_data,conclusion=conclusion, conclusion_data=conclusion_data, image_data=image_data, date_created=date_written)
        db.session.add(new_article)
        db.session.commit()
        flash('Your article has been added', 'success')
        return redirect(url_for('article'))
    return render_template('add_article.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.username.data}! You are now able to log in.", "success")
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

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
    return render_template('login.html', form=form)

@app.route('/admin')
@login_required
def admin():
    id = current_user.id
    if id == 1:
        return render_template('admin.html')
    else:
        flash('You must be the Admin to access the Admin page!....', 'info')
        return redirect(url_for('home'))

@app.route('/account')
@login_required
def account():
    return render_template('account.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))