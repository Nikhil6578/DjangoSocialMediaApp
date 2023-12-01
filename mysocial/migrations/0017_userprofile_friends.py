# Generated by Django 4.2.6 on 2023-10-25 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysocial', '0016_delete_friendrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='friends',
            field=models.ManyToManyField(blank=True, related_name='user_friends', to='mysocial.userprofile'),
        ),
    ]