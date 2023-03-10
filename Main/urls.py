from django.urls import path
from Main.views import *

urlpatterns = [
    path('', main, name="login"),
    path('about', about, name="about"),
]