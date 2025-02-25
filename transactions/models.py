from django.db import models
from account.models import User
from tutor_register.models import Tutor
from schedule.models import Schedule
from django.utils import timezone

class Transaction(models.Model):
    transaction_id = models.CharField(primary_key=True, max_length=200)
    learner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, null=True)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=100)
    price = models.FloatField(default=0)
    snap_token = models.CharField(max_length=100, null=True)
