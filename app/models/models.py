from hashlib import md5
from sqlalchemy import String, DateTime
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from flask import redirect, url_for
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin
from flask_login import current_user

import bleach
from markdown import markdown

from app.models import db

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    isAdmin = db.Column(db.Boolean, nullable=False)
    password_hash = db.Column(String(256))
    profile_image = db.Column(String(256))
    info = db.Column(String(256))
    posts = db.relationship('Post', back_populates='user', cascade='all, delete-orphan')
    comments = db.relationship('Comment', back_populates='user', cascade='all, delete-orphan')


    def __repr__(self):
        return f'{self.username}, {self.email}'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        self.profile_image = f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
        return self.profile_image



class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(String(250))
    title_html = db.Column(db.String(250))
    body = db.Column(String(2500))
    body_html = db.Column(db.String(2500))
    timestamp = db.Column(DateTime, default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='posts')
    comments = db.relationship('Comment', back_populates='post', cascade='all, delete-orphan')
    views = db.Column(db.Integer, server_default=str(0))

    def __repr__(self):
        if self.body_html:
            return f'{self.body_html}'
        return f'{self.body}'

    def get_comments_length(self):
        commments = Comment.query.filter_by(post_id=self.id).all()
        return len(commments)

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
        'h1', 'h2', 'h3', 'p']
        target.body_html = bleach.linkify(bleach.clean(
        markdown(value, output_format='html'),
        tags=allowed_tags, strip=True))

    @staticmethod
    def on_changed_title(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
        'h1', 'h2', 'h3', 'p']
        target.title_html = bleach.linkify(bleach.clean(
        markdown(value, output_format='html'),
        tags=allowed_tags, strip=True))

db.event.listen(Post.body, 'set', Post.on_changed_body)
db.event.listen(Post.title, 'set', Post.on_changed_title)

class MyModelView(ModelView):
    def is_accessible(self):
        if current_user.isAdmin:
            return current_user.is_authenticated
        else:
            return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.login'))



class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(String(1000))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post = db.relationship('Post', back_populates='comments')
    user = db.relationship('User', back_populates='comments')
    timestamp = db.Column(DateTime, default=func.now())

    def __repr__(self):
        return f'{self.content}'


