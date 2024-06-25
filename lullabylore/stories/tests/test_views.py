import random
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from unittest import mock


class StoryViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(
            username='admin', password='adminpassword', email='admin@example.com'
        )
        self.client.login(username='admin', password='adminpassword')

    @mock.patch('stories.views.add_story')
    def test_add_story_view(self, mock_add_story):
        mock_add_story.return_value = 'None'

        response = self.client.post(
            reverse('add_story'),
            {
                'title': 'Test Story',
                'content': 'Test content',
                'author': 'Test Author',
                'age_group': 'Test Age Group',
                'date': '2021-01-01'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Story added successfully!'})

    @mock.patch('stories.views.get_all_stories')
    def test_get_stories_view(self, mock_get_all_stories):
    # Mock get_all_stories to return exactly two stories
      mock_get_all_stories.return_value = [
          {'title': 'Existing Story 1', 'content': 'This is an existing story 1.',
              'author': 'Existing Author 1', 'age_group': '3-5', 'date': '2021-01-01'},
          {'title': 'Existing Story 2', 'content': 'This is an existing story 2.',
              'author': 'Existing Author 2', 'age_group': '3-5', 'date': '2021-01-01'}
      ]

      response = self.client.get(reverse('get_stories'))
      self.assertEqual(response.status_code, 200)
      stories = response.json()
      self.assertIsInstance(stories, list)
      self.assertEqual(len(stories), 2)
      self.assertTrue(
          any(story['title'] == 'Existing Story 1' for story in stories))
      self.assertTrue(
          any(story['title'] == 'Existing Story 2' for story in stories))

    @mock.patch('stories.views.get_random_story')
    def test_get_random_story_view(self, mock_get_random_story):
      stories = [
        {'title': 'Random Story', 'content': 'This is a random test story.', 'author': 'Random Author', 'age_group': '3-5', 'date': '2021-01-01'},
        {'title': 'Random Story2', 'content': 'This is a random test story.2', 'author': 'Random Author', 'age_group': '3-5', 'date': '2021-01-01'}
    ]
      selected_story = random.choice(stories)
      
      mock_get_random_story.return_value = selected_story
      
      response = self.client.get(reverse('get_random_story'))
      
      self.assertEqual(response.status_code, 200)
      story = response.json()
      self.assertIsInstance(story, dict)
      self.assertIn(story['title'], ['Random Story', 'Random Story2']) 
      self.assertIn('content', story)
      self.assertIn('author', story)
      self.assertIn('age_group', story)
      self.assertIn('date', story)
      

    def tearDown(self):
        return self.client.logout()
