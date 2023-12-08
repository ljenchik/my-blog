from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlsplit
from app import app, db
from app.forms.login_form import LoginForm
from app.forms.register_form import RegisterForm
from app.forms.post_form import PostForm
from app.models.models import User, Post


@app.route('/')
@app.route('/home')
@login_required
def index():
    posts = Post.query.all()
    return render_template("index.html", title='Home Page', posts=posts, user=current_user)


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
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
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


@app.route('/user/<username>', methods=["GET", "POST"])
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post()
        new_post.body=form.post.data
        new_post.user_id=user.id
        db.session.add(new_post)
        db.session.commit()
        flash('Your post has been saved.')
    user.profile_image = user.get_avatar(128)
    posts = Post.query.filter_by(user_id=user.id)
    return render_template('profile.html', user=user, form=form, posts=posts)
