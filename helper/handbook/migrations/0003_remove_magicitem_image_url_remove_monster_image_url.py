# Generated by Django 4.1.1 on 2025-03-27 21:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('handbook', '0002_remove_spell_distance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='magicitem',
            name='image_url',
        ),
        migrations.RemoveField(
            model_name='monster',
            name='image_url',
        ),
    ]
