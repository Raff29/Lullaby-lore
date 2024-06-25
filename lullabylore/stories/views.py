from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from .firestore_service import add_story, get_all_stories, get_random_story


def is_admin(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(is_admin)
def add_story_view(request):
  if request.method == 'POST':
    data = request.POST
    title = data.get('title')
    content = data.get('content')
    author = data.get('author')
    age_group = data.get('age_group')
    date = data.get('date')

    add_story(title, content, author, age_group, date)
    return JsonResponse({'message': 'Story added successfully!'})

  return JsonResponse({'message': 'Only admins can add stories!'}, status=403)


def get_stories_view(request):
  stories = get_all_stories()
  return JsonResponse(stories, safe=False)

def get_random_story_view(request):
  random_story = get_random_story()
  return JsonResponse(random_story, safe=False)