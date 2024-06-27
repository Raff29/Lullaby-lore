from rest_framework.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth.models import User
from ..serializers import RegisterSerializer, LoginSerializer

class RegisterSerializerTest(TestCase):
  def setUp(self):
    self.user_data = {
      'username': 'testuser',
      'email': 'test@example.com',
      'password': 'testpassword123'
    }
    self.serializer_data = {
      'username': 'newuser',
      'email': 'newuser@example.com',
      'password': 'newpassword123'
    }

  def test_create_user(self):
    serializer = RegisterSerializer(data=self.serializer_data)
    self.assertTrue(serializer.is_valid())
    user = serializer.save()
    self.assertIsInstance(user, User)
    self.assertEqual(user.username, self.serializer_data['username'])
    self.assertEqual(user.email, self.serializer_data['email'])
    # Ensure password is set correctly but not returned
    self.assertTrue(user.check_password(self.serializer_data['password']))
    self.assertNotIn('password', serializer.data)

  def test_required_fields(self):
    incomplete_data = self.serializer_data.copy()
    incomplete_data.pop('username')
    serializer = RegisterSerializer(data=incomplete_data)
    self.assertFalse(serializer.is_valid())
    self.assertIn('username', serializer.errors)

  def test_unique_username_and_email(self):
    # Create an existing user
    User.objects.create_user(**self.user_data)
    # Attempt to create a new user with the same username and email
    serializer = RegisterSerializer(data=self.user_data)
    self.assertFalse(serializer.is_valid())
    self.assertIn('username', serializer.errors)
    self.assertIn('email', serializer.errors)
    
  def tearDown(self) -> None:
    return super().tearDown()
    
class LoginSerializerTest(TestCase):
  def setUp(self):
    self.user_active = User.objects.create_user(email='test@user.com',username='activeUser', password='12345', is_active=True)
    
    self.user_inactive = User.objects.create_user(
      email='inactiveTest@user.com', username='inactiveUser', password='54321', is_active=False)
    
  def test_valid_login(self):
    serializer = LoginSerializer(data={'username': 'activeUser', 'password' : '12345'})
    self.assertTrue(serializer.is_valid())
    user = serializer.validated_data
    self.assertEqual(user, self.user_active)
    self.assertTrue(user.is_active)
  
  def test_inactive_user_login(self):
    serializer = LoginSerializer(data={
      'username': 'inactiveUser',
      'password': '54321'
    })
    with self.assertRaises(ValidationError):
      serializer.is_valid(raise_exception=True)
      serializer.validated_data({'username': 'inactiveUser', 'password': '54321'})                           
    
  def test_invalid_login(self):
    serializer = LoginSerializer(data={
      'username': 'activeUser',
      'password': 'wrongpassword'
    })
    with self.assertRaises(ValidationError):
      serializer.is_valid(raise_exception=True)      
      serializer.validated_data({'username': 'activeUser', 'password': 'wrongpassword'})
      
  def tearDown(self) -> None:
    return super().tearDown()
