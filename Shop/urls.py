from django.urls import path
from .views import *

urlpatterns = [
    path('delete_shop/<str:name>', delete_shop, name='delete_shop'),
    path('leave_shop/<str:name>', leave_shop, name='leave_shop'),
    path('create_shop', create_shop, name="create_shop"),
    path('edit_shop/<str:name>', edit_shop, name="edit_shop"),
    path('join_shop/', join_shop, name="join_shop"),
    path('all', all_shops, name="all_shops"),
    path('<str:name>', view_shop, name='view_shop'),
    path('order/<str:item>', order, name='order'),
    path('edit_product/<int:id>', edit_product, name='edit_product'),
    path('delete_product/<int:id>', delete_product, name='delete_product'),
    path('add_to_product/<int:id>', add_to_product, name='add_to_product'),
    path('sub_from_product/<int:id>', sub_from_product, name='sub_from_product'),
    path('view_product/<int:id>', view_product, name='view_product'),
    path('to_basket/<int:id>', to_basket, name='to_basket'),
]