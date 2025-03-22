from .views import create_miniature
from django.urls import path

urlpatterns = [
    path('', create_miniature, name="create_miniature"),
]