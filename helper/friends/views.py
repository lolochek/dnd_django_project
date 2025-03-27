from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FriendRequest, Friendship
from django.conf import settings

from profiles.models import User


@login_required
def send_friend_request(request, user_id):
    receiver = get_object_or_404(User, id=user_id)

    if FriendRequest.objects.filter(sender=request.user, receiver=receiver, accepted=False, declined=False).exists():
        messages.error(request, "Вы уже отправили запрос на добавление в друзья.")
        return redirect('show_user_dashboard', user_id=user_id)

    if Friendship.objects.filter(user1=request.user, user2=receiver).exists() or Friendship.objects.filter(user1=receiver, user2=request.user).exists():
        messages.error(request, "Вы уже друзья.")
        return redirect('show_user_dashboard', user_id=user_id)

    FriendRequest.objects.create(sender=request.user, receiver=receiver)
    messages.success(request, f'Запрос на добавление в друзья отправлен {receiver.username}.')
    return redirect('show_user_dashboard', user_id=user_id)



@login_required
def remove_friend(request, user_id):
    ex_friend = get_object_or_404(User, id=user_id)


    messages.success(request, f'Друг успешно удалён {ex_friend.username}.')
    return redirect('show_user_dashboard', user_id=user_id)

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

    return redirect('show_user_dashboard', user_id=friend_request.sender.id)

@login_required
def friends_list(request):
    friendships = Friendship.objects.filter(user1=request.user) | Friendship.objects.filter(user2=request.user)
    friends = {friendship.user1 if friendship.user2 == request.user else friendship.user2 for friendship in friendships}
    return render(request, 'friends_list.html', {'friends': friends})

@login_required
def friend_requests_list(request):

    friend_requests = FriendRequest.objects.filter(receiver=request.user, accepted=False, declined=False)
    friend_requests2 = FriendRequest.objects.filter(sender=request.user)

    return render(request, 'friends_requests.html', {'friend_requests': friend_requests, 'friend_requests2': friend_requests2})
