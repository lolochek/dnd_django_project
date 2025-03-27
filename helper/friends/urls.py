
from django.urls import path
from .views import send_friend_request, respond_friend_request, friends_list, friend_requests_list

urlpatterns = [
    path('send_friend_request/<int:user_id>/', send_friend_request, name='send_friend_request'),
    path('respond_friend_request/<int:request_id>/<str:action>/', respond_friend_request, name='respond_friend_request'),
    path('friends/list/', friends_list, name='friends_list'),
    path('friend_requests/', friend_requests_list, name='friend_requests_list'),
]
