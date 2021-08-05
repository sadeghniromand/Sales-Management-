from django import forms
from . import models


class QuoteForm(forms.ModelForm):
    class Meta:
        model = models.Quote
        fields = ('organization',)


class QuoteItemForm(forms.ModelForm):
    class Meta:
        model = models.QuoteItem
        exclude = ['quote', 'price']
