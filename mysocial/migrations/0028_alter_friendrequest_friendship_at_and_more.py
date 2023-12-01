# Generated by Django 4.2.6 on 2023-11-08 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysocial', '0027_remove_userprofile_friendship_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendrequest',
            name='friendship_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterUniqueTogether(
            name='friendrequest',
            unique_together={('from_user', 'to_user')},
        ),
    ]