from django import forms
from . import models


class ProductForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = '__all__'


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = ('name', 'price', 'is_taxation', 'can_be_used_for')
