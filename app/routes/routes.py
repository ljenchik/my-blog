from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required

from app import app, db
from app.forms.login_form import LoginForm
from app.forms.register_form import RegisterForm
from app.models.models import User


@app.route('/')
@app.route('/home')
@login_required
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'user': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'user': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html", title='Home Page', user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first_or_404()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(f'/user/{user.username}')
    return render_template('login_form.html', title='Log in', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User()
        new_user.username = form.username.data
        new_user.email = form.email.data
        new_user.isAdmin = False
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register_form.html', title='Register', form=form)
