# Generated by Django 4.1.7 on 2023-04-04 08:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("tutor_register", "0007_alter_tutor_ktm_person_alter_tutor_ktp_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Schedule",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_time", models.DateTimeField()),
                ("is_booked", models.BooleanField(default=False)),
                ("is_finished", models.BooleanField(default=False)),
                (
                    "learner_id",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "tutor_id",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="tutor_register.tutor",
                    ),
                ),
            ],
        ),
    ]
