from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('login', login_user, name="login"),
    path('logout', logout_user, name="logout"),
    path('register', register_user, name="register"),
    path('change_password', PasswordsChangeView.as_view(template_name='change_password.html'), name="change_password"),
    path('delete_profile', delete_profile, name="delete_profile"),
    path('edit_user', edit_user, name="edit_user"),
    path('cart', cart, name='cart'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='password_reset/1_send_email.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset/2_email_sent.html'), name='password_reset_done'),
    path('reset_password/<uidb64>/<token>/', PasswordsResetConfirmView.as_view(template_name='password_reset/3_set_password.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/4_done.html'), name='password_reset_complete'),
    path('delete_from_cart/<int:id>', delete_from_cart, name='delete_from_cart'),
    path('add_to_cart/<int:id>', add_to_cart, name='add_to_cart'),
    path('sub_from_cart/<int:id>', sub_from_cart, name='sub_from_cart'),
]