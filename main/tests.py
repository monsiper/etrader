from django.contrib.auth.models import User, AnonymousUser
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test import Client
# Create your tests here.

class TestMain(TestCase):

    def test_main_page(self):
        c= Client()
        #test case: anonymous user
        response = c.get(reverse('main_page'))
        self.assertEqual(response.status_code, 200)

        #test_case: authenticated user
        User.objects.create_user(username='john@adams.com', email='john@adams.com', password='smith')
        c.post(reverse('login'), {'email': 'john@adams.com', 'password': 'smith'})
        response = c.get(reverse('main_page'))
        self.assertEqual(response.status_code, 302)


    def test_user_panel(self):
        c= Client()
        #test case: anonymous user
        response = c.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 403)

        #test case: a user that has logged in wants to go to user_panel
        User.objects.create_user(username='john@adams.com', email='john@adams.com', password='smith')
        c.post(reverse('login'), {'email': 'john@adams.com', 'password': 'smith'})
        response = c.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
