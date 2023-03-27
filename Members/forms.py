from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile

class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=70, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs={'class': 'form-control form-control-lg', 'type': 'text', 'id': 'typeLoginX'}
        self.fields['first_name'].widget.attrs={'class': 'form-control form-control-lg', 'type': 'text', 'id': 'typeNameX'}
        self.fields['last_name'].widget.attrs={'class': 'form-control form-control-lg', 'type': 'text', 'id': 'typeSurnameX'}
        self.fields['email'].widget.attrs={'class': 'form-control form-control-lg', 'type': 'email', 'id': 'typeEmailX'}
        self.fields['password1'].widget.attrs={'class': 'form-control form-control-lg passwordInput', 'type': 'password', 'id': 'typePassword1X'}
        self.fields['password2'].widget.attrs={'class': 'form-control form-control-lg passwordInput', 'type': 'password', 'id': 'typePassword2X'}

class RegisterProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio',)
    
    def __init__(self, *args, **kwargs):
        super(RegisterProfileForm, self).__init__(*args, **kwargs)

        # self.fields['bio'].label = 'О себе'
        self.fields['bio'].widget.attrs={'class': 'form-control form-control-lg', 'id': 'typeLoginX', 'type': 'text'}
    
class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control passwordInput', 'type': 'password'}))
    new_password1 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control passwordInput', 'type': 'password'}))
    new_password2 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control passwordInput', 'type': 'password'}))

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')
    
    def __init__(self, *args, **kwargs):
        super(PasswordChangingForm, self).__init__(*args, **kwargs)

        self.fields['old_password'].label = 'Старый пароль'
        self.fields['new_password1'].label = 'Новый пароль'
        self.fields['new_password2'].label = 'Подтвердите новый пароль'

class SettingPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control passwordInput', 'type': 'password'}))
    new_password2 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control passwordInput', 'type': 'password'}))

    class Meta:
        model = User
        fields = ('new_password1', 'new_password2')
    
    def __init__(self, *args, **kwargs):
        super(SettingPasswordForm, self).__init__(*args, **kwargs)

        self.fields['new_password1'].label = 'Новый пароль'
        self.fields['new_password2'].label = 'Подтвердите новый пароль'

class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=70, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs={'class': 'form-control form-control-lg', 'type': 'text', 'id': 'typeLoginX'}
        self.fields['first_name'].widget.attrs={'class': 'form-control form-control-lg', 'type': 'text', 'id': 'typeNameX'}
        self.fields['last_name'].widget.attrs={'class': 'form-control form-control-lg', 'type': 'text', 'id': 'typeSurnameX'}
        self.fields['email'].widget.attrs={'class': 'form-control form-control-lg', 'type': 'email', 'id': 'typeEmailX'}

class AvatarFileUploadInput(forms.ClearableFileInput):
    input_type = 'file'
    template_name = "widgets/image_upload_input.html"

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'photo')
        widgets = {"photo": AvatarFileUploadInput } # https://www.advantch.com/blog/how-to-create-custom-form-widgets-with-django-alpinejs-and-tailwindcss/
    
    def __init__(self, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)

        self.fields['bio'].widget.attrs={'class': 'form-control form-control-lg', 'id': 'typeLoginX', 'type': 'text', 'style': 'min-height: 42px;',}
        self.fields['photo'].widget.attrs={'class': 'form-control form-control'}