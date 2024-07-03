from django.test import TestCase
from unittest import mock
from ..firestore_service import get_all_stories, add_story, get_random_story, update_story, delete_story


class StoryServiceTests(TestCase):
    @mock.patch('stories.firestore_service.db.collection')
    def test_add_story_service(self, mock_db_collection):
        mock_doc_ref = mock.Mock()
        mock_db_collection.return_value.document.return_value = mock_doc_ref

        add_story('Service Test Story', 'This is a service test story.',
                  'Service Author', '3-5', '2021-01-01')

        mock_db_collection.assert_called_once_with('stories')
        mock_doc_ref.set.assert_called_once_with({
            'title': 'Service Test Story',
            'content': 'This is a service test story.',
            'author': 'Service Author',
            'age_group': '3-5',
            'date': '2021-01-01',
        })

    @mock.patch('stories.firestore_service.db.collection')
    def test_get_all_stories_service(self, mock_db_collection):
        mock_doc1 = mock.Mock()
        mock_doc1.to_dict.return_value = {
            'title': 'Random Story',
            'content': 'This is a random test story.',
            'author': 'Random Author',
            'age_group': '3-5',
            'date': mock.ANY,
        }

        mock_doc2 = mock.Mock()
        mock_doc2.to_dict.return_value = {
            'title': 'Random Story 2',
            'content': 'This is a random test story 2.',
            'author': 'Random Author 2',
            'age_group': '3-5',
            'date': mock.ANY,
        }

        mock_db_collection.return_value.stream.return_value = [
            mock_doc1, mock_doc2]

        stories = get_all_stories()
        self.assertIsInstance(stories, list)
        self.assertEqual(len(stories), 2)
        self.assertEqual(stories[0]['title'], 'Random Story')
        self.assertEqual(stories[1]['title'], 'Random Story 2')


@mock.patch('stories.firestore_service.db.collection')
def test_get_random_story_service(self, mock_get_all_stories):
    mock_get_all_stories.return_value = [
        {'title': 'Random Story', 'content': 'This is a random test story.',
            'author': 'Random Author', 'age_group': '3-5', 'date': mock.ANY},
        {'title': 'Random Story 2', 'content': 'This is a random test story 2.',
            'author': 'Random Author 2', 'age_group': '3-5', 'date': mock.ANY}
    ]

    story = get_random_story()
    self.assertIsInstance(story, dict)
    self.assertIn('title', story)
    self.assertIn(story['title'], ['Random Story', 'Random Story 2'])
    self.assertIn('content', story)
    self.assertIn('author', story)
    self.assertIn('age_group', story)


@mock.patch('stories.firestore_service.db.collection')
def test_update_story_service(mock_db_collection):
    mock_story_ref = mock.Mock()
    mock_db_collection.return_value.document.return_value = mock_story_ref

    update_story('story_id', {'title': 'Updated Story', 'content': 'This is an updated story.',
                 'author': 'Updated Author', 'age_group': '3-5', 'date': '2021-01-01'})

    mock_db_collection.assert_called_once_with('stories')
    mock_db_collection.return_value.document.assert_called_once_with(
        'story_id')
    mock_story_ref.update.assert_called_once_with({
        'title': 'Updated Story',
        'content': 'This is an updated story.',
        'author': 'Updated Author',
        'age_group': '3-5',
        'date': '2021-01-01',
    })


@mock.patch('stories.firestore_service.db.collection')
def test_delete_story_service(self, mock_get_all_stories, mock_db_collection):
    existing_stories_before_deletion = [
        {'story_id': '1', 'title': 'Story 1'},
        {'story_id': '2', 'title': 'Story to be deleted'},
        {'story_id': '3', 'title': 'Story 2'},
    ]

    mock_get_all_stories.return_value = existing_stories_before_deletion

    delete_story('2')

    updated_stories_after_deletion = [
        story for story in existing_stories_before_deletion if story['story_id'] != '2'
    ]

    mock_get_all_stories.return_value = updated_stories_after_deletion

    stories = get_all_stories()

    self.assertNotIn(
        {'story_id': '2', 'title': 'Story to be deleted'}, stories)

#TODO: Add test for add_favourite_story, get_favourite_stories, delete_favourite_story