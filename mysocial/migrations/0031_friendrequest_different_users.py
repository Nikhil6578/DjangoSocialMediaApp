# Generated by Django 4.2.6 on 2023-11-10 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysocial', '0030_alter_friendrequest_unique_together_and_more'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='friendrequest',
            constraint=models.CheckConstraint(check=models.Q(('from_user', models.F('to_user')), _negated=True), name='different_users'),
        ),
    ]
