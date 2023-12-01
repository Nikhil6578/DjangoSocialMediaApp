from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path("user_post_upload/", views.upload_or_edit_post,
         name="user_post_upload"),
    path('edit_user_post/<int:post_id>/', views.upload_or_edit_post,
         name='edit_user_post'),
    path("user_post/", views.user_post_or_friend_post, name="post_view"),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),

    # User Friend Posts Url
    path('user_friend_post/<int:request_id>/', views.user_post_or_friend_post,
         name='user_friend_post'),
]
