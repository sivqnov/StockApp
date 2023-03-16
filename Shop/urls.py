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
    path('order/', order, name='order'),
    # path('create_item/<str:name>', create_product, name="create_product"),
    # path('delete_item/<int:id>', delete_product, name='delete_product'),
    # path('edit_item/<int:id>', edit_product, name='edit_product'),
    # path('view_item/<int:id>', view_product, name='view_product'),
]