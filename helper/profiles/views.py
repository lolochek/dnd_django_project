from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User

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
                login(request, user)
                messages.success(request, 'Вы успешно вошли!')
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
