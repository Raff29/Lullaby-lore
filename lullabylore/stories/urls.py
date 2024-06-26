from django.urls import path
from . import views

urlpatterns = [
    path('add-story/', views.add_story_view, name='add_story'),
    path('get-stories/', views.get_stories_view, name='get_stories'),
    path('get-random-story/', views.get_random_story_view, name='get_random_story'),
    path('story/update/<str:story_id>/', views.update_story_view, name='update_story'),
    path('story/delete/<str:story_id>/', views.delete_story_view, name='delete_story'),
]
