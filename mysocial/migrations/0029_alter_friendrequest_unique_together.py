# Generated by Django 4.2.6 on 2023-11-09 07:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysocial', '0028_alter_friendrequest_friendship_at_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='friendrequest',
            unique_together={('to_user', 'from_user'), ('from_user', 'to_user')},
        ),
    ]