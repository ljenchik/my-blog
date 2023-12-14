from app.models.models import User

def test_new_user():
    user = User(username='olena', email='olena@gmail.com', isAdmin=False)
    user.set_password('123')
    assert user.username == 'olena'
    assert user.email == 'olena@gmail.com'
    assert user.isAdmin == False
    assert user.password_hash == user.check_password('123')
