from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CreateManufactureForm, CreateCatalogItemForm
from django.contrib.auth.models import User
from .models import Manufacture, CatalogItem
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
def create_manufacture(request):
    form = CreateManufactureForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        manufacture = Manufacture.objects.get(name=form.cleaned_data['name'])
        code = generate_code()
        manufacture.code = code
        manufacture.save()
        user = User.objects.get(username=str(request.user))
        Profile.objects.get(user=user).manufactures.add(manufacture)
        messages.success(request, ("Предприятие успешно создано и добавлено к вам в профиль!"))
        return redirect('all_manufactures')
    context = {
        'title': 'Создание предприятия',
        'request': request,
        'form': form,
    }
    return render(request, 'create_manufacture.html', context)

@login_required(login_url='login')
def edit_manufacture(request, name):
    profile = Profile.objects.get(user=request.user)
    if profile.manufactures.filter(name=name).exists():
        manufacture = Manufacture.objects.get(name=name)
        form = CreateManufactureForm(request.POST or None, request.FILES or None, instance=manufacture)
        if form.is_valid():
            form.save()
            messages.success(request, ("Данные сохранены!"))
            return redirect('all_manufactures')
        context = {
            'title': 'Редактирование предприятия',
            'request': request,
            'form': form,
        }
        return render(request, 'create_manufacture.html', context)
    else:
        messages.success(request, ("Вы не можете редактировать данное предприятие, так как не состоите в нем!"))
        return redirect('all_manufactures')

@login_required(login_url='login')
def delete_manufacture(request, name):
    profile = Profile.objects.get(user=request.user)
    if profile.manufactures.filter(name=name).exists():
        try:
            Manufacture.objects.get(name=name).delete()
            messages.success(request, ("Предприятие и все его данные были успешно удалены!"))
            return redirect('all_manufactures')
        except:
            messages.success(request, ("Произошла ошибка!"))
            return redirect('all_manufactures')
    else:
        messages.success(request, ("Вы не можете удалить данное предприятие, так как не состоите в нем!"))
        return redirect('all_manufactures')

@login_required(login_url='login')
def leave_manufacture(request, name):
    profile = Profile.objects.get(user=request.user)
    if profile.manufactures.filter(name=name).exists():
        try:
            manufacture = Manufacture.objects.get(name=name)
            profile.manufactures.remove(manufacture)
            messages.success(request, (f"Вы успешно покинули предприятие {manufacture.name}"))
            return redirect('all_manufactures')
        except:
            messages.success(request, ("Произошла ошибка!"))
            return redirect('all_manufactures')
    else:
        messages.success(request, ("Вы не можете покинуть данное предприятие, так как не состоите в нем!"))
        return redirect('all_manufactures')

@login_required(login_url='login')
def join_manufacture(request):
    if request.method == "POST":
        code = request.POST.get('manufacture_code', 'default_code')
        if Manufacture.objects.filter(code=code).exists():
            profile = Profile.objects.get(user=request.user)
            if profile.manufactures.filter(code=code).exists():
                messages.success(request, (f"Вы уже состоите в предприятии {profile.manufactures.get(code=code).name}"))
                return redirect('all_manufactures')
            else:
                code_manufacture = Manufacture.objects.get(code=code)
                profile.manufactures.add(code_manufacture)
                messages.success(request, (f"Вы вступили в предприятие {code_manufacture.name}"))
                return redirect('all_manufactures')
        else:
            messages.success(request, (f"Предприятия с таким кодом не существует!"))
            return redirect('all_manufactures')
    else:
        messages.success(request, ("При попытке вступления в предприятие произошла ошибка!"))
        return redirect('all_manufactures')

@login_required(login_url='login')
def all_manufactures(request):
    mine = Profile.objects.get(user=request.user).manufactures
    manufactures = []
    for item in Manufacture.objects.all():
        if not mine.filter(id=item.id).exists():
            manufactures.append(item)
    context = {
        'title': 'Все предприятия',
        'request': request,
        'profile': Profile.objects.get(user=request.user),
        'mine': mine,
        'manufactures': manufactures,
        'l': len(mine.all()) + len(manufactures),
    }
    return render(request, 'all.html', context)

@login_required(login_url='login')
def view_manufacture(request, name):
    try:
        profile = Profile.objects.get(user=request.user)
        is_mine = profile.manufactures.filter(name=name).exists()
        manufacture = Manufacture.objects.get(name=name)
        members = Profile.objects.filter(manufactures__id=manufacture.id)
        catalog_items = CatalogItem.objects.filter(manufacturer_id=manufacture.id)
        context = {
            'title': manufacture.name,
            'request': request,
            'profile': Profile.objects.get(user=request.user),
            'manufacture': manufacture,
            'members': members,
            'catalog_items': catalog_items,
            'is_mine': is_mine,
        }
        return render(request, 'view_manufacture.html', context)
    except:
        messages.success(request, ("Предприятия с таким именем не существует!"))
        return redirect('all_manufactures')

# Catalog Item

@login_required(login_url='login')
def create_item(request, name):
    profile = Profile.objects.get(user=request.user)
    if profile.manufactures.filter(name=name).exists():
        form = CreateCatalogItemForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            manufacture = Manufacture.objects.get(name=name)
            item_name = form.cleaned_data['name']
            catalog_item = CatalogItem.objects.get(name=item_name)
            catalog_item.manufacturer = manufacture
            catalog_item.save()
            messages.success(request, ("Товар каталога успешно создан!"))
            return redirect('view_manufacture', name=manufacture.name)
        context = {
            'title': 'Создание товара каталога',
            'request': request,
            'form': form,
        }
        return render(request, 'create_item.html', context)
    else:
        messages.success(request, ("Вы не можете создать товар для данного предприятия, так как не состоите в нем!"))
        return redirect('all_manufactures')

@login_required(login_url='login')
def delete_item(request, id):
    profile = Profile.objects.get(user=request.user)
    item = CatalogItem.objects.get(id=id)
    if profile.manufactures.filter(name=item.manufacturer.name).exists():
        try:
            item.delete()
            messages.success(request, ("Товар и все его данные были успешно удалены!"))
            return redirect('view_manufacture', name=item.manufacturer.name)
        except:
            messages.success(request, ("Произошла ошибка!"))
            return redirect('view_manufacture', name=item.manufacturer.name)
    else:
        messages.success(request, ("Вы не можете удалить данный товар, так как не состоите в предприятии, которому он принадлежит!"))
        return redirect('view_manufacture', name=item.manufacturer.name)

@login_required(login_url='login')
def edit_item(request, id):
    profile = Profile.objects.get(user=request.user)
    item = CatalogItem.objects.get(id=id)
    if profile.manufactures.filter(name=item.manufacturer.name).exists():
        form = CreateCatalogItemForm(request.POST or None, request.FILES or None, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, ("Изменения сохранены!"))
            return redirect('view_manufacture', name=item.manufacturer.name)
        context = {
            'title': 'Создание товара каталога',
            'request': request,
            'form': form,
        }
        return render(request, 'create_item.html', context)
    else:
        messages.success(request, ("Вы не можете редактировать данный товар, так как не состоите в предприятии, которому он принадлежит!"))
        return redirect('view_manufacture', name=item.manufacturer.name)

@login_required(login_url='login')
def view_item(request, id):
    try:
        profile = Profile.objects.get(user=request.user)
        item = CatalogItem.objects.get(id=id)
        context = {
            'title': item.name,
            'request': request,
            'profile': profile,
            'item': item,
            'is_mine': True if profile.manufactures.filter(id=item.manufacturer.id).exists() else False,
        }
        return render(request, 'view_item.html', context)
    except:
        messages.success(request, ("Предприятия с таким именем не существует!"))
        return redirect('all_manufactures')