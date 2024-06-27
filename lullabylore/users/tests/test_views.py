from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class RegisterViewTests(APITestCase):
    def test_register_user(self):
        response = self.client.post(
            reverse('register'),
            {
                'username': 'testuser',
                'password': 'testpassword',
                'email': 'test@test.com'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

    def test_register_user_invalid_data(self):
        response = self.client.post(
            reverse('register'),
            {
                'username': 'testuser',
                'password': 'testpassword',
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)


class LoginViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', email='test@test.com', password='testpassword')

    def test_login_user(self):
        response = self.client.post(
            reverse('login'),
            {
                'username': 'testuser',
                'password': 'testpassword',
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response.data)
        self.assertIn('token', response.data)

    def test_login_user_invalid_credentials(self):
        response = self.client.post(
            reverse('login'),
            {
                'username': 'testuser',
                'password': 'wrongpassword',
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('user', response.data)
        self.assertNotIn('token', response.data)

    def tearDown(self) -> None:
        return super().tearDown()


class LogoutViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@test.com',
                                             password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_logout_user(self):
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
