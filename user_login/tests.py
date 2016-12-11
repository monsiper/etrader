from django.contrib.auth.models import User, AnonymousUser
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test import Client
from views import login_user

# Create your tests here.


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

    def test_login_view_with_GET(self):
        c = Client()
        response = c.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        c = Client()
        c.post('/login', {'email': 'a@d.com', 'password': 'ahmet'})
        response = c.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('main_page'))

class TestSignUp(TestCase):

    def test_signup_view_with_GET(self):
        c = Client()
        response = c.get('/signup/')
        self.assertEqual(response.status_code, 200)

    def test_signup_view_fails(self):
        c = Client()

        #test case: no first_name was provided
        response = c.post('/signup/',{'last_name': 'keser',
                                      'password': 'ahmet', 'email': 'john@adams.com'})
        self.assertEqual(response.status_code, 400)

        #test_case: invalid email
        response = c.post('/signup/',{'first_name': 'mehmet', 'last_name': 'keser',
                                      'password': 'ahmet', 'email': 'john.adam.com'})
        self.assertEqual(response.status_code, 400)

        #test_case: user with the same email address already exists
        User.objects.create_user(username='john@adams.com', email='john@adams.com', password='smith')
        response = c.post('/signup/',{'first_name': 'mehmet', 'last_name': 'keser',
                                      'password': 'ahmet', 'email': 'john@adams.com'})
        self.assertEqual(response.status_code, 400)

    def test_signup_view_succeeds(self):
        c = Client()

        response = c.post('/signup/',{'first_name': 'ahmet', 'last_name': 'keser',
                                      'password': 'ahmet', 'email': 'john@adams.com'})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard'))
