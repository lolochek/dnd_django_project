from django.conf.urls.static import static
from django.urls import path

from .views import user_registration_view, registration_success, user_login_view, user_logout_view, user_dashboard_view
from django.conf import settings

urlpatterns = [
    path('register/', user_registration_view, name='register'),
    path('login/', user_login_view, name='login'),
    path('logout/', user_logout_view, name='logout'),
    path('dashboard/', user_dashboard_view, name='dashboard'),
    path('registration-success/', registration_success, name='registration_success'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)