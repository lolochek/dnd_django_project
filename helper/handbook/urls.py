from django.urls import path
from .views import (
    get_index,
    get_handbook,
    spell_detail,
    monster_detail,
    magic_item_detail
)

urlpatterns = [
    path('main/', get_index, name="get_index"),
    path('', get_handbook, name='get_handbook'),

    path('spells/<int:spell_id>/', spell_detail, name='spell_detail'),
    path('monsters/<int:monster_id>/', monster_detail, name='monster_detail'),
    path('magic-items/<int:item_id>/', magic_item_detail, name='magic_item_detail'),

]
