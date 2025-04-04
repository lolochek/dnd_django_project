from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import EditProfileForm
from .models import User

from friends.models import Friendship

# Create your views here.

def user_registration_view(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            email = request.POST.get('email')
            login_id = request.POST.get('login')
            password = request.POST.get('password')
            avatar = request.FILES.get('avatar')
            profile_description = request.POST.get('profile_description')

            if not username or not email or not login_id or not password:
                messages.error(request, 'Все поля должны быть заполнены.')
                return render(request, 'registration.html')

            if User.objects.filter(email=email).exists():
                messages.error(request, 'Пользователь с таким email уже существует.')
                return render(request, 'registration.html')

            if User.objects.filter(login=login_id).exists():
                messages.error(request, 'Пользователь с таким логином уже существует.')
                return render(request, 'registration.html')

            user = User(username=username, email=email, login=login_id, avatar=avatar,
                        profile_description=profile_description)
            user.set_password(password)
            user.save()

            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Ошибка регистрации: {str(e)}')
            return render(request, 'registration.html')
    return render(request, 'registration.html')


def user_login_view(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')
            if not email or not password:
                messages.error(request, 'Введите email и пароль.')
                return render(request, 'login.html')

            user = authenticate(request, email=email, password=password)
            if user is not None:
                if not user.is_active:
                    messages.error(request, 'Ваш аккаунт заблокирован. Чао')
                    return render(request, 'login.html')

                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Неверный email или пароль.')
        except Exception as e:
            messages.error(request, f'Ошибка входа: {str(e)}')
    return render(request, 'login.html')


@login_required(login_url='/login/')
def user_dashboard_view(request):
    return render(request, 'dashboard.html', {'user': request.user})


def user_logout_view(request):
    try:
        logout(request)
        messages.success(request, 'Вы вышли из системы.')
    except Exception as e:
        messages.error(request, f'Ошибка выхода: {str(e)}')
    return redirect('login')

def registration_success(request):
    return render(request, 'registration_success.html')


@login_required
def delete_profile(request):
    if request.method == 'GET' and request.GET.get('confirm_delete') == 'DELETE':
        user = request.user
        user.delete()
        messages.success(request, 'Ваш аккаунт был удален.')
        return redirect('login')
    return render(request, 'confirm_delete.html')



@login_required
def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        else:
            messages.error(request, 'Ошибка при обновлении профиля. Проверьте введенные данные.')
    else:
        form = EditProfileForm(instance=user)

    return render(request, 'edit_profile.html', {'form': form})


from django.db.models import Q


@login_required
def all_users(request):
    friendships = Friendship.objects.filter(user1=request.user) | Friendship.objects.filter(user2=request.user)
    friends = {friendship.user1 if friendship.user2 == request.user else friendship.user2 for friendship in friendships}

    search_query = request.GET.get('search', '')

    users = User.objects.exclude(
        Q(id=request.user.id) | Q(is_superuser=True) | Q(is_staff=True)
    )
    if search_query:
        users = users.filter(Q(username__icontains=search_query) | Q(login__icontains=search_query))

    return render(request, 'all_users.html', {'users': users, 'friends': friends, 'search_query': search_query})


@login_required
def search_users(request):
    query = request.GET.get('q', '')
    users = User.objects.filter(username__icontains=query) if query else []
    return render(request, 'search_results.html', {'users': users, 'query': query})


@login_required
def show_user_dashboard(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.user == user:
        return redirect('dashboard')

    friendships = Friendship.objects.filter(user1=user) | Friendship.objects.filter(user2=user)
    friends = {friendship.user1 if friendship.user2 == user else friendship.user2 for friendship in friendships}

    return render(request, 'user_dashboard.html', {'user': user, 'friends': friends})


@staff_member_required
def change_user_activity(request, user_id, is_active):
    user = get_object_or_404(User, id=user_id)

    user.is_active = bool(is_active)
    user.save()

    messages.success(request,f"Уровень доступа пользователя '{user.username}' изменен на {'активен' if user.is_active else 'неактивен'}.")

    return redirect(all_users)
