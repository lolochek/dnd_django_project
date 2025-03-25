from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FriendRequest, Friendship
from django.conf import settings


@login_required
def send_friend_request(request, user_id):
    receiver = get_object_or_404(settings.AUTH_USER_MODEL, id=user_id)

    if request.user == receiver:
        messages.error(request, "Невозможно отправить запрос самому себе.")
        return redirect('profile', user_id=user_id)

    if FriendRequest.objects.filter(sender=request.user, receiver=receiver, accepted=False, declined=False).exists():
        messages.error(request, "Вы уже отправили запрос на добавление в друзья.")
        return redirect('profile', user_id=user_id)

    FriendRequest.objects.create(sender=request.user, receiver=receiver)
    messages.success(request, f'Запрос на добавление в друзья отправлен {receiver.username}.')
    return redirect('profile', user_id=user_id)


@login_required
def respond_friend_request(request, request_id, action):
    friend_request = get_object_or_404(FriendRequest, id=request_id, receiver=request.user)

    if action == 'accept':
        friend_request.accepted = True
        friend_request.save()

        Friendship.objects.create(user1=friend_request.sender, user2=request.user)

        messages.success(request, "Вы стали друзьями!")
    elif action == 'decline':
        friend_request.declined = True
        friend_request.save()

        messages.success(request, "Вы отклонили запрос на добавление в друзья.")

    return redirect('profile', user_id=friend_request.sender.id)

@login_required
def friends_list(request):
    friendships = Friendship.objects.filter(user1=request.user) | Friendship.objects.filter(user2=request.user)
    friends = {friendship.user1 if friendship.user2 == request.user else friendship.user2 for friendship in friendships}
    return render(request, 'friends_list.html', {'friends': friends})


@login_required
def profile_view(request, user_id):
    user = get_object_or_404(settings.AUTH_USER_MODEL, id=user_id)
    return render(request, 'profile.html', {'user_dashboard.html': user})
