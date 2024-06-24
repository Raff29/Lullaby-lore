from django.urls import path
from .views import StoryOfTheDay

urlpatterns = [
  path('story-of-the-day/', StoryOfTheDay.as_view(), name='story-of-the-day'),
]
