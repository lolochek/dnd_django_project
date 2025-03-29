from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from .models import Spell, Monster, MagicItem
from .serializers import SpellSerializer, MonsterSerializer, MagicItemSerializer

class SpellListApiView(ListAPIView):
    queryset = Spell.objects.all()
    serializer_class = SpellSerializer

class SpellDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = Spell.objects.all()
    serializer_class = SpellSerializer


class MonsterListApiView(ListAPIView):
    queryset = Monster.objects.all()
    serializer_class = MonsterSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['armor_class', 'hit_points']

    search_fields = ['name', 'description', 'abilities']

    ordering_fields = ['name', 'hit_points', 'armor_class']

class MonsterDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = Monster.objects.all()
    serializer_class = MonsterSerializer

class MagicItemListApiView(ListAPIView):
    queryset = MagicItem.objects.all()
    serializer_class = MagicItemSerializer

class MagicItemDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = MagicItem.objects.all()
    serializer_class = MagicItemSerializer
