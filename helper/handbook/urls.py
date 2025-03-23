from .views import get_handbook
from django.urls import path

urlpatterns = [
    path('', get_handbook, name="get_handbook"),
]