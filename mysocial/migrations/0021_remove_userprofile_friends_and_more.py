# Generated by Django 4.2.6 on 2023-11-07 06:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mysocial', '0020_remove_userprofile_age'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='friends',
        ),
        migrations.AddField(
            model_name='friendrequest',
            name='friendship_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
