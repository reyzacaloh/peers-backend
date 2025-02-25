from django.test import TestCase
from django.core.exceptions import ValidationError
from account.models import User
from tutor_register.models import Tutor
from ..models import Schedule
import datetime
class ScheduleModelTest(TestCase):
    email = 'testuser@example.com'
    password = 'testpass123'

    def setUp(self):
        self.user = User.objects.create(
            email='test2@test.com',
            password='test',
            role=User.TUTOR
        )
        self.tutor = Tutor.objects.create(
            uid=self.user,
            subject = 'Matematika',
            university = 'Universitas 1'
        )

    def test_create_schedule(self):
        tutor_id = self.tutor
        create_schedule=Schedule.objects.create(
            tutor_id = tutor_id,
            date_time = '2023-04-23T18:00:00Z'
        )
        new_schedule = Schedule.objects.get(tutor_id = tutor_id)
        self.assertEqual(new_schedule,create_schedule)
        self.assertEqual(new_schedule.tutor_id, tutor_id)
        self.assertIsInstance(new_schedule.date_time, datetime.datetime)

    def test_create_schedule_with_invalid_date(self):
        tutor_id = self.tutor
        with self.assertRaises(ValidationError):
           Schedule.objects.create(
                tutor_id = tutor_id,
                date_time = 'lalala'
            )

    def test_delete_schedule(self):
        tutor_id = self.tutor
        Schedule.objects.create(
            tutor_id = tutor_id,
            date_time = '2023-04-23T18:00:00Z'
        )
        schedule = Schedule.objects.get(tutor_id = tutor_id)
        schedule.delete()
        self.assertEqual(Schedule.objects.filter(tutor_id = tutor_id).first(),None)
    
    def test_delete_non_existing_schedule(self):
        tutor_id = self.tutor
        with self.assertRaises(Schedule.DoesNotExist):
            schedule = Schedule.objects.get(tutor_id = tutor_id)
            schedule.delete()

