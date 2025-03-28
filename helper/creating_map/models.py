from django.db import models
from profiles.models import User
# Create your models here.


class MapImage(models.Model):
    map_image = models.ImageField(upload_to='maps/')
    name = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)