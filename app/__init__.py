from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_admin import Admin

from app.errors.errors import error_blueprint
from app.routes.routes import blueprint
from config import Config
from flask_bootstrap import Bootstrap
from flask_pagedown import PageDown

def create_app(test_config=None):
    # # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # app.config.from_mapping(
    #     SECRET_KEY='dev',
    #     DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    # )
    #
    # if test_config is None:
    #     # load the instance config, if it exists, when not testing
    #     app.config.from_pyfile('config.py', silent=True)
    # else:
    #     # load the test config if passed in
    #     app.config.from_mapping(test_config)
    #
    # # ensure the instance folder exists
    # try:
    #     os.makedirs(app.instance_path)
    # except OSError:
    #     pass
    #
    # # a simple page that says hello
    # @app.route('/hello')
    # def hello():
    #     return 'Hello, World!'
    #
    # return app
    app.config.from_object(Config)

    from app.models import db
    db.init_app(app)

    Bootstrap(app)
    PageDown(app)
    migrate = Migrate(app, db, render_as_batch=True)

    login = LoginManager(app)
    login.login_view = 'main.login'
    login.init_app(app)

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

    return app






