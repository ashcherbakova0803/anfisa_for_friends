from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import login, update_session_auth_hash, get_user_model
from django.contrib import messages
from .forms import UserForm, UserRegisterForm

User = get_user_model()


def register(request):
    """
    Регистрация нового пользователя.
    Использует кастомную форму UserRegisterForm.
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрированы!')
            return redirect('homepage:index')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile_view(request, username):
    """
    Страница профиля пользователя.
    """
    user = get_object_or_404(User, username=username)
    return render(request, 'users/profile.html', {'profile_user': user})


@login_required
def profile_edit(request):
    """
    Редактирование профиля текущего пользователя.
    """
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлён!')
            return redirect('users:profile', username=request.user.username)
    else:
        form = UserForm(instance=request.user)
    return render(request, 'users/profile_edit.html', {'form': form})


@login_required
def password_change(request):
    """
    Смена пароля текущего пользователя.
    """
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Пароль успешно изменён!')
            return redirect('users:profile', username=request.user.username)
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/password_change.html', {'form': form})
