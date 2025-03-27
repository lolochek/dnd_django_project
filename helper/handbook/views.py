from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, get_object_or_404
from .models import Spell, Monster, MagicItem, Comment

# Create your views here.

def get_handbook(request):
    category = request.GET.get('category', 'monsters')
    notes = []

    if category == 'spells':
        notes = Spell.objects.all()
    elif category == 'magic_items':
        notes = MagicItem.objects.all()
    else:
        notes = Monster.objects.all()

    return render(request, "handbook.html", {'notes': notes, 'category': category})


def get_index(request):
    return render(request, "index.html", {})


def spell_detail(request, spell_id):
    spell = get_object_or_404(Spell, id=spell_id)

    spell_content_type = ContentType.objects.get_for_model(Spell)

    comments = Comment.objects.filter(
        content_type=spell_content_type,
        object_id=spell.id,
        parent__isnull=True
    ).select_related('user').prefetch_related('replies')

    return render(request, 'spell_detail.html', {'spell': spell, 'comments': comments})


def monster_list(request):
    monsters = Monster.objects.all()
    return render(request, "handbook.html", {'monsters': monsters})


def monster_detail(request, monster_id):
    monster = get_object_or_404(Monster, id=monster_id)

    monster_content_type = ContentType.objects.get_for_model(Monster)

    comments = Comment.objects.filter(
        content_type=monster_content_type,
        object_id=monster.id,
        parent__isnull=True
    ).select_related('user').prefetch_related('replies')

    return render(request, 'monster_detail.html', {'monster': monster, 'comments': comments})

def magic_item_list(request):
    magic_items = MagicItem.objects.all()
    return render(request, 'magic_item_list.html', {'magic_items': magic_items})


def magic_item_detail(request, item_id):
    magic_item = get_object_or_404(MagicItem, id=item_id)

    magic_item_content_type = ContentType.objects.get_for_model(MagicItem)

    comments = Comment.objects.filter(
        content_type=magic_item_content_type,
        object_id=magic_item.id,
        parent__isnull=True
    ).select_related('user').prefetch_related('replies')

    return render(request, 'magic_item_detail.html', {'magic_item': magic_item, 'comments': comments})
