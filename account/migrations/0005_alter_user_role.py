# Generated by Django 4.1.7 on 2023-03-17 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_user_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Admin'), (2, 'TUTOR'), (3, 'LEARNER')], default=3, null=True),
        ),
    ]
