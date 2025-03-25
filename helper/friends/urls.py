from django.urls import path
from .views import friends_list, profile_view

urlpatterns = [
    path('list/', friends_list, name='friends_list'),

    path('profile/<int:user_id>/', profile_view, name='user_profile'),

]
