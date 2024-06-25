from django.urls import path
from . import views

urlpatterns = [
    path('add-story/', views.add_story_view, name='add_story'),
    path('get-stories/', views.get_stories_view, name='get_stories'),
    path('get-random-story/', views.get_random_story_view, name='get_random_story')
]
