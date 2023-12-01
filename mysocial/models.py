from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_image = models.ImageField(
        upload_to="profile_images/", null=True, blank=True,
    )
    phone_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=15,
                              choices=[('male', 'Male'),
                                       ('female', 'Female')]
                              )
    dob = models.DateField()
    address = models.TextField()

    def __str__(self):
        return self.user.username


class FriendRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    from_user = models.ForeignKey(
        UserProfile,
        related_name='sent_requests',
        on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        UserProfile,
        related_name='received_requests',
        on_delete=models.CASCADE
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,
                              default='pending')
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Enforce that from_user and to_user must be different for each row
        constraints = [
            models.CheckConstraint(
                check=~models.Q(from_user=models.F('to_user')),
                name='different_users'
            ),

            # models.UniqueConstraint(
            #     fields=['from_user', 'to_user'],
            #     condition=models.Q(from_user=models.F('to_user')) &
            #               models.Q(to_user=models.F('from_user')),
            #     name='reverse_unique_together',
            # ),
            # models.UniqueConstraint(
            #     fields=['from_user', 'to_user'],
            #     condition=models.Q(from_user=models.F('to_user')),
            #     name='unique_pair'
            # ),
            # models.UniqueConstraint(
            #     fields=['to_user', 'from_user'],
            #     condition=models.Q(to_user=models.F('from_user')),
            #     name='unique_pair_reverse'
            # )
            models.UniqueConstraint(
                fields=['to_user', 'from_user'],
                condition=models.Q(to_user__lte=models.F('from_user')),
                name='unique_pair'
            )
        ]
