from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CreateManufactureForm
from django.contrib.auth.models import User
from .models import Manufacture
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
        print(f'\n\n\n{code}\n\n\n')
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

@login_required(login_url='login')
def delete_manufacture(request, name):
    try:
        manufacture = Manufacture.objects.get(name=name).delete()
        messages.success(request, ("Предприятие и все его данные были успешно удалены!"))
        return redirect('all_manufactures')
    except:
        messages.success(request, ("Произошла ошибка!"))
        return redirect('all_manufactures')

@login_required(login_url='login')
def leave_manufacture(request, name):
    try:
        manufacture = Manufacture.objects.get(name=name)
        profile = Profile.objects.get(user=User.objects.get(username=str(request.user)))
        profile.manufactures.remove(manufacture)
        messages.success(request, (f"Вы успешно покинули предприятие {manufacture.name}"))
        return redirect('all_manufactures')
    except:
        messages.success(request, ("Произошла ошибка!"))
        return redirect('all_manufactures')

@login_required(login_url='login')
def join_manufacture(request):
    if request.method == "POST":
        code = request.POST.get('manufacture_code', 'default_code')
        if Manufacture.objects.filter(code=code).exists():
            profile = Profile.objects.get(user=User.objects.get(username=str(request.user)))
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
        # if commentObj.likes.filter(user=User.objects.get(username=currentUser)).exists():
        
    else:
        messages.success(request, ("Ошибка:((("))
        return redirect('all_manufactures')

@login_required(login_url='login')
def all_manufactures(request):
    context = {
        'title': 'Все предприятия',
        'request': request,
        'profile': Profile.objects.get(user=request.user),
    }
    return render(request, 'all.html', context)

@login_required(login_url='login')
def view_manufacture(request, name):
    try:
        profile = Profile.objects.get(user=request.user)
        if profile.manufactures.filter(name=name).exists():
            manufacture = Manufacture.objects.get(name=name)
            members = Profile.objects.filter(manufactures__id=manufacture.id)
            context = {
                'title': manufacture.name,
                'request': request,
                'profile': Profile.objects.get(user=request.user),
                'manufacture': manufacture,
                'members': members,
            }
            return render(request, 'view_manufacture.html', context)
        else:
            messages.success(request, ("Вы не состоите в этом предприятии"))
            return redirect('all_manufactures')
    except:
        messages.success(request, ("Предприятия с таким именем не существует!"))
        return redirect('all_manufactures')