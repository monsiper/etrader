from django.test import TestCase
from views import login_user

# Create your tests here.

# ./manage.py test

# class MyTest(

# pytest



def test_login_view():

    User.objects.creat()


    # now test
    test_request = request(type='GET')
    login_user(test_request)
    assert 3 == 2 + 1




if __name__ == "__main__":
    test_login_view()
    test_foo()

