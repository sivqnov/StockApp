from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterUserForm, RegisterProfileForm, PasswordChangingForm, SettingPasswordForm
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.views import PasswordChangeView, PasswordResetConfirmView
from django.urls import reverse_lazy

# Create your views here.

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            messages.success(request, ("Возникла ошибка при попытке входа в аккаунт. Попробуйте снова!"))
            return redirect('login')
    else:
        context = {
            'title': 'Вход в аккаунт',
        }
        return render(request, 'login.html', context)

def logout_user(request):
    username = request.user
    logout(request)
    messages.success(request, (f"Вы успешно вышли из аккаунта {username}"))
    return redirect('main')

def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        formProfile = RegisterProfileForm(request.POST)
        if form.is_valid() and formProfile.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            bio = formProfile.cleaned_data['bio']
            userobj = User.objects.get(username=username)
            Profile.objects.create(user=userobj, photo='default_user.png', bio=bio)
            messages.success(request, ("Регистрация успешна!"))
            return redirect('main')
    else:
        form = RegisterUserForm()
        formProfile = RegisterProfileForm()
    context = {
        'title': 'Регистрация',
        'form': form,
        'formProfile': formProfile,
        }
    return render(request, 'register.html', context)

def user_profile(request, user):
    try:
        userobj = User.objects.get(username=user)
        profile = Profile.objects.get(user = userobj.id)
        context = {
            'struser': str(request.user),
            'profile': profile,
            'request': request,
        }
        return render(request, 'profile.html', context)
    except:
        messages.success(request, ("Пользователя с таким именем не найдено!"))
        return redirect('main')

class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('main')

class PasswordsResetConfirmView(PasswordResetConfirmView):
    form_class = SettingPasswordForm
    success_url = reverse_lazy('password_reset_complete')