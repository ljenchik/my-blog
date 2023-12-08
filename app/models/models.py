from hashlib import md5
from sqlalchemy import String, DateTime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func
from app import db, login
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    isAdmin = db.Column(db.Boolean, nullable=False)
    password_hash = db.Column(String(256))
    profile_image = db.Column(String(256))
    info = db.Column(String(256))
    posts = db.relationship('Post', backref='user', lazy=True)


    def __repr__(self):
        return f'User {self.username}, {self.email}'

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
    body = db.Column(String(140))
    timestamp = db.Column(DateTime, default=func.now())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'Post {self.body}'
