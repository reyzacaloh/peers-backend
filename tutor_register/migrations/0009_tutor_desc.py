# Generated by Django 4.1.7 on 2023-05-04 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutor_register', '0008_tutor_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutor',
            name='desc',
            field=models.TextField(default=''),
        ),
    ]
