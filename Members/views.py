from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterUserForm, RegisterProfileForm, PasswordChangingForm, SettingPasswordForm, UpdateUserForm, UpdateProfileForm
from django.contrib.auth.models import User
from Shop.models import Product, Shop
from .models import Profile, CartItem
from django.contrib.auth.views import PasswordChangeView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
import os
from Stock.settings import STATICFILES_DIRS
import json
# Create your views here.

def login_user(request):
    if request.user.is_authenticated:
        return redirect('user', user=str(request.user))
    else:
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

@login_required(login_url='login')
def logout_user(request):
    username = request.user
    logout(request)
    messages.success(request, (f"Вы успешно вышли из аккаунта {username}"))
    return redirect('main')

def register_user(request):
    if request.user.is_authenticated:
        return redirect('user', user=str(request.user))
    else:
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
            'title': userobj.get_username,
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

@login_required(login_url='login')
def delete_profile(request):
    try:
        userobj = User.objects.get(username=str(request.user)).delete()
        messages.success(request, ("Пользователь и все его данные были успешно удалены!"))
        return redirect('main')
    except:
        messages.success(request, ("Произошла ошибка!"))
        return redirect('main')

@login_required(login_url='login')
def edit_user(request):
    user = User.objects.get(username=str(request.user))
    profile = Profile.objects.get(user=user)
    form = UpdateUserForm(request.POST or None, instance=user)
    formProfile = UpdateProfileForm(request.POST or None, request.FILES or None, instance=profile)
    if form.is_valid() and formProfile.is_valid():
        form.save()
        formProfile.save()
        print(f"\n\n\n{str(Profile.objects.get(user=User.objects.get(username=form.cleaned_data['username'])).photo)}\n\n\n")
        if str(Profile.objects.get(user=User.objects.get(username=form.cleaned_data['username'])).photo) == "":
            Profile.objects.get(user=User.objects.get(username=form.cleaned_data['username'])).photo = os.path.join(STATICFILES_DIRS[0], 'images/default_user.png')
        messages.success(request, ("Данные сохранены!"))
        return redirect('user', user=user.username)
    context = {
        'request': request,
        'user': user,
        'profile': profile,
        'form': form,
        'formProfile': formProfile,
    }
    return render(request, 'edit_user.html', context)

@login_required(login_url='login')
def cart(request):
    profile = Profile.objects.get(user=request.user)
    total = 0
    for item in profile.cart.all():
        total += item.product.price * item.amount
    context = {
        'title': 'Корзина',
        'request': request,
        'profile': profile,
        'total': round(total, 2),
    }
    return render(request, 'cart.html', context)

@login_required(login_url='login')
def delete_from_cart(request, id):
    profile = Profile.objects.get(user=request.user)
    cart_item = CartItem.objects.get(id=id)
    product = Product.objects.get(id=cart_item.product.id)
    product.amount += cart_item.amount
    product.save()
    cart_item.delete()
    messages.success(request, ("Товар был удален из корзины"))
    return redirect('cart')

@login_required(login_url='login')
def add_to_cart(request, id):
    profile = Profile.objects.get(user=request.user)
    cart_item = CartItem.objects.get(id=id)
    product = Product.objects.get(id=cart_item.product.id)
    if product.amount > 1:
        product.amount -= 1
        product.save()
        cart_item.amount += 1
        cart_item.save()
        return redirect('cart')
    else:
        messages.success(request, ("Товар закончился на складе магазина"))
        return redirect('cart')

@login_required(login_url='login')
def sub_from_cart(request, id):
    profile = Profile.objects.get(user=request.user)
    cart_item = CartItem.objects.get(id=id)
    product = Product.objects.get(id=cart_item.product.id)
    if cart_item.amount > 1:
        product.amount += 1
        product.save()
        cart_item.amount -= 1
        cart_item.save()
        return redirect('cart')
    else:
        product.amount += 1
        product.save()
        cart_item.delete()
        messages.success(request, ("Товар был удален из корзины"))
        return redirect('cart')

@login_required(login_url='login')
def edit_cart(request, id):
    profile = Profile.objects.get(user=request.user)
    if profile.cart.filter(id=id).exists():
        if request.method == "POST":
            item = profile.cart.get(id=id)
            if Shop.objects.filter(name=request.POST.get('shop', 'default_shop')).exists():
                shop = Shop.objects.get(name=request.POST.get('shop', 'default_shop'))
                if Product.objects.filter(id=item.product.id).filter(stock=shop).exists():
                    max_to_order = item.amount + item.product.amount
                    form_amount = int(request.POST.get('amount', '0'))
                    print(f"\n\n\n{form_amount}\n\n\n")
                    if form_amount>0:
                        if form_amount > max_to_order:
                            messages.success(request, ("На складе магазине нет такого количества товара"))
                            return redirect('edit_cart', id=id)
                        else:
                            product = item.product
                            if form_amount > item.amount:
                                product.amount -= (form_amount - item.amount)
                                product.save()
                                item.amount = form_amount
                                item.save()
                            elif item.amount == form_amount:
                                pass
                            else:
                                product.amount += (item.amount - form_amount)
                                product.save()
                                item.amount = form_amount
                                item.save()
                            messages.success(request, ("Успех!"))
                            return redirect('cart')
                    else:
                        messages.success(request, ("Количество товара в корзине не может быть меньше или равно 0"))
                        return redirect('edit_cart', id=id)
                else:
                    messages.success(request, ("Такого товара не существует"))
                    return redirect('edit_cart', id=id)
            else:
                messages.success(request, ("Магазина с таким названием не существует"))
                return redirect('edit_cart', id=id)
        else:
            item = profile.cart.get(id=id)
            context = {
                'title': 'Редактирование товара в корзине',
                'request': request,
                'profile': Profile.objects.get(user=request.user),
                'item': item,
                'max_to_order': item.amount + item.product.amount,
                'start_price': round(item.amount * item.product.price, 2),
            }
            return render(request, 'edit_cart.html', context)
    else:
        messages.success(request, ("Такого товара нет в вашей корзине"))
        return redirect('cart')
    
@login_required(login_url='login')
def to_orders(request):
    profile = Profile.objects.get(user=request.user)
    
    messages.success(request, ("Товары были заказаны, корзина очищена!"))
    return redirect('cart')

@login_required(login_url='login')
def save_bio(request):
    if request.method == "POST":
        result = json.loads(request.body)
        profile = Profile.objects.get(user=request.user)
        bio = result.get('bio', 'none')
        profile.bio = bio
        profile.save()
        messages.success(request, ("Изменения сохранены!"))
    else:
        messages.success(request, ("Произошла ошибка!"))
    return redirect('user', user=str(request.user))