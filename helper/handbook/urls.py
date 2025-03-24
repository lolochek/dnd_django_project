from .views import get_handbook, get_index
from django.urls import path

urlpatterns = [
    path('main/', get_index, name="get_index"),
    path('', get_handbook, name="get_handbook"),
]