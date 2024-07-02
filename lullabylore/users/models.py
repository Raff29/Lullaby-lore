from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

class FavouriteStories(models.Model):
    story_id = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title or self.story_id


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favourite_stories = models.ManyToManyField(FavouriteStories, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        logger.info(f"User profile created for {instance.username}")


post_save.connect(create_user_profile, sender=User)
