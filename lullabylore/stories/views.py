from django.shortcuts import render
from django.utils import timezone
from .models import Story
from rest_framework import generics
from .serializers import StorySerializer

class StoryOfTheDay(generics.RetrieveAPIview):
  serializer_class = StorySerializer
  
  def get_object(self):
    today = timezone.now().date()
    return Story.objects.filter(date=today).first()


