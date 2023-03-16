from django import forms
from .models import Shop, Product

class DateInput(forms.DateInput):
    input_type = 'date'

class CreateShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ('name', 'bio', 'photo')
    
    def __init__(self, *args, **kwargs):
        super(CreateShopForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs={'class': 'form-control form-control-lg', 'id': 'typeNameX', 'type': 'text'}
        self.fields['bio'].widget.attrs={'class': 'form-control form-control-lg', 'id': 'typeBioX', 'type': 'text'}
        self.fields['photo'].widget.attrs={'class': 'form-control form-control-lg'}

class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('amount', 'price')
    
    def __init__(self, *args, **kwargs):
        super(CreateProductForm, self).__init__(*args, **kwargs)

        self.fields['amount'].widget.attrs={'class': 'form-control form-control-lg', 'id': 'typeAmountX', 'step': '1'}
        self.fields['price'].widget.attrs={'class': 'form-control form-control-lg', 'id': 'typePriceX', 'step': '0.01'}