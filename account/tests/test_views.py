from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from model_bakery import baker
import json

from ..models import User
from ..serializers import UserSerializer

# Create your tests here.
class UserTest(APITestCase, URLPatternsTestCase):
    """ Test module for User """

    urlpatterns = [
        path('api/auth/', include('account.urls')),
    ]

    def setUp(self):
        self.user1 = User.objects.create_user(
            email='test1@test.com',
            password='test',
        )

        self.admin = User.objects.create_superuser(
            email='admin@test.com',
            password='admin',
        )

    def test_user_registration(self):
        """ Test if a user can register """
        url = reverse('register')
        data = {
            'email': 'test2@test.com',
            'password': 'test',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class PeersJWTTokenTest(TestCase):

    def setUp(self):
        self.email='test1@test.com'
        self.password='test'
        self.user1 = User.objects.create_user(
            email=self.email,
            password=self.password,
        )

    def test_obtain_jwt_token(self):
        url = reverse('token_create')
        data = {'email': self.email, 'password': self.password}
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'access')
        self.assertContains(response, 'refresh')
    
    def test_obtain_jwt_token_invalid_password(self):
        url = reverse('token_create')
        data = {'email': self.email, 'password': 'self.password'}
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 401)

class UserManagementViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = baker.make(User)
    
    def tearDown(self):
        self.client = None
        self.user = None

    def test_get_user(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('user_profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], True)
        self.assertEqual(response.data['statusCode'], status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'User data fetched')

        expected_user_data = UserSerializer(self.user).data
        self.assertEqual(response.data['user'], expected_user_data)
    
    def test_get_user_unauthenticated(self):
        url = reverse('user_profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()['detail'], 'Authentication credentials were not provided.')