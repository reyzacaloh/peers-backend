from django.test import TestCase, Client
from django.urls import reverse
import json
from account.models import User
from tutor_register.models import Tutor
from schedule.models import Schedule
from ..models import Transaction
from model_bakery import baker
from ..views import create_snap_token
from django.conf import settings
from unittest import mock
from unittest.mock import patch
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from model_bakery.recipe import Recipe, foreign_key
from datetime import datetime
import uuid

class UpdateMidtransTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = baker.make(User)
        self.tutor = baker.make(Tutor)
        self.schedule = baker.make(Schedule)

        self.transaction = Transaction.objects.create(
            transaction_id='test-transaction-id', learner=self.user,
            tutor=self.tutor, schedule=self.schedule, status='pending', price=10.0)

    def test_get_update_from_midtrans(self):
        url = reverse('update-midtrans')
        data = {'order_id': 'test-transaction-id', 'transaction_status': 'settlement'}
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        transaction = Transaction.objects.get(transaction_id='test-transaction-id')
        self.assertEqual(transaction.status, 'COMPLETED')
        schedule = Schedule.objects.get(pk=self.schedule.pk)
        self.assertTrue(schedule.is_booked)

        data = {'order_id': 'test-transaction-id', 'transaction_status': 'deny'}
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        transaction = Transaction.objects.get(transaction_id='test-transaction-id')
        self.assertEqual(transaction.status, 'FAILED')
        schedule = Schedule.objects.get(pk=self.schedule.pk)
        self.assertFalse(schedule.is_booked)

        data = {'order_id': 'test-transaction-id', 'transaction_status': 'expired'}
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        transaction = Transaction.objects.get(transaction_id='test-transaction-id')
        self.assertEqual(transaction.status, 'EXPIRED')
        schedule = Schedule.objects.get(pk=self.schedule.pk)
        self.assertFalse(schedule.is_booked)


class TestCreateSnapToken(TestCase):

    @mock.patch('requests.post')
    def test_create_snap_token(self, mock_post):
        mock_post.return_value.ok = True
        mock_post.return_value.text = json.dumps({"token": "snap_token"})

        order_id = "order_id"
        gross_amount = 100000
        user = User.objects.create(email="test@gmail.com", first_name="test", last_name="test", password="test")
        tutor = Tutor.objects.create(uid=user, subject="math")
        snap_token = create_snap_token(order_id, gross_amount, user, tutor)

        self.assertEqual(snap_token, "snap_token")

        expected_payload = {
            "transaction_details": {
                "order_id": order_id,
                "gross_amount": gross_amount
            },
            "credit_card": {"secure": True},
            "customer_details": {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
            },
            "item_details": {
                "tutor_name": tutor.uid.first_name + " " + tutor.uid.last_name,
                "tutor_id": tutor.pk,
                "tutor_email": tutor.uid.email,
                "name": tutor.subject,
                "price": gross_amount,
                "quantity": 1
            },
            "custom_expiry": {
                "expiry_duration": 5,
                "unit": "minute"
            }
        }
        mock_post.assert_called_once_with(
            settings.MIDTRANS_URL,
            json=expected_payload,
            headers={
                "accept": "application/json",
                "content-type": "application/json",
                "authorization": "Basic " + settings.MIDTRANS_AUTH.decode('UTF-8')
            }
        )


# class MakeTransactionViewTest(APITestCase):

#     def setUp(self):
#         self.url = reverse("book")
#         self.client = APIClient()
#         self.user = Recipe(User)
#         self.tutor = Recipe(Tutor, uid=foreign_key(self.user))
#         self.schedule = baker.make(Schedule)
#         self.user = self.user.make()
#         self.tutor = self.tutor.make()
#         self.data = {
#             'tutor_id': self.user.pk,
#             'schedule_id': self.schedule.id,
#         }

#     def test_make_transaction_success(self):
#         self.client.force_authenticate(user=self.user)
#         self.request = self.client.post(self.url, data=json.dumps(self.data), content_type='application/json')
#         response = self.request
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         transaction = Transaction.objects.last()
#         self.assertEqual(transaction.tutor, self.tutor)
#         self.assertEqual(transaction.learner, self.user)
#         self.assertEqual(transaction.schedule, self.schedule)
#         self.assertEqual(transaction.price, self.tutor.price_per_hour)
#         self.assertEqual(transaction.status, 'PENDING')
#         self.assertIsNotNone(transaction.snap_token)
    
#     def test_make_transaction_fail_when_schedule_is_booked(self):
#         self.user = Recipe(User)
#         self.tutor = Recipe(Tutor, uid=foreign_key(self.user))
#         self.schedule = Recipe(Schedule, is_booked=True)
#         self.user = self.user.make()
#         self.tutor = self.tutor.make()
#         self.schedule = self.schedule.make()
#         self.data = {
#             'tutor_id': self.user.id,
#             'schedule_id': self.schedule.id,
#         }
#         self.client.force_authenticate(user=self.user)
#         self.request = self.client.post(self.url, data=json.dumps(self.data), content_type='application/json')
#         response = self.request
#         self.assertEqual(response.status_code, status.HTTP_417_EXPECTATION_FAILED)
#         self.assertEqual(response.json(), {"message": "Failed. Not Available"})

#     def test_make_transaction_auth_fail(self):
#         self.request = self.client.post(self.url, data=json.dumps(self.data), content_type='application/json')
#         response = self.request
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_make_transaction_snap_token_fail(self):
#         self.request = self.client.post(self.url, data=json.dumps(self.data), content_type='application/json')
#         response = self.request
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#         self.assertEqual(response.json(), {'detail': 'Authentication credentials were not provided.'})
#         self.assertFalse(Transaction.objects.exists())


class GetTutorBookedScheduleTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='testuser@test.com', password='testpass', role=User.TUTOR)
        self.tutor = Tutor.objects.create(uid=self.user, price_per_hour=20.0)
        self.schedule = Schedule.objects.create(date_time='2023-05-15 14:00:00')
        self.transaction = Transaction.objects.create(
            transaction_id='abc123',
            learner=self.user,
            tutor=self.tutor,
            schedule=self.schedule,
            price=20.0,
            status='PENDING',
            snap_token='snap_token'
        )

    def test_get_tutor_booked_schedule(self):
        url = reverse('booked-list')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['transactions']), 1)
        transaction = response.json()['transactions'][0]
        self.assertEqual(transaction['transaction_id'], 'abc123')
        self.assertEqual(transaction['schedule'], '2023-05-15T07:00:00Z')
        self.assertEqual(transaction['price'], 20.0)
        self.assertEqual(transaction['status'], 'PENDING')
        self.assertEqual(transaction['snap_token'], 'snap_token')
        self.assertEqual(transaction['learner_name'], self.user.first_name)


class GetLearnerUnpaidBookingTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpassword'
        )
        self.tutor = Tutor.objects.create(
            uid=self.user,
            subject='Maths',
            price_per_hour=50
        )
        self.schedule = Schedule.objects.create(
            tutor_id=self.tutor,
            date_time='2023-05-06 10:00:00',
            is_booked=False
        )
        self.transaction = Transaction.objects.create(
            transaction_id='1a2b3c',
            learner=self.user,
            tutor=self.tutor,
            schedule=self.schedule,
            price=50,
            status='PENDING',
            snap_token='snap_token_123'
        )

    def test_get_learner_unpaid_booking(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('booking-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['booking_list']), 1)
        self.assertEqual(response.json()['booking_list'][0]['transaction_id'], '1a2b3c')
        self.assertEqual(response.json()['booking_list'][0]['price'], 50)
        self.assertEqual(response.json()['booking_list'][0]['status'], 'PENDING')
        self.assertEqual(response.json()['booking_list'][0]['snap_token'], 'snap_token_123')
        self.assertEqual(response.json()['booking_list'][0]['tutor_name'], 'Test User')
        self.assertEqual(response.json()['booking_list'][0]['subject'], 'Maths')
        self.assertEqual(response.json()['booking_list'][0]['tutor_id'], self.tutor.pk)
        self.assertEqual(response.json()['booking_list'][0]['schedule_id'], self.schedule.pk)

class CancelBookingTest(APITestCase):
    def setUp(self):
        self.user = Recipe(User)
        self.tutor = Recipe(Tutor, uid=foreign_key(self.user))
        self.schedule = Recipe(Schedule,
            date_time=datetime.now(),
            tutor_id=foreign_key(self.tutor),
            is_booked=True
        )
        self.transaction = Recipe(Transaction,
            transaction_id=str(uuid.uuid4()),
            learner=foreign_key(self.user),
            tutor=foreign_key(self.tutor),
            schedule=foreign_key(self.schedule),
            price=self.tutor.make().price_per_hour,
            status='PENDING',
            snap_token='snap_token'
        )
        
   
    def test_cancel_booking_successfully(self):
        url = reverse('cancel-booking')
        self.schedule = Recipe(Schedule,
            date_time=datetime.now(),
            tutor_id=foreign_key(self.tutor),
            is_booked=False
        )
        self.user = self.user.make()
        self.tutor = self.tutor.make()
        self.schedule = self.schedule.make()
        self.transaction = self.transaction.make()

        cancel_data = {'order_id': self.transaction.transaction_id}
        self.client.force_authenticate(user=self.user)
      
        response = self.client.post(url, data=json.dumps(cancel_data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Transaction.objects.filter(transaction_id=self.transaction.transaction_id).exists(), False)
        self.assertEqual(response.json(), {'message': "booking has been cancelled"})

    def test_cancel_booking_failed(self):
        url = reverse('cancel-booking')
        self.user = self.user.make()
        self.tutor = self.tutor.make()
        self.schedule = self.schedule.make()
        self.transaction = self.transaction.make()

        cancel_data = {'order_id': self.transaction.transaction_id}
        self.client.force_authenticate(user=self.user)
   
        with patch('requests.post') as mock_request:
            mock_request.return_value.status_code = 400
            response = self.client.post(url, data=json.dumps(cancel_data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(Transaction.objects.filter(transaction_id=self.transaction.transaction_id).exists(), True)
        self.assertEqual(response.json(), {'message': "booking can't be cancelled"})

    def tearDown(self):
        Transaction.objects.all().delete()
        Schedule.objects.all().delete()
        Tutor.objects.all().delete()
        User.objects.all().delete()

class GetTutorTotalIncomeTestCase(APITestCase):
    def setUp(self):
        # create a user
        self.user = User.objects.create(
            email='test@example.com',
            password='testpass'
        )
        
        # create a tutor
        self.tutor = Tutor.objects.create(
            uid=self.user,
            price_per_hour=10.0
        )
        
        # create a schedule
        self.schedule = Schedule.objects.create(
            tutor_id=self.tutor,
            learner_id=self.user,
            date_time='2023-05-06 10:00:00',
            is_booked=True
        )
        
        # create some transactions for the tutor
        Transaction.objects.create(
            transaction_id='t1',
            learner=self.user,
            tutor=self.tutor,
            schedule=self.schedule,
            status='success',
            price=10.0,
            snap_token='snap1'
        )
        
        Transaction.objects.create(
            transaction_id='t2',
            learner=self.user,
            tutor=self.tutor,
            schedule=self.schedule,
            status='success',
            price=10.0,
            snap_token='snap2'
        )
        
    def test_get_tutor_total_income(self):
        # login the user
        self.client.force_authenticate(user=self.user)
        
        # make a GET request to the view
        url = reverse('tutor-income')
        response = self.client.get(url)
        
        # assert that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # assert that the response contains the correct total income
        expected_response = {
            "tutor_id": self.tutor.pk,
            "total_income": 20.0
        }
        self.assertEqual(response.json(), expected_response)

    def test_tutor_not_found(self):
        self.user = User.objects.create(
            email='test2@example.com',
            password='testpass'
        )

        self.client.force_authenticate(user=self.user)

        # make a GET request to the view
        url = reverse('tutor-income')
        response = self.client.get(url)

        # assert that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {"message": "Tutor not found"})
        
class GetLearnerPaidBookingTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpassword',
            profile_picture = "image.jpg"
        )
        self.tutor = Tutor.objects.create(
            uid=self.user,
            subject='Maths',
            price_per_hour=50
        )
        self.schedule = Schedule.objects.create(
            tutor_id=self.tutor,
            date_time='2023-05-06 10:00:00',
            is_booked=False
        )
        self.transaction = Transaction.objects.create(
            transaction_id='1a2b3c',
            learner=self.user,
            tutor=self.tutor,
            schedule=self.schedule,
            price=50,
            status='COMPLETED',
            snap_token='snap_token_123'
        )

    def test_get_learner_paid_booking(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('booking-paid')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['booking_list']), 1)
        self.assertEqual(response.json()['booking_list'][0]['transaction_id'], '1a2b3c')
        self.assertEqual(response.json()['booking_list'][0]['price'], 50)
        self.assertEqual(response.json()['booking_list'][0]['status'], 'COMPLETED')
        self.assertEqual(response.json()['booking_list'][0]['snap_token'], 'snap_token_123')
        self.assertEqual(response.json()['booking_list'][0]['tutor_name'], 'Test User')
        self.assertEqual(response.json()['booking_list'][0]['subject'], 'Maths')
        self.assertEqual(response.json()['booking_list'][0]['tutor_email'], 'test@example.com')
        self.assertEqual(str(response.json()['booking_list'][0]['uid']), str(self.tutor.uid.uid))
        self.assertEqual(response.json()['booking_list'][0]['profile_pic'], '/media/image.jpg')
        self.assertEqual(response.json()['booking_list'][0]['schedule_id'], self.schedule.pk)
        
class GetTutorBookedScheduleTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='testuser@test.com', password='testpass', role=User.TUTOR)
        self.tutor = Tutor.objects.create(uid=self.user, price_per_hour=20.0)
        self.schedule = Schedule.objects.create(date_time='2023-05-15 14:00:00')
        self.transaction = Transaction.objects.create(
            transaction_id='abc123',
            learner=self.user,
            tutor=self.tutor,
            schedule=self.schedule,
            price=20.0,
            status='COMPLETED',
            snap_token='snap_token'
        )

    def test_get_tutor_booked_schedule(self):
        url = reverse('tutor-paid-schedule')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['booking_list']), 1)
        transaction = response.json()['booking_list'][0]
        self.assertEqual(transaction['transaction_id'], 'abc123')
        self.assertEqual(transaction['schedule'], '2023-05-15T07:00:00Z')
        self.assertEqual(transaction['price'], 20.0)
        self.assertEqual(transaction['status'], 'COMPLETED')
        self.assertEqual(transaction['snap_token'], 'snap_token')
