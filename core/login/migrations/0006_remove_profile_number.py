# Generated by Django 5.0.4 on 2024-04-13 10:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0005_profile_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='number',
        ),
    ]
