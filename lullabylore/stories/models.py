from django.db import models

class Story(models.Model):
  title = models.CharField(max_length=200)
  content = models.TextField()
  date = models.DateTimeField(unique=True)
  
  def __str__(self):
    return self.title
