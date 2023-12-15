from app import create_app
from app.models.models import User
from unittest import TestCase
from flask_login import login_user


class TestDb(TestCase):
    def setUp(self):
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SECRET_KEY": 'MY_SECRET_TESTING_KEY',
            "TESTING": True
        })
        from app.models import db
        self.db = db
        with self.app.app_context():
            db.create_all()

    def test_new_user(self):
        with self.app.app_context():
            user = User(username='olena', email='olena@gmail.com', isAdmin=False)
            user.set_password('123')
            self.db.session.add(user)
            self.db.session.commit()

            assert user.username == 'olena'
            assert user.email == 'olena@gmail.com'
            assert user.isAdmin == False
            assert user.check_password('123')

    def test_login(self):
        with self.app.app_context():
            user = User(username='olena', email='olena@gmail.com', isAdmin=False)
            user.set_password('123')
            self.db.session.add(user)
            self.db.session.commit()

            client = self.app.test_client()
            r = client.post('/login', data={
                'email': 'olena@gmail.com', 'password': '123'})
            assert r.status_code == 200

    def test_home(self):
        with self.app.app_context():
            with self.app.test_request_context():
                client = self.app.test_client()

                login_user(User(username='olena', email='olena@gmail.com', isAdmin=False))
                response = client.get("/home")
                assert response.status_code == 200
                assert b"Sort by" in response.data
