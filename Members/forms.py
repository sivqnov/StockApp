from django.contrib.auth.forms import UserCreationForm
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
        
        # self.fields['username'].label = 'Логин'
        # self.fields['first_name'].label = 'Имя'
        # self.fields['last_name'].label = 'Фамилия'
        # self.fields['email'].label = 'Почта'

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