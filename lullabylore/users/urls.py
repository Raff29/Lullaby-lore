from django.urls import path
from .views import add_favourite_story_view, register_view, login_view, logout_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('favourite-stories/', add_favourite_story_view, name='favourite-stories')
]
