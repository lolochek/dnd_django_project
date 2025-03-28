import json

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from .forms import CommentForm, MonsterEditForm
from .models import Spell, Monster, MagicItem, Comment, ChangeRequest


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

    return render(request, "handbook.html", {'notes': notes, 'category': category})



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

    return render(request, 'monster_detail.html', {
        'monster': monster,
        'comments': comments,
        'form': form
    })


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
def monster_edit(request, monster_id):
    monster = get_object_or_404(Monster, pk=monster_id)

    if request.method == 'POST':
        form = MonsterEditForm(request.POST, instance=monster)
        if form.is_valid():
            changes = {}
            for field in form.cleaned_data:
                old_value = getattr(monster, field)
                new_value = form.cleaned_data[field]
                if old_value != new_value:
                    changes[field] = new_value

            if changes:
                ChangeRequest.objects.create(
                    user=request.user,
                    content_object=monster,
                    changes=changes
                )
            messages.success(request, 'Заявка на редактирование отправлена.')
            return redirect('monster_detail', monster_id=monster.pk)

    else:
        form = MonsterEditForm(instance=monster)

    return render(request, 'monster_edit.html', {'form': form, 'monster': monster})






@login_required
def my_change_requests(request):
    requests = ChangeRequest.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'user_requests.html', {'requests': requests})

@staff_member_required
def change_requests_list(request):
    change_requests = ChangeRequest.objects.select_related('user', 'content_type').order_by('-created_at')
    return render(request, 'change_requests_list.html', {'change_requests': change_requests})


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