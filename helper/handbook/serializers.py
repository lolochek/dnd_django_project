from rest_framework import serializers
from .models import Spell, Monster, MagicItem

class SpellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spell
        fields = '__all__'

class MonsterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monster
        fields = '__all__'

class MagicItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MagicItem
        fields = '__all__'
