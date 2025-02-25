from django.db import models
from tutor_register.models import Tutor
from account.models import User
# Create your models here.
class Schedule(models.Model):
    tutor_id = models.ForeignKey(Tutor, on_delete=models.CASCADE, null=True, blank=True)
    learner_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date_time = models.DateTimeField()
    is_booked = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)
