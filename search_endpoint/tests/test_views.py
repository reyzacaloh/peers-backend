from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase, APIClient
from tutor_register.models import Tutor
from account.models import User

class TutorTest(APITestCase, URLPatternsTestCase):

    urlpatterns = [
        path("api/search_tutor/", include('search_endpoint.urls')),
    ]

    def setUp(self):
        self.user1 = User.objects.create(
            email='test1@test.com',
            password='test',
            role=User.LEARNER
        )
        self.user2 = User.objects.create(
            email='test2@test.com',
            password='test',
        )
        self.tutor1 = Tutor.objects.create(
            uid=self.user1,
            subject = 'Matematika',
            university = 'Universitas 1',
            is_accepted = True
        )
        self.tutor2 = Tutor.objects.create(
            uid=self.user2,
            subject = 'Fisika',
            university = 'Universitas 2',
            is_accepted = True
        )
        self.client = APIClient()

    def test_search_all_tutor(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['tutors']),2)

    def test_search_specific_tutor_by_subject(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('search') + "?sub=Matematika"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['tutors']),1)

    def test_search_specific_tutor_by_user_id(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('search') + "?id=1"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['tutors']),1)
    
    def test_search_specific_tutor_by_user_id_not_found(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('search') + "?id=9"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Tutor tidak ditemukan')

    def test_no_tutor_found(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('search') + "?sub=Biologi"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['tutors'], [])

    def test_request_is_unauthenticated(self):
        url = reverse('search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
