from flask import Flask, render_template, flash, redirect, url_for
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '023772ef3f65adc59f6ef24456d09d4d0fec1b86f52a10712e4d8459737107e7'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/store')
def store():
    return render_template('store.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}", "success")
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data=='aman@gmail.com' and form.password.data=='1234':
            return redirect(url_for('account'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/account')
def account():
    return f"hello"

if __name__ == '__main__':
    app.run(debug=True)