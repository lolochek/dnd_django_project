from django.shortcuts import render, get_object_or_404
from .models import Spell, Monster, MagicItem, Comment

# Create your views here.

def get_handbook(request):
    return render(request, "handbook.html", {})

def get_index(request):
    return render(request, "index.html", {})


def spell_list(request):
    spells = Spell.objects.all()
    return render(request, 'spell_list.html', {'spells': spells})

def spell_detail(request, spell_id):
    spell = get_object_or_404(Spell, id=spell_id)
    comments = Comment.objects.filter(spell=spell, parent__isnull=True).select_related('user').prefetch_related('replies')
    return render(request, 'spell_detail.html', {'spell': spell, 'comments': comments})

def monster_list(request):
    monsters = Monster.objects.all()
    return render(request, 'monster_list.html', {'monsters': monsters})

def monster_detail(request, monster_id):
    monster = get_object_or_404(Monster, id=monster_id)
    comments = Comment.objects.filter(monster=monster, parent__isnull=True).select_related('user').prefetch_related('replies')
    return render(request, 'monster_detail.html', {'monster': monster, 'comments': comments})

def magic_item_list(request):
    magic_items = MagicItem.objects.all()
    return render(request, 'magic_item_list.html', {'magic_items': magic_items})

def magic_item_detail(request, item_id):
    magic_item = get_object_or_404(MagicItem, id=item_id)
    comments = Comment.objects.filter(magic_item=magic_item, parent__isnull=True).select_related('user').prefetch_related('replies')
    return render(request, 'magic_item_detail.html', {'magic_item': magic_item, 'comments': comments})
