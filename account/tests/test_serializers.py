from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from ..models import User
from ..serializers import AuthUserRegistrationSerializer, UserSerializer


class AuthUserRegistrationSerializerTests(TestCase):
    def setUp(self):
        self.validated_data = {
            'email': 'test@example.com',
            'uid':'ab812671-86c8-487d-ab5b-8d25af5bf7e5',
            'password': 'testpassword',
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '2000-01-01',
        }
        self.file = SimpleUploadedFile('test.jpg', b'test image content', content_type='image/jpeg')
        self.serializer = AuthUserRegistrationSerializer()

    def test_serializer_valid(self):
        # Test that serializer is valid with valid data
        serializer = AuthUserRegistrationSerializer(data=self.validated_data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_invalid_email(self):
        # Test that serializer is invalid with invalid email
        data = self.validated_data.copy()
        data['email'] = 'invalid-email'
        serializer = AuthUserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_create(self):
        # Test that serializer creates a new user object with valid data
        serializer = AuthUserRegistrationSerializer(data=self.validated_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertIsInstance(user, User)

class UserSerializerTests(TestCase):
    def test_valid_data(self):
        data = {
            'email': 'admin@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'role': User.ADMIN
        }

        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()

        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.first_name, data['first_name'])
        self.assertEqual(user.last_name, data['last_name'])
        self.assertEqual(user.role, data['role'])

    def test_missing_required_fields(self):
        data = {}
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())