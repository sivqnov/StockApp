from django import forms
from .models import Manufacture, CatalogItem

class CreateManufactureForm(forms.ModelForm):
    class Meta:
        model = Manufacture
        fields = ('name', 'bio', 'photo')
    
    def __init__(self, *args, **kwargs):
        super(CreateManufactureForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs={'class': 'form-control form-control-lg', 'id': 'typeNameX', 'type': 'text'}
        self.fields['bio'].widget.attrs={'class': 'form-control form-control-lg', 'id': 'typeBioX', 'type': 'text'}
        self.fields['photo'].widget.attrs={'class': 'form-control form-control-lg'}

class CreateCatalogItemForm(forms.ModelForm):
    class Meta:
        model = CatalogItem
        fields = ('name', 'bio', 'code', 'photo', 'date_of_manufacture', 'expiration_date', 'price')
        widgets = {
            'date_of_manufacture': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control', 
                    'placeholder': 'Select a date',
                    'type': 'date'
                    }),
            'expiration_date': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control', 
                    'placeholder': 'Select a date',
                    'type': 'date'
                    }),
        }
    
    def __init__(self, *args, **kwargs):
        super(CreateCatalogItemForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs={'class': 'form-control form-control-lg', 'id': 'typeNameX', 'type': 'text'}
        self.fields['bio'].widget.attrs={'class': 'form-control form-control-lg', 'id': 'typeBioX', 'type': 'text'}
        self.fields['code'].widget.attrs={'class': 'form-control form-control-lg', 'id': 'typeCodeX', 'maxlength': '13'}
        self.fields['photo'].widget.attrs={'class': 'form-control form-control-lg'}
        self.fields['date_of_manufacture'].widget.attrs={'class': 'form-control form-control-lg form-icon-trailing', 'id': 'typeDateX'}
        self.fields['expiration_date'].widget.attrs={'class': 'form-control form-control-lg form-icon-trailing', 'id': 'typeExpX', 'type': 'date'}
        self.fields['price'].widget.attrs={'class': 'form-control form-control-lg', 'id': 'typePriceX', 'step': '0.01'}

# manufacturer = models.ForeignKey('Manufacture', on_delete=models.CASCADE, blank=False, null=True, verbose_name='Производитель')
# name = models.CharField(max_length = 150, verbose_name='Название')
# bio = models.TextField(blank=True, verbose_name='О предприятии')
# code = models.CharField(max_length = 13, verbose_name='Код товара')
# photo = models.ImageField(upload_to = 'catalog_items/%Y/%m/%d/', blank=True, verbose_name='Фото')
# date_of_manufacture = models.DateField(verbose_name='Дата производства')
# expiration_date = models.DateField(verbose_name='Годен до')
# price = models.FloatField(validators=[MinValueValidator(1)], verbose_name='Цена')