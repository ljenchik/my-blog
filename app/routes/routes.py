from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlsplit
from app import app, db
from app.forms.login_form import LoginForm
from app.forms.register_form import RegisterForm
from app.forms.update_profile_form import UpdateProfileForm
from app.forms.post_form import PostForm
from app.forms.update_post_form import UpdatePostForm
from app.forms.delete_post_form import DeletePostForm
from app.forms.comment_form import CommentForm
from app.models.models import User, Post, Comment


@app.route('/')
@app.route('/home')
@login_required
def index():
    posts = Post.query.all()
    return render_template("index.html", title='Home Page', posts=posts)


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
        return redirect(url_for('user', username=username))
    user.profile_image = user.get_avatar(128)
    posts = Post.query.filter_by(user_id=user.id).all()
    return render_template('profile.html', user=user, form=form, posts=posts)


@app.route('/update_profile', methods=["GET", "POST"])
@login_required
def update_profile():
    form = UpdateProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.info = form.info.data
        # current_user.profile_image = form.profile_image.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.info.data = current_user.info
        # form.profile_image.data = current_user.profile_image
    return render_template('update_profile_form.html',
                           form=form)


@app.route('/update_post/<id>', methods=["GET", "POST"])
@login_required
def update_post(id):
    post = Post.query.filter_by(id=id).first_or_404()
    user = User.query.filter_by(id=post.user_id).first_or_404()

    update_post_form = UpdatePostForm()
    delete_post_form = DeletePostForm()

    if update_post_form.validate_on_submit():
        updated_post = Post(body=update_post_form.post.data, user_id=user.id)
        post.body = updated_post.body
        db.session.commit()
        flash('Your post has been changed.')
        return redirect(url_for('user', username=user.username))
    elif request.method == 'GET':
        update_post_form.post.data = post.body
    return render_template('manage_post.html',
                           update_post_form=update_post_form, delete_post_form=delete_post_form, id=id)


@app.route('/delete_post/<id>', methods=["GET", "POST"])
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first_or_404()
    user = User.query.filter_by(id=post.user_id).first_or_404()

    update_post_form = UpdatePostForm()
    delete_post_form = DeletePostForm()

    if delete_post_form.validate_on_submit():
        db.session.delete(post)
        db.session.commit()
        flash('Your post has been deleted.')
        return redirect(url_for('user', username=user.username))
    elif request.method == 'GET':
        update_post_form.post.data = post.body
    return render_template('manage_post.html', 
                           update_post_form=update_post_form, delete_post_form=delete_post_form, id=id)


@app.route('/post/<id>', methods=["GET", "POST"])
@login_required
def post(id):
    post = Post.query.filter_by(id=id).first_or_404()
    if not post.views:
        post.views = 1
    else:
        post.views += 1
    db.session.commit()
    post_author = User.query.filter_by(id=post.user_id).first_or_404()
    form = CommentForm()
    if form.validate_on_submit():
            new_comment = Comment()
            new_comment.content = form.content.data
            new_comment.post_id = id
            new_comment.user_id = current_user.id
            db.session.add(new_comment)
            db.session.commit()
            flash('Your comment has been added.')
            return redirect(url_for('post', id=id))

    comments = Comment.query.filter_by(post_id=id).order_by(Comment.timestamp.desc()).all()
    return render_template('post.html',
                           post=post,
                           title='Add comment',
                           form=form, post_author=post_author, comments=comments)


@app.route('/sort/<sort_by>', methods=["GET", "POST"])
@login_required
def sort(sort_by):
    if sort_by == 'date':
        posts = Post.query.order_by(Post.timestamp.desc()).all()
        print(posts)
        return render_template("index.html", title='Home Page', posts=posts)
    elif sort_by == 'popularity':
        posts = Post.query.order_by(Post.views.desc()).all()
        return render_template("index.html", title='Home Page', posts=posts)

    

    


