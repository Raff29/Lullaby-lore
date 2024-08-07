from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from stories.firestore_service import add_favourite_story, delete_favourite_story
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .models import UserProfile


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def register_view(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        return Response({"message": "This is the registration page. Please POST your registration details."}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def login_view(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "user": UserSerializer(user).data,
                "token": token.key
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        return Response({"message": "This is the login page. Please POST your login details."}, status=status.HTTP_200_OK)


@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_favourite_story_view(request):
    user = request.user
    if not hasattr(user, 'userprofile'):
        user_profile = UserProfile.objects.create(user=user)
    else:
        user_profile = user.userprofile
        
    story_id = request.data.get('id')
    title = request.data.get('title')

    if add_favourite_story(user_profile, story_id, title):
        return Response({'message': 'Story added to favourites'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'message': 'Story already exists in favourites!'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_favourite_stories_view(request):
    user = request.user.userprofile
    favourite_stories = list(user.favourite_stories.all().values())
    return JsonResponse(favourite_stories, safe=False)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_favourite_story_view(request, story_id):
    user = request.user.userprofile
    delete_favourite_story(user,story_id)
    return Response(status=status.HTTP_204_NO_CONTENT)
    
    