from .views import get_handbook, get_index, spell_list, spell_detail, monster_list, monster_detail, magic_item_list, \
    magic_item_detail
from django.urls import path

urlpatterns = [
    path('main/', get_index, name="get_index"),
    path('', get_handbook, name="get_handbook"),

    path('spells/', spell_list, name='spell_list'),
    path('spells/<int:spell_id>/', spell_detail, name='spell_detail'),
    path('monsters/', monster_list, name='monster_list'),
    path('monsters/<int:monster_id>/', monster_detail, name='monster_detail'),
    path('magic-items/', magic_item_list, name='magic_item_list'),
    path('magic-items/<int:item_id>/', magic_item_detail, name='magic_item_detail'),
]

