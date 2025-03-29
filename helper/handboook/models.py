from django.db import models



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
    abilities = models.TextField()
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
    last_updated = models.DateTimeField(auto_now=True)

    def apply_changes(self, changes):
        for field, value in changes.items():
            setattr(self, field, value)
        self.save()


