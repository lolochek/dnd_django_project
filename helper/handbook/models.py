from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models import JSONField


# Create your models here.

class Spell(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    level = models.IntegerField()
    character_class = models.CharField(max_length=255)
    school = models.CharField(max_length=100)
    casting_time = models.CharField(max_length=100)
    range = models.CharField(max_length=100)
    components = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    additional_info = JSONField(blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)

    def apply_changes(self, changes):
        for field, value in changes.items():
            setattr(self, field, value)
        self.save()


class Monster(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    hit_points = models.IntegerField()
    armor_class = models.IntegerField()
    speed = models.CharField(max_length=100)
    abilities = models.JSONField()
    additional_info = JSONField(blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)


    def apply_changes(self, changes):
        for field, value in changes.items():
            setattr(self, field, value)
        self.save()


class MagicItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    rarity = models.CharField(max_length=100)
    effect = models.TextField()
    additional_info = JSONField(blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)

    def apply_changes(self, changes):
        for field, value in changes.items():
            setattr(self, field, value)
        self.save()


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')


class ChangeRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В обработке...'),
        ('approved', 'Принят'),
        ('rejected', 'Отклонён'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    changes = models.JSONField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

