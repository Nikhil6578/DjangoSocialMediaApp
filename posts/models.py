# django imports
from django.db import models

# self imports
from mysocial.models import UserProfile


class UserPost(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ImageField(
        upload_to="profile_images/", null=True, blank=True
    )
    dop = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    caption = models.TextField()

    def __str__(self):
        return self.userprofile.user.username
