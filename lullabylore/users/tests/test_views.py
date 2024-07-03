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

    def tearDown(self) -> None:
        return super().tearDown()


class AddFavouriteStoryViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@test.com',
                                             password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_add_favourite_story(self):
        response = self.client.post(
            reverse('favourite-stories'),
            {
                'id': 1,
                'title': 'Test Story'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data, {'message': 'Story added to favourites'})

    def test_add_existing_favourite_story(self):
        response = self.client.post(
            reverse('favourite-stories'),
            {
                'id': 1,
                'title': 'Test Story'
            }
        )

        response = self.client.post(
            reverse('favourite-stories'),
            {
                'id': 1,
                'title': 'Test Story'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data, {'message': 'Story already exists in favourites!'})

    def tearDown(self):
        return super().tearDown()


class GetFavouriteStoriesViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@test.com',
                                             password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_get_favourite_story(self):

        self.client.post(
            reverse('favourite-stories'),
            {
                'id': 1,
                'title': 'Test Story'
            }
        )
        response = self.client.get(reverse('my-favourite-stories'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        favourite_stories = response.json()
        self.assertIsInstance(favourite_stories, list)
        self.assertEqual(len(favourite_stories), 1)

    def test_get_favourite_stories(self):

        self.client.post(
            reverse('favourite-stories'),
            {
                'id': 1,
                'title': 'Test Story'
            },
        )
        self.client.post(
            reverse('favourite-stories'),
            {
                'id': 2,
                'title': 'Test Story2'
            },
        )
        response = self.client.get(reverse('my-favourite-stories'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        favourite_stories = response.json()
        self.assertIsInstance(favourite_stories, list)
        self.assertEqual(len(favourite_stories), 2)

    def test_get_no_favourite_story(self):
        response = self.client.get(reverse('my-favourite-stories'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        favourite_stories = response.json()
        self.assertIsInstance(favourite_stories, list)
        self.assertEqual(len(favourite_stories), 0)

    def tearDown(self):
        return super().tearDown()


class DeleteFavouriteStoryViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@test.com',
                                             password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_delete_favourite_story(self):
        self.client.post(
            reverse('favourite-stories'),
            {
                'id': 1,
                'title': 'Test Story'
            },
        )

        response = self.client.delete(
            reverse('delete-favourite-story',  args=[1]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        favourite_stories_id = self.user.userprofile.favourite_stories.all(
        ).values_list('id', flat=True)
        self.assertNotIn(1, favourite_stories_id)

    def tearDown(self):
        return super().tearDown()
