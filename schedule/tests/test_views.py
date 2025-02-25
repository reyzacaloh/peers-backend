import datetime
from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase, APIClient
from ..models import Schedule
from tutor_register.models import Tutor
from account.models import User



class TutorTest(APITestCase, URLPatternsTestCase):

    urlpatterns = [
        path("api/schedule/", include('schedule.urls')),
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
            role=User.TUTOR
        )
        self.tutor = Tutor.objects.create(
            uid=self.user2,
            subject = 'Matematika',
            university = 'Universitas 1'
        )
        self.schedule1 = Schedule.objects.create(
            tutor_id=self.tutor,
            learner_id=None,
            date_time=datetime.datetime(2024, 10, 9, 22, 55, 59, 0)
        )
        self.schedule2 = Schedule.objects.create(
            tutor_id=self.tutor,
            learner_id=self.user1,
            date_time=datetime.datetime(2024, 10, 9, 22, 55, 59, 0)
        )
        self.data = "date_time=2023-04-23T20:00:00.0Z"

    def test_post_schedule(self):
        self.client.force_authenticate(user=self.user2)
        url = reverse('schedule')
        response = self.client.post(url,self.data,content_type='application/x-www-form-urlencoded')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Schedule.objects.get(pk=3).tutor_id,self.tutor)

    def test_post_failed_because_query_paramas(self):
        self.client.force_authenticate(user=self.user2)
        url = reverse('schedule') + "?id=1"
        response = self.client.post(url,self.data,content_type='application/x-www-form-urlencoded')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], "invalid query params for post")
        self.assertEqual(Schedule.objects.filter(pk=3).first(),None)

    def test_post_failed_data_wrong(self):
        self.client.force_authenticate(user=self.user2)
        url = reverse('schedule') + "?id=1"
        response = self.client.post(url,{},content_type='application/x-www-form-urlencoded')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Schedule.objects.filter(pk=3).first(),None)
    
    def test_get_schedule_tutor(self):
        self.client.force_authenticate(user=self.user2)
        url = reverse('schedule') + "?tutor=1"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['schedules']),2)

    def test_get_schedule_learner(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('schedule') + "?tutor=0"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['schedules']),1)
    
    def test_get_schedule_tutor_not_exist(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('schedule') + "?tutor=1"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_schedule_tutor_failed_because_no_query_params(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('schedule')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], "invalid query params for get")

    def test_get_schedule_tutor_failed_because_wrong_query_params(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('schedule') + "?tid=1"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], "invalid query params for get")

    def test_delete_schedule(self):
        self.client.force_authenticate(user=self.user2)
        url = reverse('schedule') + "?sid=1"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Schedule.DoesNotExist):
            Schedule.objects.get(pk=1)

    def test_delete_schedule_not_exist(self):
        self.client.force_authenticate(user=self.user2)
        url = reverse('schedule') + "?sid=6"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_failed_because_query_paramas(self):
        self.client.force_authenticate(user=self.user2)
        url = reverse('schedule')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], "invalid query params for delete")
        self.assertEqual(Schedule.objects.filter(pk=3).first(),None)
