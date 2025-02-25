from django.db import models
from django.utils import timezone
from account.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

def upload_ktm(instance, filename):
    return 'ktm/{}/{}'.format(instance.uid.uid, filename)


def upload_transkrip(instance, filename):
    return 'transkrip/{}/{}'.format(instance.uid.uid, filename)


def upload_ktm_person(instance, filename):
    return 'ktm_person/{}/{}'.format(instance.uid.uid, filename)


# Create your models here.
class Tutor(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    subject = models.CharField(max_length=25)
    university = models.CharField(max_length=50)
    pddikti = models.CharField(max_length=100)
    ktp = models.FileField(upload_to=upload_ktm)
    transkrip = models.FileField(upload_to=upload_transkrip)
    ktm_person = models.ImageField(upload_to=upload_ktm_person)
    desc = models.TextField(default="")
    is_submitted = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)
    price_per_hour = models.FloatField(default=35000)
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],default=0.0, blank=True
    )
    review_count = models.IntegerField(blank=True, default=0)
