# Generated by Django 4.2.6 on 2023-10-23 08:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mysocial', '0008_friendship_friendrequest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friendrequest',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='friendrequest',
            name='is_accepted',
        ),
        migrations.AddField(
            model_name='friendrequest',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], default='pending', max_length=10),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='friend',
            field=models.ManyToManyField(related_name='sent_friend_requests', through='mysocial.FriendRequest', to='mysocial.userprofile'),
        ),
        migrations.AlterField(
            model_name='friendrequest',
            name='from_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend_requests_sent', to='mysocial.userprofile'),
        ),
        migrations.AlterField(
            model_name='friendrequest',
            name='to_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend_requests_received', to='mysocial.userprofile'),
        ),
        migrations.DeleteModel(
            name='Friendship',
        ),
    ]
