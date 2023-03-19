from django import template
from Members.models import Profile
from django.contrib.auth.models import User

register = template.Library()

@register.inclusion_tag('modules/nav_profile.html')
def nav_profile(request):
    if request.user.is_authenticated:
        userobj = User.objects.get(username=request.user)
        profile = Profile.objects.get(user=userobj)
        context = {
            "request": request,
            "profile": profile,
        }
    else:
        context = {
            "request": request,
        }
    return context

@register.simple_tag()
def cart_items(request):
    return Profile.objects.get(user=request.user).cart.count()