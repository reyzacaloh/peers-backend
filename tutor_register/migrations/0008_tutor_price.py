# Generated by Django 4.1.7 on 2023-05-04 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutor_register', '0007_alter_tutor_ktm_person_alter_tutor_ktp_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutor',
            name='price',
            field=models.IntegerField(default=30000),
        ),
    ]
