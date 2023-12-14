from app.models.models import User
from unittest import TestCase

from app import db, User

class TestDb(TestCase):
    def setUp(self):
        db.init_app('sqlite://')
        db.create_all()
        user = User(username='olena', email='olena@gmail.com', isAdmin=False)
        user.set_password('123')
        db.session.add(user)
        db.commit()

    def test_new_user(self):
        user = User(username='olena', email='olena@gmail.com', isAdmin=False)
        user.set_password('123')
        assert user.username == 'olena'
        assert user.email == 'olena@gmail.com'
        assert user.isAdmin == False
        assert user.check_password('123')


# from app import app
# import http
# from unittest.mock import patch

class UserModelTest(TestCase):
    # def setUp(self) -> None:
    #     self.client = app.test_client()
    #
    # def test_departments(self):
    #     with patch(
    #             'app.views.department_view.requests'
    #     ) as requests_mock:
    #         response = self.client.get('/')
    #         self.assertEqual(http.HTTPStatus.OK, response.status_code)
    #         requests_mock.get.assert_called_once_with('http://localhost/api/departments')

    def test_new_user(self):
        user = User(username='olena', email='olena@gmail.com', isAdmin=False)
        user.set_password('123')
        assert user.username == 'olena'
        assert user.email == 'olena@gmail.com'
        assert user.isAdmin == False
        assert user.check_password('123')
