# Generated by Django 4.2.6 on 2023-10-23 08:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mysocial', '0010_remove_userprofile_friend_delete_friendrequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='FriendRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], default='pending', max_length=10)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend_requests_sent', to='mysocial.userprofile')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend_requests_received', to='mysocial.userprofile')),
            ],
        ),
        migrations.AddField(
            model_name='userprofile',
            name='friend',
            field=models.ManyToManyField(related_name='sent_friend_requests', through='mysocial.FriendRequest', to='mysocial.userprofile'),
        ),
    ]
