from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CreateShopForm, CreateProductForm
from django.contrib.auth.models import User
from .models import Shop, Product
from Members.models import Profile
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from random import randint
# Create your views here.

def generate_code():
    sym = 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890'
    result = ''
    for i in range(0, 16):
        result+=sym[randint(0, len(sym)-1)]
    return result

@login_required(login_url='login')
def create_shop(request):
    form = CreateShopForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        shop = Shop.objects.get(name=form.cleaned_data['name'])
        code = generate_code()
        shop.code = code
        shop.save()
        user = User.objects.get(username=str(request.user))
        Profile.objects.get(user=user).shops.add(shop)
        messages.success(request, ("Магазин успешно создан и добавлен к вам в профиль!"))
        return redirect('user', user=str(request.user))
    context = {
        'title': 'Создание предприятия',
        'request': request,
        'form': form,
    }
    return render(request, 'create_shop.html', context)

@login_required(login_url='login')
def edit_shop(request, name):
    profile = Profile.objects.get(user=request.user)
    if profile.shops.filter(name=name).exists():
        shop = Shop.objects.get(name=name)
        form = CreateShopForm(request.POST or None, request.FILES or None, instance=shop)
        if form.is_valid():
            form.save()
            messages.success(request, ("Данные сохранены!"))
            return redirect('user', user=str(request.user))
        context = {
            'title': 'Редактирование магазина',
            'request': request,
            'form': form,
        }
        return render(request, 'create_shop.html', context)
    else:
        messages.success(request, ("Вы не можете редактировать данный магазин, так как не состоите в нем!"))
        return redirect('user', user=str(request.user))

@login_required(login_url='login')
def leave_shop(request, name):
    profile = Profile.objects.get(user=request.user)
    if profile.shops.filter(name=name).exists():
        try:
            shop = Shop.objects.get(name=name)
            profile.shops.remove(shop)
            messages.success(request, (f"Вы успешно покинули магазин {shop.name}"))
            return redirect('user', user=str(request.user))
        except:
            messages.success(request, ("Произошла ошибка!"))
            return redirect('user', user=str(request.user))
    else:
        messages.success(request, ("Вы не можете покинуть данный магазин, так как не состоите в нем!"))
        return redirect('user', user=str(request.user))

@login_required(login_url='login')
def join_shop(request):
    if request.method == "POST":
        code = request.POST.get('shop_code', 'default_code')
        if Shop.objects.filter(code=code).exists():
            profile = Profile.objects.get(user=request.user)
            if profile.shops.filter(code=code).exists():
                messages.success(request, (f"Вы уже состоите в магазине {profile.shops.get(code=code).name}"))
                return redirect('all_manufactures')
            else:
                code_shop = Shop.objects.get(code=code)
                profile.shops.add(code_shop)
                messages.success(request, (f"Вы вступили в магазин {code_shop.name}"))
                return redirect('all_manufactures')
        else:
            messages.success(request, (f"Магазина с таким кодом не существует!"))
            return redirect('all_manufactures')
    else:
        messages.success(request, ("При попытке вступления в магазин произошла ошибка!"))
        return redirect('all_manufactures')

@login_required(login_url='login')
def delete_shop(request, name):
    profile = Profile.objects.get(user=request.user)
    if profile.manufactures.filter(name=name).exists():
        try:
            Shop.objects.get(name=name).delete()
            messages.success(request, ("Магазин и все его данные были успешно удалены!"))
            return redirect('all_manufactures')
        except:
            messages.success(request, ("Произошла ошибка!"))
            return redirect('all_manufactures')
    else:
        messages.success(request, ("Вы не можете удалить данный магазин, так как не состоите в нем!"))
        return redirect('all_manufactures')