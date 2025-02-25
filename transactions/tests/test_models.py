from django.test import TestCase
from django.utils import timezone
from account.models import User
from tutor_register.models import Tutor
from schedule.models import Schedule
from  ..models import Transaction
from model_bakery import baker

class TransactionModelTest(TestCase):
    def setUp(self):
        self.user = baker.make(User)
        self.tutor = baker.make(Tutor)
        self.schedule = baker.make(Schedule)

        self.transaction = Transaction.objects.create(
            transaction_id='test-transaction-id', learner=self.user,
            tutor=self.tutor, schedule=self.schedule, status='pending', price=10.0)

    def test_transaction_model(self):
        self.assertEqual(str(self.transaction.transaction_id), 'test-transaction-id')
        self.assertEqual(self.transaction.learner, self.user)
        self.assertEqual(self.transaction.tutor, self.tutor)
        self.assertEqual(self.transaction.schedule, self.schedule)
        self.assertEqual(self.transaction.status, 'pending')
        self.assertEqual(self.transaction.price, 10.0)
        self.assertIsNone(self.transaction.snap_token)
