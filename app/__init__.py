from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from config import Config

app = Flask(__name__)

app.config.from_object(Config)

db = SQLAlchemy(app)

migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'

from app.models.models import Post, User, MyModelView, Comment
admin = Admin(app, name='my-blog', template_mode='bootstrap3')
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Post, db.session))
admin.add_view(MyModelView(Comment, db.session))

from app.routes import routes
from app.models import models
from app.errors import errors
