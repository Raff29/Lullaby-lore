from users.models import FavouriteStories
from .firebase_init import db
import random


def add_story(title, content, author, age_group, date):
    doc_ref = db.collection("stories").document()
    doc_ref.set({
        "title": title,
        "content": content,
        "author": author,
        "age_group": age_group,
        "date": date
    })


def add_favourite_story(user_profile, story_id, title):
    if not story_id:
        raise ValueError("story_id must be provided and not empty")
    
    favourite_story, created = FavouriteStories.objects.get_or_create(
        story_id=story_id,
        defaults={'title': title}
    )

    if not user_profile.favourite_stories.filter(story_id=story_id).exists():
        user_profile.favourite_stories.add(favourite_story)
        return True


def get_random_story():
    stories = get_all_stories()
    if stories:
        return random.choice(stories)
    return None


def get_all_stories():
    stories_ref = db.collection("stories")
    docs = stories_ref.stream()
    all_stories = [{'id': docs.id, **docs.to_dict()} for docs in docs]
    return all_stories


def update_story(story_id, updates):
    story_ref = db.collection("stories").document(story_id)
    story_ref.update(updates)


def delete_story(story_id):
    story_ref = db.collection("stories").document(story_id)
    story_ref.delete()
