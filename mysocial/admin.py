from django.contrib import admin
from mysocial.models import UserProfile, FriendRequest


admin.site.register(UserProfile)
# admin.site.register(UserPost)
admin.site.register(FriendRequest)
