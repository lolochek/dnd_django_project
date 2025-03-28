from django.conf.urls.static import static
from django.urls import path

from .views import user_registration_view, registration_success, user_login_view, user_logout_view, user_dashboard_view, \
    delete_profile, edit_profile, all_users, search_users, show_user_dashboard, change_user_activity
from django.conf import settings

urlpatterns = [
    path('register/', user_registration_view, name='register'),
    path('login/', user_login_view, name='login'),
    path('logout/', user_logout_view, name='logout'),
    path('dashboard/', user_dashboard_view, name='dashboard'),
    path('registration-success/', registration_success, name='registration_success'),

    path('edit/', edit_profile, name='edit_profile'),
    path('delete/', delete_profile, name='delete_profile'),

    path('users/', all_users, name='all_users'),
    path('search/', search_users, name='search_users'),
    path('user-dashboard/<int:user_id>/', show_user_dashboard, name='show_user_dashboard'),
    path('change-activity/<int:user_id>/<int:is_active>/', change_user_activity, name='change_user_activity')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)