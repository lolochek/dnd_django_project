from django.urls import path

from . import api
from .views import get_handbook, monster_detail, add_comment, request_monster_change, my_change_requests, \
    change_requests_list, process_change_request, magic_item_detail, spell_detail, home

urlpatterns = [
    path('', get_handbook, name='get_handbook'),

    path('spells/<int:spell_id>/', spell_detail, name='spell_detail'),
    path('monsters/<int:monster_id>/', monster_detail, name='monster_detail'),
    path('magic-items/<int:item_id>/', magic_item_detail, name='magic_item_detail'),

    path('comment/<str:model_name>/<int:object_id>/', add_comment, name='add_comment'),

    path('monster/<int:monster_id>/edit/', request_monster_change, name='monster_edit'),
    path('spells/<int:spell_id>/edit/', request_monster_change, name='spell_edit'),

    path('my-requests/', my_change_requests, name='my_change_requests'),
    path('change-requests/', change_requests_list, name='change_requests_list'),
    path('change-request/<int:request_id>/<str:action>/', process_change_request, name='process_change_request'),

    path('api-spells/', api.SpellListApiView.as_view(), name='api_spell_list'),
    path('api-spells/<int:pk>/', api.SpellDetailApiView.as_view(), name='api_spell_detail'),
    path('api-monsters/', api.MonsterListApiView.as_view(), name='api_monster_list'),
    path('api-monsters/<int:pk>/', api.MonsterDetailApiView.as_view(), name='api_monster_detail'),
    path('api-magic-items/', api.MagicItemListApiView.as_view(), name='api_magic_item_list'),
    path('api-magic-items/<int:pk>/', api.MagicItemDetailApiView.as_view(), name='api_magic_item_detail'),
]