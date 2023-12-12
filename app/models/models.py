from app import db, login

from hashlib import md5

from sqlalchemy import String, DateTime
from sqlalchemy.sql import func

from werkzeug.security import generate_password_hash, check_password_hash
from flask import redirect, url_for
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin
from flask_login import current_user



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

    @login.user_loader
    def load_user(id):
        return db.session.get(User, int(id))

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
    body = db.Column(String(2500))
    timestamp = db.Column(DateTime, default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='posts')
    comments = db.relationship('Comment', back_populates='post', cascade='all, delete-orphan')
    views = db.Column(db.Integer, server_default=str(0))

    def __repr__(self):
        return f'{self.body}'

    def get_comments_length(self):
        commments = Comment.query.filter_by(post_id=self.id).all()
        return len(commments)


class MyModelView(ModelView):
    def is_accessible(self):
        if current_user.isAdmin:
            return current_user.is_authenticated
        else:
            return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))



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


