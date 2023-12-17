import flask

from app import create_app
from app.models.models import User
from unittest import TestCase
from flask_login import login_user, current_user
from flask import current_app


class TestApp(TestCase):
    def setUp(self):
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SECRET_KEY": 'MY_SECRET_TESTING_KEY',
            "TESTING": True,
            "WTF_CSRF_ENABLED": False
        })
        self.app_context = self.app.app_context()
        self.app_context.push()

        from app.models import db
        self.db = db
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        self.app_context.pop()
        self.app = None
        self.app_context = None

    def test_app(self):
        assert self.app is not None
        assert current_app == self.app

    def test_adding_new_user(self):
        with self.app.app_context():
            user = User()
            user.username = 'ben'
            user.email = "ben@gmail.com"
            user.isAdmin = False
            user.set_password('123')
            self.db.session.add(user)
            self.db.session.commit()

            assert user.username == 'ben'
            assert user.email == 'ben@gmail.com'
            assert user.isAdmin == False
            assert user.check_password('123')
            my_query = self.db.func.count(User.id)
            number = self.db.session.execute(my_query).scalar()
            assert number == 1

    def test_adding_new_users(self):
        with self.app.app_context():
            user = User()
            user.username = 'ben'
            user.email = "ben@gmail.com"
            user.isAdmin = False
            user.set_password('123')
            self.db.session.add(user)
            self.db.session.commit()

            user = User()
            user.username = 'harry'
            user.email = "harry@gmail.com"
            user.isAdmin = False
            user.set_password('123')
            self.db.session.add(user)
            self.db.session.commit()

            my_query = self.db.func.count(User.id)
            number = self.db.session.execute(my_query).scalar()
            assert number == 2

    def test_register_form_get(self):
        with self.app.app_context():
            client = self.app.test_client()
            response = client.get('/register', follow_redirects=True)
            assert response.status_code == 200
            html = response.get_data(as_text=True)
            assert 'Username' in html
            assert 'Email' in html
            assert 'Password' in html
            assert 'Confirm password' in html
            assert 'name="submit' in html
            assert 'Register' in html
            assert 'Sign Up' in html
            # Navbar
            assert 'My Blog' in html
            assert 'Home' in html
            assert 'Login' in html
            assert 'Logout' in html
            assert 'Profile' in html
            assert 'Add post' in html

    def test_register_user_post(self):
        with self.app.app_context():
            client = self.app.test_client()
            response = client.post('/register', data={
                'username': 'ben',
                'email': 'ben@gmail.com',
                'password': '123',
                'confirm_password': '123',
            }, follow_redirects=True)

            assert response.status_code == 200
            assert 'login' in response.request.path

            response = client.post('/login', data={
                'email': 'ben@gmail.com',
                'password': '123',
            }, follow_redirects=True)

            assert response.status_code == 200
            assert '/home' in response.request.path

            html = response.get_data(as_text=True)
            assert 'Hi, ben!' in html
            # Navbar
            assert 'My Blog' in html
            assert 'Home' in html
            assert 'Login' in html
            assert 'Logout' in html
            assert 'Profile' in html
            assert 'Add post' in html

    def test_login_form_get(self):
        with self.app.app_context():
            client = self.app.test_client()
            response = client.get('/login', follow_redirects=True)
            assert response.status_code == 200
            html = response.get_data(as_text=True)
            assert 'Email' in html
            assert 'Password' in html
            assert 'Log in' in html
            # Navbar
            assert 'My Blog' in html
            assert 'Home' in html
            assert 'Login' in html
            assert 'Logout' in html
            assert 'Profile' in html
            assert 'Add post' in html

    def test_login_post(self):
        with self.app.app_context():
            user = User()
            user.username = 'ben'
            user.email = "ben@gmail.com"
            user.isAdmin = False
            user.set_password('123')
            self.db.session.add(user)
            self.db.session.commit()
            client = self.app.test_client()
            response = client.post('/login', data={
                'email': 'ben@gmail.com', 'password': '123'}, follow_redirects=True)
            assert response.status_code == 200
            assert '/home' in response.request.path

            html = response.get_data(as_text=True)
            assert 'Hi, ben!' in html
            # Navbar
            assert 'My Blog' in html
            assert 'Home' in html
            assert 'Login' in html
            assert 'Logout' in html
            assert 'Profile' in html
            assert 'Add post' in html

    def test_home_page(self):
        with self.app.app_context():
            with self.app.test_request_context():
                client = self.app.test_client()
                user = User()
                user.username = 'sue'
                user.email = "sue@gmail.com"
                user.isAdmin = False
                user.set_password('123')
                login_user(user)
                response = client.get('/home')
                assert current_user.username == 'sue'
                assert user.is_authenticated == True
                assert response.status_code == 200
                html = response.get_data(as_text=True)
                assert 'Hi, sue!' in html
                assert "Sort by" in html

    def test_profile_page(self):
        with self.app.app_context():
            with self.app.test_request_context():
                client = self.app.test_client()
                # user = User()
                # user.username = 'ben'
                # user.email = "ben@gmail.com"
                # user.isAdmin = False
                # user.set_password('123')
                # login_user(user)
                self.login()
                response = client.get('/user/susan',
                                      follow_redirects=True)
                assert current_user.username == 'susan'
                print("==============Response", response.text)
                assert response.status_code == 200
                # assert b"ben" in response.data
