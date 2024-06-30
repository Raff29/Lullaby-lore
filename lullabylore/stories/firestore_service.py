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
    favourite_story, created = FavouriteStories.objects.get_or_create(
        firebase_story_id=story_id,
        defaults={'title': title}
    )

    if not user_profile.favourite_stories.filter(firebase_story_id=story_id).exists():
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

    stories = []
    for doc in docs:
        stories.append(doc.to_dict())
    return stories


def update_story(story_id, updates):
    story_ref = db.collection("stories").document(story_id)
    story_ref.update(updates)


def delete_story(story_id):
    story_ref = db.collection("stories").document(story_id)
    story_ref.delete()
