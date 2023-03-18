from django import template
from Members.models import Profile
from django.contrib.auth.models import User

register = template.Library()

@register.inclusion_tag('modules/price.html')
def price(item):
    context = {
        'manufacture_price': item.item.price,
        'shop_price': item.price,
        'price_difference': round(item.price - item.item.price, 2),
        'markup': round(((item.price-item.item.price)/item.item.price)*100, 2),
        'total_manufacture': round(item.item.price * item.amount, 2),
        'total_shop': round(item.price * item.amount, 2),
        'total_difference': round((item.price * item.amount) - (item.item.price * item.amount), 2),
    }
    return context