from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import user_passes_test
from .firestore_service import add_story, get_all_stories, get_random_story, update_story, delete_story


def is_admin(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(is_admin)
@require_http_methods(["POST"])
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

@require_http_methods(["GET"])
def get_stories_view(request):
  stories = get_all_stories()
  return JsonResponse(stories, safe=False)

@require_http_methods(["GET"])
def get_random_story_view(request):
  random_story = get_random_story()
  return JsonResponse(random_story, safe=False)

@require_http_methods(["PATCH"])
@user_passes_test(is_admin)
def update_story_view(request, story_id):
  if request.method == 'PATCH':
    data = request.POST
    updates = {
      'title': data.get('title'),
      'content': data.get('content'),
      'author': data.get('author'),
      'age_group': data.get('age_group'),
      'date': data.get('date')
    }
    update_story(story_id, updates)
    return JsonResponse({'message': 'Story updated successfully!'})

  return JsonResponse({'message': 'Only admins can update stories!'}, status=403)

@require_http_methods(["DELETE"])
@user_passes_test(is_admin)
def delete_story_view(request, story_id):
  if request.method == 'DELETE':
    delete_story(story_id)
    return JsonResponse({'message': 'Story deleted successfully!'})
  
  return JsonResponse({'message': 'Only admins can delete stories!'}, status=403)
    
  
