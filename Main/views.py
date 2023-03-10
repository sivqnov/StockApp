from django.shortcuts import render

# Create your views here.

def main(request):
    context = {
        'request': request,
        'title': 'Главная',
    }
    return render(request, 'main.html', context)

def about(request):
    context = {
        'request': request,
        'title': 'О сайте',
    }
    return render(request, 'about.html', context)