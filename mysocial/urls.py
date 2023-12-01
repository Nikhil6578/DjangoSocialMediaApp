from django.urls import path
from . import views

app_name = 'mysocial'

urlpatterns = [
    path("signup/", views.signup_or_update, name="signup"),
    path("login/", views.user_login, name="user_login"),
    path("userdetail/", views.user_detail, name="user_detail"),
    path("userupdate/", views.signup_or_update, name="user_update"),

    # ... Friend Suggestion Urls ...
    path('friend_suggestion/', views.friend_suggestion,
         name='friend_suggestion'),
    path('send_friend_request/<int:user_id>/',
         views.send_or_cancel_friend_request,
         name='send_friend_request'),
    path('cancel_friend_request/<int:user_id>/',
         views.send_or_cancel_friend_request,
         name='cancel_friend_request'),
    path('accept_friend_request/<int:request_id>/',
         views.manage_receive_friend_request
         ,
         {'action': 'accept'}, name='accept_friend_request'),
    path('reject_friend_request/<int:request_id>/',
         views.manage_receive_friend_request
         ,
         {'action': 'reject'}, name='reject_friend_request'),

    # Friend_List Urls
    path('friendrequestlist/', views.friend_request_list,
         name='friend_request_list'),
    path('friendslist/', views.friends_list, name='friend_list'),
    path('user_friend_delete/<int:request_id>/', views.user_friend_delete,
         name='user_friend_delete'),

    # logout
    path('logout/', views.logout_view, name="logout_view")
]
