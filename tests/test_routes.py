import os
import re

import flask

from app import create_app
from app.models.models import User, Post
from unittest import TestCase
from flask_login import login_user, current_user
from flask import current_app

from config import basedir


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
            self.populate_db()
            self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()
        self.app = None
        self.app_context = None

    def test_app(self):
        assert self.app is not None
        assert current_app == self.app

    def populate_db(self):
        user = User()
        user.username = 'olena'
        user.email = 'olena@gmail.com'
        user.isAdmin = False
        user.set_password('123')
        self.db.session.add(user)
        self.db.session.commit()
        found_user = User.query.filter_by(username=user.username).first_or_404()
        assert str(found_user) == f'{user.username}, {user.email}'



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
            assert number == 2

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
            assert number == 3

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

    def test_register_user_wrong_username(self):
        with self.app.app_context():
            client = self.app.test_client()
            response = client.post('/register', data={
                'username': 'ben',
                'email': 'ben@gmail.com',
                'password': '123',
                'confirm_password': '123',
            }, follow_redirects=True)

            assert response.status_code == 200

            response = client.post('/register', data={
                'username': 'ben',
                'email': 'benji@gmail.com',
                'password': '123',
                'confirm_password': '123',
            }, follow_redirects=True)

            assert response.status_code == 200
            html = response.get_data(as_text=True)
            assert 'Please use a different username' in html

    def test_register_user_wrong_email(self):
        with self.app.app_context():
            client = self.app.test_client()
            response = client.post('/register', data={
                'username': 'benji',
                'email': 'ben@gmail.com',
                'password': '123',
                'confirm_password': '123',
            }, follow_redirects=True)

            assert response.status_code == 200

            response = client.post('/register', data={
                'username': 'ben',
                'email': 'ben@gmail.com',
                'password': '1234',
                'confirm_password': '1234',
            }, follow_redirects=True)

            assert response.status_code == 200
            html = response.get_data(as_text=True)
            assert 'Please use a different email address' in html

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

    def login(self):
        self.client.post('/login', data={
            'email': 'olena@gmail.com',
            'password': '123',
        })

    def test_profile_page_get(self):
        with self.app.app_context():
            with self.app.test_request_context():
                client = self.app.test_client()
                self.login()
                response = client.get(f'/user/olena', follow_redirects=True)
                assert response.status_code == 200
                html = response.get_data(as_text=True)
                assert 'olena' in html
                assert 'Update profile' in html
                assert 'Create a new post' in html
                assert 'Title (Markdown enabled)' in html
                assert 'Content (Markdown enabled)' in html

    def test_access_failed(self):
        with self.app.app_context():
            client = self.app.test_client()
            response = client.get('/home',
                                  follow_redirects=True)
            assert response.status_code == 200
            html = response.get_data(as_text=True)
            assert 'Please log in to access this page' in html

    def test_admin_access(self):
        with self.app.app_context():
            with self.app.test_request_context():
                client = self.app.test_client()
                user = User()
                user.username = 'benji'
                user.email = "benji@gmail.com"
                user.isAdmin = True
                user.set_password('123')
                login_user(user)
                response = client.get('/home', follow_redirects=True)
                assert response.status_code == 200
                html = response.get_data(as_text=True)
                assert 'Admin view' in html

    def test_admin_access_failed(self):
        with self.app.app_context():
            with self.app.test_request_context():
                client = self.app.test_client()
                user = User()
                user.username = 'benji'
                user.email = "benji@gmail.com"
                user.isAdmin = False
                user.set_password('123')
                login_user(user)
                response = client.get('/home', follow_redirects=True)
                assert response.status_code == 200
                html = response.get_data(as_text=True)
                assert 'Admin view' not in html

    def test_register_user_mismatched_passwords(self):
        with self.app.app_context():
            client = self.app.test_client()
            response = client.post('/register', data={
                'username': 'ben',
                'email': 'ben@gmail.com',
                'password': '123',
                'confirm_password': '321',
            })
            assert response.status_code == 200
            html = response.get_data(as_text=True)
            assert 'Field must be equal to password.' in html

    def test_create_post(self):
         with self.app.app_context():
            client = self.app.test_client()
            self.login()
            response = client.post('/user/olena', data={'title': 'Title 1', 'post': 'Post body 1', 'user_id': 1},
                                    follow_redirects=True)
            assert response.status_code == 200
            assert '/user/olena' in response.request.path
            html = response.get_data(as_text=True)
            assert "olena's posts" in html
            assert "Title 1" in html
            assert "Post body 1" in html
            assert "Posted on" in html
