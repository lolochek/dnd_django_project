from django.db import models

from profiles.models import User
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True)
