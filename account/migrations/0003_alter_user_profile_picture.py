# Generated by Django 4.1.7 on 2023-03-02 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_user_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=models.CharField(blank=True, max_length=700, null=True),
        ),
    ]
