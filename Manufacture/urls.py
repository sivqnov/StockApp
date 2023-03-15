from django.urls import path
from .views import *

urlpatterns = [
    path('delete_manufacture/<str:name>', delete_manufacture, name='delete_manufacture'),
    path('leave_manufacture/<str:name>', leave_manufacture, name='leave_manufacture'),
    path('create_manufacture', create_manufacture, name="create_manufacture"),
    path('edit_manufacture/<str:name>', edit_manufacture, name="edit_manufacture"),
    path('join_manufacture/', join_manufacture, name="join_manufacture"),
    path('all', all_manufactures, name="all_manufactures"),
    path('<str:name>', view_manufacture, name='view_manufacture'),
    path('create_item/<str:name>', create_item, name="create_item"),
    path('delete_item/<int:id>', delete_item, name='delete_item'),
    path('edit_item/<int:id>', edit_item, name='edit_item'),
    path('view_item/<int:id>', view_item, name='view_item'),
]