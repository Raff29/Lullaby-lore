from django.test import TestCase
from ..firestore_service import add_story, get_all_stories

class StoryServicesTests(TestCase):
  def test_add_story(self):
    add_story('Test Story', 'Test content', 'Test Author', 'Test Age Group', '2021-01-01')
    stories = get_all_stories()
    self.assertTrue(any(story['title'] == 'Test Story' for story in stories))
    
  def test_get_all_stories(self):
    stories = get_all_stories()
    self.assertIsInstance(stories, list)

