from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
from django.contrib.auth.models import User
from django.contrib.auth import logout

class RegisterView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = RegisterSerializer
  permission_classes = [AllowAny]
  
class LoginView(generics.CreateAPIView):
  serializer_class = LoginSerializer
  permission_classes = [AllowAny]
  
  def post(self,request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data
    token, created = Token.objects.get_or_create(user=user)
    return Response({
      "user": UserSerializer(user).data,
      "token": token.key
    })
    
class LogoutView(generics.CreateAPIView):
  def post(self, request):
    logout(request)
    #TODO redirect to index page
    return Response(status=204)
  
  
