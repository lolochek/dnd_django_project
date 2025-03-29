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

class MonsterDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = Monster.objects.all()
    serializer_class = MonsterSerializer

class MagicItemListApiView(ListAPIView):
    queryset = MagicItem.objects.all()
    serializer_class = MagicItemSerializer

class MagicItemDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = MagicItem.objects.all()
    serializer_class = MagicItemSerializer
