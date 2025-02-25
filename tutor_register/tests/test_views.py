from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import include, path, reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase, APIClient
from django.test import TestCase

from account.models import User

from ..models import Tutor
from schedule.models import Schedule
from ..serializers import TutorSerializer


class TutorTest(APITestCase, URLPatternsTestCase):

    urlpatterns = [
        path('api/tutor_form/', include('tutor_register.urls')),
    ]

    def setUp(self):
        self.user = User.objects.create(
            email='test1@test.com',
            password='test',
            role=User.LEARNER
        )
        self.url = reverse('upload')
        self.data = {
            "subject": "Matematika",
            "university": "Universitas Indonesia",
            "pddikti": "https://pddikti.kemdikbud.go.id/data_mahasiswa/abcdef",
            "ktp": SimpleUploadedFile('test_ktm.pdf', b'abcdef', content_type='application/pdf'),
            "transkrip": SimpleUploadedFile('test_transkrip.pdf', b'abcdef', content_type='application/pdf'),
            "ktm_person": SimpleUploadedFile('test_ktm_person.jpg', b'abcdef', content_type='image/jpg'),
            "price_per_hour": 50000,
            "desc": "hello i'm a tutor",
        }

    def test_user_upload(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_unauthenticated(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TutorVerifyAPITest(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            email='test2@test.com',
            password='test',
            role=User.ADMIN
        )
        self.client.force_authenticate(user=self.admin)

        self.user = User.objects.create(
            email='test1@test.com',
            password='test',
            role=User.ADMIN
        )
        self.url = reverse('verify')
        self.tutor = Tutor.objects.create(
            uid=self.user,
            subject="Matematika",
            university="Universitas Indonesia",
            pddikti="https://pddikti.kemdikbud.go.id/data_mahasiswa/abcdef",
            ktp=SimpleUploadedFile('test_ktm.pdf', b'abcdef', content_type='application/pdf'),
            transkrip=SimpleUploadedFile('test_transkrip.pdf', b'abcdef', content_type='application/pdf'),
            ktm_person=SimpleUploadedFile('test_ktm_person.jpg', b'abcdef', content_type='image/jpg')
        )

    def test_get_applicants(self):
        # arrange
        url = reverse('verify')
        response = self.client.get(url)

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], True)

    def test_patch_applicant(self):
        # arrange
        url = reverse('verify')
        data = {
            "pddikti": "https://pddikti.kemdikbud.go.id/data_mahasiswa/abcdef",
            'subject': 'math',
            'is_accepted': 'true'
        }
        response = self.client.patch(url, data=data)

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['subject'], 'math')

    def test_fail_patch_applicant(self):
        # arrange
        url = reverse('verify')
        data = {
            "pddikti": "https://pddikti.kemdikbud.go.id/data_mahasiswa/abcdef",
            "email": "a",
            "transkrip": "a"
        }
        response = self.client.patch(url, data=data)

        # assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TutorDetailsViewTestCase(APITestCase):
    def setUp(self):
        self.user = baker.make(User)
        self.tutor = baker.make(Tutor, uid=self.user)

    def test_get_tutor_details(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('tutor_details')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_response = {
            'success': True,
            'statusCode': status.HTTP_200_OK,
            'message': 'Tutor data fetched',
            'tutor': TutorSerializer(self.tutor).data
        }
        self.assertEqual(response.data, expected_response)

    def test_get_tutor_details_unauthorized(self):
        url = reverse('tutor_details')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_tutor(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('tutor_details')
        uid = self.tutor.uid.uid
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_response = {
            'success': True,
            'statusCode': status.HTTP_200_OK,
            'message': 'tutor uid={uid} has been deleted'.format(uid=uid),
        }
        self.assertEqual(response.data, expected_response)


    def test_delete_tutor_details_unauthorized(self):
        url = reverse('tutor_details')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class TutorRatingViewTestCase(APITestCase):

    def setUp(self):
        self.user = baker.make(User)
        self.tutor = baker.make(Tutor, uid=self.user)
        self. schedule = baker.make(Schedule, tutor_id=self.tutor)
        self.url = reverse('rate_tutor')
        self.data = {
            "rating": 5,
            "tutor_id": self.tutor.id,
            "schedule_id": self.schedule.id
        }

    def test_rate_tutor(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_unauthenticated(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unexpected_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, {"tutor_id": self.tutor.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TutorPriceUpdateTestCase(APITestCase):

    def setUp(self):
        self.user = baker.make(User)
        self.tutor = baker.make(Tutor, uid=self.user)
        self.url = reverse('price_update')
        self.data = {
            "new_price": 69420,
        }

    def test_rate_tutor(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_unauthenticated(self):
        response = self.client.patch(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unexpected_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.url, {"price": 10000})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
