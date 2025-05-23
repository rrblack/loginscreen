from http.client import responses

from django.template.context_processors import request
from django.test import TestCase, Client
from django.urls import reverse

from .models import MyUserManager, User


# 単位テスト
class TestModels(TestCase):
    def setUp(self):
        #startup
        self.client = Client()
        self.user = User.objects.create_user(email='testuser@gmail.com', password='password', name='testman')

        #urls
        self.top_page_url = reverse('top_page')
        self.login_url = reverse('user_login')
        self.sign_up_url = reverse('sign_up')
        self.mail_check_url = reverse('mail_check')
        self.mail_verification_url = reverse('mail_verification')
        self.custom_logout_url = reverse('custom_logout')

    def test_top_page_GET(self):
        self.client.login(email = 'testuser@gmail.com', password = 'password')
        response = self.client.get(self.top_page_url)
        print(response)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/top_page.html')

    def test_top_page_GET_not_logged_in(self):
        response = self.client.get(self.top_page_url)
        print(response)
        self.assertEqual(response.status_code, 302)

    def test_login_GET(self):
        response = self.client.get(self.login_url)
        print(response)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login_POST(self):
        response = self.client.post(self.login_url)
        print(response)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login_POST_valid_credentials(self):
        response = self.client.post(self.login_url, {'email':'testuser@gmail.com','password':'password'})
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('top_page'))

    def test_login_POST_invalid_credentials(self):
        response = self.client.post(self.login_url,{'email':'testuser@gmail.com','password':'pasword'} )
        print(response)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login_POST_invalid_form(self):
        response = self.client.post(self.login_url, {'email': 'teasda123131', 'password': '13131@#!#!@#'})
        print(response)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')


    def test_login_POST_logged_in(self):
        self.client.login(email = 'testuser@gmail.com', password = 'password')
        response = self.client.post(self.top_page_url)
        print(response)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/top_page.html')


    def test_signup_POST(self):
        response = self.client.post(self.sign_up_url)
        print(response)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/sign_up.html')

    def test_mail_check_GET(self):
        response = self.client.get(self.mail_check_url)
        print(response)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('sign_up'))

    def test_mail_check_POST(self):
        User.objects.all().delete()
        response = self.client.post(self.mail_check_url, {'name':'testerr', 'email':'testerr@gmail.com', 'password':'imatester'})

        print(response)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('mail_verification'))

    def test_mail_check_POST_already_registered_user(self):
        response = self.client.post(self.mail_check_url,
                                    {'name': 'billy', 'email': 'testuser@gmail.com', 'password': 'password'},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Email already registered")


    def test_mail_check_POST_invalid_form(self):
        response = self.client.post(self.mail_check_url,
                                    {'name': 'testerr', 'email': 'testuser@gmail.com', 'password': 'imatester', 'random': 'thisis'})
        print(response)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('sign_up'))

    def test_mail_check_POST_invalid_form_missing_data(self):
        response = self.client.post(self.mail_check_url,
                                    {'email': 'testuser@gmail.com', 'password': 'imatester', 'random': 'thisis'})
        print(response)
        self.assertEqual(response.status_code, 302)
        #self.assertContains(response, "Error")
        self.assertRedirects(response, reverse('sign_up'))

    def test_mail_verification_GET(self):
        response = self.client.get(self.mail_verification_url)
        print(response)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,reverse('sign_up'))

    def test_mail_verification_POST(self):
        response = self.client.post(self.mail_verification_url, follow=True)
        print(response)
        print(response.redirect_chain)
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Registration session expired or invalid.")

    def test_custom_logout_GET(self):
        response = self.client.get(self.custom_logout_url)
        print(response)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))


#総合テスト
class Registration(TestCase):

    def setUp(self):
        self.session_data={
            'pending_user': {
                    'name': 'Test',
                    'email': 'test@test.com',
                    'password': 'password'
        },
            'verification_code': '123456'
        }
        print(self.session_data)
        self.top_page_url = reverse('top_page')
        self.login_url = reverse('user_login')
        self.sign_up_url = reverse('sign_up')
        self.mail_check_url = reverse('mail_check')
        self.mail_verification_url = reverse('mail_verification')
        self.custom_logout_url = reverse('custom_logout')

    def set_session(self):
        request = self.client.get(self.mail_verification_url)
        session = self.client.session
        for key, value in self.session_data.items():
            session[key] = value
        session.save()

    def test_mail_verification_post_success(self):
        self.set_session()
        response = self.client.post(self.mail_verification_url,{'code':'123456'}, follow=True)

        self.assertRedirects(response, reverse('top_page'))

        self.assertTrue(User.objects.filter(email="test@test.com").exists())

    def test_mail_verification_post_invalid_code(self):
        self.set_session()
        response = self.client.post(self.mail_verification_url,{'code':'123453'}, follow=True)
        self.assertRedirects(response, reverse('mail_verification'))

        self.assertFalse(User.objects.filter(email="test@test.com").exists())
        self.assertContains(response, "Invalid code")

    def test_mail_verification_post_missing_session_data(self):

        response = self.client.post(self.mail_verification_url,{'code':'123456'}, follow=True)
        self.assertRedirects(response, reverse('sign_up'))
        self.assertContains(response, "Registration session expired or invalid.")


