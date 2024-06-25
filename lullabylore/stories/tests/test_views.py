from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class StoryViewTests(TestCase):
  def setUp(self):
    self.client = Client()
    self.admin = User.objects.create_superuser(
      username='admin', password='adminpassword', email='admin@example.com'
    )
    self.client.login(username='admin', password='adminpassword')
    
  def test_add_story_view(self):
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
    
  def test_get_stories_view(self):
    response = self.client.get(reverse('get_stories'))
    self.assertEqual(response.status_code, 200)
    stories = response.json()
    self.assertIsInstance(stories, list)
    
  def tearDown(self):
    return self.client.logout()
    