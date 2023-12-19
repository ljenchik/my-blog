from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from app.forms.login_form import LoginForm
from app.forms.register_form import RegisterForm
from app.forms.update_profile_form import UpdateProfileForm
from app.forms.post_form import PostForm
from app.forms.update_post_form import UpdatePostForm
from app.forms.delete_post_form import DeletePostForm
from app.forms.comment_form import CommentForm
from app.forms.dropdown_form import DropdownForm
from app.models import db
from app.models.models import User, Post, Comment
from flask import Blueprint

blueprint = Blueprint('main', __name__)


@blueprint.route('/', methods=["GET", "POST"])
@blueprint.route('/home', methods=["GET", "POST"])
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 2
    posts = Post.query.filter().paginate(page=page, per_page=per_page, error_out=False)
    form = DropdownForm()
    return render_template("index.html", posts=posts, form=form)


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first_or_404()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('main.login'))
        login_user(user)
        return redirect(url_for('main.index'))
    return render_template('login_form.html', form=form)


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@blueprint.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User()
        new_user.username = form.username.data
        new_user.email = form.email.data
        new_user.isAdmin = False
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Congratulations, you have registered!')
        return redirect(url_for('main.login'))
    return render_template('register_form.html', form=form)


@blueprint.route('/user/<username>', methods=["GET", "POST"])
@login_required
def user(username):
        user = User.query.filter_by(username=username).first_or_404()
        print(user.id)
        form = PostForm()
        page = request.args.get('page', 1, type=int)
        per_page = 2
        if form.validate_on_submit():
            new_post = Post()
            new_post.title=form.title.data
            new_post.body=form.post.data
            new_post.user_id=user.id
            db.session.add(new_post)
            db.session.commit()
            flash('Your post has been saved.')
            return redirect(url_for('main.user', username=username))
        user.profile_image = user.get_avatar(128)
        posts = Post.query.filter_by(user_id=user.id).order_by(Post.timestamp.desc())
        posts_count = Post.query.filter_by(user_id=user.id).order_by(Post.timestamp.desc()).count()
        print(posts_count)
        if posts_count > 0:
            paginated_posts = posts.paginate(page=page, per_page=per_page, error_out=False)
            return render_template('profile.html', user=user, form=form, posts=paginated_posts)
        else:
            return render_template('profile.html', user=user, form=form)


@blueprint.route('/update_profile', methods=["GET", "POST"])
@login_required
def update_profile():
    form = UpdateProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.info = form.info.data
        # current_user.profile_image = form.profile_image.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.info.data = current_user.info
        # form.profile_image.data = current_user.profile_image
    return render_template('update_profile_form.html',
                           form=form)


@blueprint.route('/update_post/<id>', methods=["GET", "POST"])
@login_required
def update_post(id):
    post = Post.query.filter_by(id=id).first_or_404()
    user = User.query.filter_by(id=post.user_id).first_or_404()

    update_post_form = UpdatePostForm()
    delete_post_form = DeletePostForm()

    if update_post_form.validate_on_submit():
        updated_post = Post(body=update_post_form.post.data, user_id=user.id, title=update_post_form.title.data)
        post.title = updated_post.title
        post.body = updated_post.body
        db.session.commit()
        flash('Your post has been changed.')
        return redirect(url_for('main.user', username=user.username))
    elif request.method == 'GET':
        update_post_form.post.data = post.body
        update_post_form.title.data = post.title
    return render_template('manage_post.html',
                           update_post_form=update_post_form, delete_post_form=delete_post_form, id=id)


@blueprint.route('/delete_post/<id>', methods=["GET", "POST"])
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
        return redirect(url_for('main.user', username=user.username))
    elif request.method == 'GET':
        update_post_form.post.data = post.body
        update_post_form.title.data = post.title
    return render_template('manage_post.html', 
                           update_post_form=update_post_form, delete_post_form=delete_post_form, id=id)


@blueprint.route('/post/<id>', methods=["GET", "POST"])
@login_required
def post(id):
    post = Post.query.filter_by(id=id).first_or_404()
    post_author = User.query.filter_by(id=post.user_id).first_or_404()
    if not post.views and post_author != current_user:
        post.views = 1
    elif post.views and post_author != current_user:
        post.views += 1
    db.session.commit()
    form = CommentForm()
    if form.validate_on_submit():
            new_comment = Comment()
            new_comment.content = form.content.data
            new_comment.post_id = id
            new_comment.user_id = current_user.id
            db.session.add(new_comment)
            db.session.commit()
            flash('Your comment has been added.')
            return redirect(url_for('main.post', id=id))

    comments = Comment.query.filter_by(post_id=id).order_by(Comment.timestamp.desc()).all()
    return render_template('post.html',
                           post=post,
                           title='Add comment',
                           form=form, post_author=post_author, comments=comments)


@blueprint.route('/sort/<sort_by>', methods=["GET", "POST"])
@login_required
def sort(sort_by):
    form=DropdownForm()
    page = request.args.get('page', 1, type=int)
    per_page = 2
    if sort_by == 'newest':
        posts = Post.query.order_by(Post.timestamp.desc()).paginate(page=page, per_page=per_page, error_out=False)
        return render_template("index.html", posts=posts, form=form, sort_by=sort_by)
    elif sort_by == 'oldest':
        posts = Post.query.order_by(Post.timestamp.asc()).paginate(page=page, per_page=per_page, error_out=False)
        return render_template("index.html",  posts=posts, form=form, sort_by=sort_by)
    elif sort_by == 'popular':
        posts = Post.query.order_by(Post.views.desc()).paginate(page=page, per_page=per_page, error_out=False)
        return render_template("index.html", posts=posts, form=form, sort_by=sort_by)
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template("index.html", posts=posts, form=form)

    

    


