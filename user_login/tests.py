from django.contrib.auth.models import User, AnonymousUser
from django.core.urlresolvers import reverse
from django.test import TestCase
from views import login_user

# Create your tests here.

# ./manage.py test

# class MyTest(

# pytest
from django.test import Client

class TestUser(TestCase):

    def test_is_authenticated(self):

        user = User.objects.create_user(username='john@adams.com', email='john@adams.com', password='smith')
        self.assertEqual(user.is_authenticated(), True)
        user = AnonymousUser()
        self.assertEqual(user.is_authenticated(), False)


    def test_create_user(self):

        user = User.objects.create_user(username='m@m.com')
        self.assertTrue(user)
        try:
            user = User.objects.create_user(username='')
        except:
            self.assertTrue(ValueError)


class TestLogin(TestCase):

    def test_login_view_fails(self):

        c = Client()
        response = c.post('/login/', {'email': 'john@adams.com', 'password': 'smith'})
        # from ipdb import set_trace
        # print response.content
        self.assertTrue("could not authenticate" in response.content)
        self.assertEqual(response.status_code, 401)

    def test_login_view_succeeds(self):
        c = Client()
        User.objects.create_user(username='john@adams.com', email='john@adams.com', password='smith')

        u = User.objects.first()
        u.set_password('smith')
        u.save()

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.filter(email='john@adams.com').count(), 1)
        response = c.post('/login/', {'email': 'john@adams.com', 'password': 'smith'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard'))

