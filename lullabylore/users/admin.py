from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserProfile, FavouriteStories


class userProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_favourite_stories')
    search_fields = ('user__username',)

    def get_favourite_stories(self, obj):
        return ", ".join([fav.title for fav in obj.favourite_stories.all()])
    get_favourite_stories.short_description = 'Favourite Stories'


class FavouriteStoriesAdmin(admin.ModelAdmin):
    list_display = ('story_id', 'title', 'created_at')
    search_fields = ('story_id', 'title')
    
admin.site.register(FavouriteStories, FavouriteStoriesAdmin)
admin.site.register(UserProfile, userProfileAdmin)
