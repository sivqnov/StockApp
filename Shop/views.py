from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CreateShopForm, CreateProductForm
from django.contrib.auth.models import User
from .models import Shop, Product
from Members.models import Profile
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from random import randint
from Manufacture.models import Manufacture, CatalogItem
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
        messages.success(request, ("Магазин успешно создан и добавлен к вам в профиль"))
        return redirect('all_shops')
    context = {
        'title': 'Создание магазина',
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
            messages.success(request, ("Данные сохранены"))
            return redirect('all_shops')
        context = {
            'title': 'Редактирование магазина',
            'request': request,
            'form': form,
        }
        return render(request, 'create_shop.html', context)
    else:
        messages.success(request, ("Вы не можете редактировать данный магазин, так как не состоите в нем"))
        return redirect('all_shops')

@login_required(login_url='login')
def leave_shop(request, name):
    profile = Profile.objects.get(user=request.user)
    if profile.shops.filter(name=name).exists():
        try:
            shop = Shop.objects.get(name=name)
            profile.shops.remove(shop)
            messages.success(request, (f"Вы успешно покинули магазин {shop.name}"))
            return redirect('all_shops')
        except:
            messages.success(request, ("Произошла ошибка!"))
            return redirect('all_shops')
    else:
        messages.success(request, ("Вы не можете покинуть данный магазин, так как не состоите в нем"))
        return redirect('all_shops')

@login_required(login_url='login')
def join_shop(request):
    if request.method == "POST":
        code = request.POST.get('shop_code', 'default_code')
        if Shop.objects.filter(code=code).exists():
            profile = Profile.objects.get(user=request.user)
            if profile.shops.filter(code=code).exists():
                messages.success(request, (f"Вы уже состоите в магазине {profile.shops.get(code=code).name}"))
                return redirect('all_shops')
            else:
                code_shop = Shop.objects.get(code=code)
                profile.shops.add(code_shop)
                messages.success(request, (f"Вы вступили в магазин {code_shop.name}"))
                return redirect('all_shops')
        else:
            messages.success(request, (f"Магазина с таким кодом не существует"))
            return redirect('all_shops')
    else:
        messages.success(request, ("При попытке вступления в магазин произошла ошибка"))
        return redirect('all_shops')

@login_required(login_url='login')
def delete_shop(request, name):
    profile = Profile.objects.get(user=request.user)
    if profile.shops.filter(name=name).exists():
        try:
            Shop.objects.get(name=name).delete()
            messages.success(request, ("Магазин и все его данные были успешно удалены"))
            return redirect('all_shops')
        except:
            messages.success(request, ("Произошла ошибка"))
            return redirect('all_shops')
    else:
        messages.success(request, ("Вы не можете удалить данный магазин, так как не состоите в нем"))
        return redirect('all_shops')
    
@login_required(login_url='login')
def all_shops(request):
    mine = Profile.objects.get(user=request.user).shops
    shops = []
    for item in Shop.objects.all():
        if not mine.filter(id=item.id).exists():
            shops.append(item)
    context = {
        'title': 'Все магазины',
        'request': request,
        'profile': Profile.objects.get(user=request.user),
        'mine': mine,
        'shops': shops,
        'l': len(mine.all()) + len(shops),
    }
    return render(request, 'all_shops.html', context)

@login_required(login_url='login')
def view_shop(request, name):
    try:
        profile = Profile.objects.get(user=request.user)
        is_mine = profile.shops.filter(name=name).exists()
        shop = Shop.objects.get(name=name)
        members = Profile.objects.filter(shops__id=shop.id)
        items = Product.objects.filter(stock_id=shop.id)
        stock_sum = 0
        for item in items:
            stock_sum += item.price * item.amount
        context = {
            'title': shop.name,
            'request': request,
            'profile': Profile.objects.get(user=request.user),
            'shop': shop,
            'members': members,
            'items': items,
            'is_mine': is_mine,
            'manufactures': Manufacture.objects.all(),
            'stock_sum': stock_sum,
        }
        return render(request, 'view_shop.html', context)
    except:
        messages.success(request, ("Магазина с таким именем не существует"))
        return redirect('all_shops')

@login_required(login_url='login')
def order(request, item):
    if request.method == "POST":
        shop_str = request.POST.get('stock', 'default_stock')
        if Shop.objects.filter(name=shop_str).exists():
            profile = Profile.objects.get(user=request.user)
            if profile.shops.filter(name=shop_str).exists():
                item_str = request.POST.get('item', 'default_item')
                if CatalogItem.objects.filter(name=item_str).exists():
                    shop = Shop.objects.get(name=shop_str)
                    item = CatalogItem.objects.get(name=item_str)
                    if Product.objects.filter(item=item).filter(stock=shop).exists():
                        product = Product.objects.filter(item=item).get(stock=shop)
                        messages.success(request, (f"Вы были перенаправлены на страницу редактирования товара {item.name} магазина {shop.name}, т.к. пытались заказать товар, который уже есть на складе магазина"))
                        return redirect('edit_product', id=product.id)
                    else:
                        Product.objects.create(item=item, stock=shop, amount=int(request.POST.get('amount', '0')), price=float(request.POST.get('price', '0')))
                        messages.success(request, (f"Заказ успешно выполнен"))
                        return redirect('view_shop', name=shop.name)
                else:
                    messages.success(request, ("Товара с таким названием не существует"))
                    return redirect('all_shops')
            else:
                messages.success(request, ("Вы не можете заказать товар на склад этого магазина, так как не состоите в нем"))
                return redirect('all_shops')
        else:
            messages.success(request, ("Магазина с таким кодом не существует"))
            return redirect('all_shops')
    else:  
        try:
            context = {
            'title': item,
            'request': request,
            'profile': Profile.objects.get(user=request.user),
            'item': CatalogItem.objects.get(name=item)
            }
            return render(request, 'order.html', context)
        except:
            messages.success(request, (f"Такого товара не существует"))
            return redirect('all_shops')

@login_required(login_url='login')
def edit_product(request, id):
    profile = Profile.objects.get(user=request.user)
    if profile.shops.filter(name=Product.objects.get(id=id).stock.name).exists():
        product = Product.objects.get(id=id)
        shop = Shop.objects.get(name=product.stock.name)
        form = CreateProductForm(request.POST or None, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, ("Данные сохранены"))
            return redirect('view_shop', name=product.stock.name)
        context = {
            'title': 'Редактирование товара',
            'request': request,
            'form': form,
            'product': product,
        }
        return render(request, 'edit_product.html', context)
    else:
        messages.success(request, ("Вы не можете редактировать данный товар, так как не состоите в магазине, которому он принадлежит"))
        return redirect('view_shop', name=Product.objects.get(id=id).stock.name)

@login_required(login_url='login')
def add_to_product(request, id):
    profile = Profile.objects.get(user=request.user)
    if profile.shops.filter(name=Product.objects.get(id=id).stock.name).exists():
        product = Product.objects.get(id=id)
        product.amount += 1
        product.save()
        messages.success(request, ("Данные сохранены"))
        return redirect('view_shop', name=product.stock.name)
    else:
        messages.success(request, ("Вы не можете редактировать данный товар, так как не состоите в магазине, которому он принадлежит"))
        return redirect('view_shop', name=Product.objects.get(id=id).stock.name)

@login_required(login_url='login')
def sub_from_product(request, id):
    profile = Profile.objects.get(user=request.user)
    if profile.shops.filter(name=Product.objects.get(id=id).stock.name).exists():
        product = Product.objects.get(id=id)
        if product.amount > 1:
            product.amount -= 1
            product.save()
            messages.success(request, ("Данные сохранены"))
            return redirect('view_shop', name=product.stock.name)
        else:
            messages.success(request, (f"Товар {product.name} закончился на складе и был удален!"))
            product.delete()
            return redirect('view_shop', name=product.stock.name)
    else:
        messages.success(request, ("Вы не можете редактировать данный товар, так как не состоите в магазине, которому он принадлежит"))
        return redirect('view_shop', name=Product.objects.get(id=id).stock.name)

@login_required(login_url='login')
def delete_product(request, id):
    profile = Profile.objects.get(user=request.user)
    if profile.shops.filter(name=Product.objects.get(id=id).stock.name).exists():
        product = Product.objects.get(id=id)
        name = product.stock.name
        product.delete()
        messages.success(request, ("Товар был удален"))
        return redirect('view_shop', name=name)
    else:
        messages.success(request, ("Вы не можете удалить данный товар, так как не состоите в магазине, которому он принадлежит"))
        return redirect('view_shop', name=Product.objects.get(id=id).stock.name)

@login_required(login_url='login')
def view_product(request, id):
    try:
        profile = Profile.objects.get(user=request.user)
        item = Product.objects.get(id=id)
        context = {
            'title': item.item.name,
            'request': request,
            'profile': profile,
            'item': item,
            'is_mine': True if profile.shops.filter(id=item.stock.id).exists() else False,
        }
        return render(request, 'view_product.html', context)
    except:
        messages.success(request, ("Товара с таким именем не существует!"))
        return redirect('all_shops')