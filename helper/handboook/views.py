from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from .forms import MonsterChangeForm
from .models import Spell, MagicItem, Monster
from handbook.models import Comment
from handbook.forms import CommentForm
from handbook.models import ChangeRequest

from articles.models import Article


# Create your views here.


def get_handbook(request):
    category = request.GET.get('category', 'monsters')
    notes = []

    if category == 'spells':
        notes = Spell.objects.all().order_by('name')
    elif category == 'magic_items':
        notes = MagicItem.objects.all().order_by('name')
    else:
        notes = Monster.objects.all().order_by('name')

    return render(request, "handbook1.html", {'notes': notes, 'category': category})


def monster_detail(request, monster_id):
    monster = get_object_or_404(Monster, id=monster_id)
    monster_content_type = ContentType.objects.get_for_model(Monster)

    comments = Comment.objects.filter(
        content_type=monster_content_type,
        object_id=monster.id,
        parent__isnull=True
    ).select_related('user').prefetch_related('replies')

    form = CommentForm()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.content_type = monster_content_type
            comment.object_id = monster.id
            comment.parent_id = request.POST.get("parent_id")
            comment.save()
            return redirect('monster_detail', monster_id=monster.id)

    return render(request, 'monster_detail1.html', {
        'monster': monster,
        'comments': comments,
        'form': form
    })

def spell_detail(request, spell_id):
    spell = get_object_or_404(Spell, id=spell_id)
    spell_content_type = ContentType.objects.get_for_model(Spell)

    comments = Comment.objects.filter(
        content_type=spell_content_type,
        object_id=spell.id,
        parent__isnull=True
    ).select_related('user').prefetch_related('replies')

    form = CommentForm()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.content_type = spell_content_type
            comment.object_id = spell.id
            comment.parent_id = request.POST.get("parent_id")
            comment.save()
            return redirect('spell_detail', spell_id=spell.id)

    return render(request, 'spell_detail.html', {
        'spell': spell,
        'comments': comments,
        'form': form
    })

def about(request):
    return render(request, 'about.html')

def magic_item_detail(request, item_id):
    magic_item = get_object_or_404(MagicItem, id=item_id)
    magic_item_content_type = ContentType.objects.get_for_model(MagicItem)

    comments = Comment.objects.filter(
        content_type=magic_item_content_type,
        object_id=magic_item.id,
        parent__isnull=True
    ).select_related('user').prefetch_related('replies')

    form = CommentForm()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.content_type = magic_item_content_type
            comment.object_id = magic_item.id
            comment.parent_id = request.POST.get("parent_id")
            comment.save()
            return redirect('magic_item_detail', item_id=magic_item.id)

    return render(request, 'magic_item_detail.html', {
        'magic_item': magic_item,
        'comments': comments,
        'form': form
    })


@login_required
def add_comment(request, monster_id):
    monster = get_object_or_404(Monster, id=monster_id)
    monster_content_type = ContentType.objects.get_for_model(Monster)
    parent_id = request.POST.get("parent_id")
    parent_comment = Comment.objects.filter(id=parent_id).first() if parent_id else None

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.content_type = monster_content_type
            comment.object_id = monster.id
            comment.parent = parent_comment
            comment.save()
            return redirect('monster_detail', monster_id=monster.id)

    return redirect('monster_detail', monster_id=monster.id)


@login_required
def request_monster_change(request, monster_id):
    monster = get_object_or_404(Monster, id=monster_id)

    if request.method == 'POST':
        form = MonsterChangeForm(request.POST)
        if form.is_valid():

            change_request = form.save_changes(user=request.user, monster=monster)
            messages.success(request, 'заявка на изменение отправлена!')
            return redirect('monster_detail', monster_id=monster.id)
    else:
        form = MonsterChangeForm(instance=monster)

    return render(request, 'request_monster_change.html', {
        'form': form,
        'monster': monster
    })




@login_required
def my_change_requests(request):
    requests = ChangeRequest.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'user_requests1.html', {'requests': requests})

@staff_member_required
def change_requests_list(request):
    change_requests = ChangeRequest.objects.select_related('user', 'content_type').order_by('-created_at')
    return render(request, 'change_requests_list1.html', {'change_requests': change_requests})


@staff_member_required
def process_change_request(request, request_id, action):
    change_request = get_object_or_404(ChangeRequest, id=request_id)

    if change_request.status != 'pending':
        messages.warning(request, 'Заявка уже обработана.')
        return redirect('change_requests_list')

    if action == 'approve':

        obj = change_request.content_object
        if obj:
            obj.apply_changes(change_request.changes)
            change_request.status = 'approved'
            change_request.save()
            messages.success(request, 'Заявка принята и изменения применены.')
    elif action == 'reject':
        change_request.status = 'rejected'
        change_request.save()
        messages.info(request, 'Заявка отклонена.')
    else:
        messages.error(request, 'Неверное действие.')

    return redirect('change_requests_list')


def home(request):
    articles = Article.objects.order_by('-created_at')[:5]

    latest_spells = Spell.objects.order_by('-last_updated')[:2]
    latest_monsters = Monster.objects.order_by('-last_updated')[:2]
    latest_items = MagicItem.objects.order_by('-last_updated')[:2]

    latest_updates = []

    for spell in latest_spells:
        latest_updates.append({'type': 'Заклинание', 'obj': spell})

    for monster in latest_monsters:
        latest_updates.append({'type': 'Монстр', 'obj': monster})

    for item in latest_items:
        latest_updates.append({'type': 'Магический предмет', 'obj': item})

    latest_updates.sort(key=lambda x: x['obj'].last_updated, reverse=True)

    return render(request, "home.html", {
        'articles': articles,
        'latest_updates': latest_updates,
    })