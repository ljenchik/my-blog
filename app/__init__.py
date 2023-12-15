import os

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_admin import Admin

from app.errors.errors import error_blueprint
from app.routes.routes import blueprint
from config import Config
from flask_bootstrap import Bootstrap
from flask_pagedown import PageDown

migrate = Migrate()
bootstrap=Bootstrap()
pagedown=PageDown()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_object(Config)
    else:
        app.config.from_mapping(test_config)

    from app.models import db
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    login = LoginManager(app)
    login.login_view = 'main.login'
    login.init_app(app)

    bootstrap.init_app(app)
    pagedown.init_app(app)

    @login.user_loader
    def load_user(id):
        return db.session.get(User, int(id))

    from app.models.models import Post, User, MyModelView, Comment
    admin = Admin(app, name='my-blog', template_mode='bootstrap3')
    admin.add_view(MyModelView(User, db.session))
    admin.add_view(MyModelView(Post, db.session))
    admin.add_view(MyModelView(Comment, db.session))

    app.register_blueprint(blueprint)
    app.register_blueprint(error_blueprint)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app






