from django import forms
from . import models


class QuoteForm(forms.ModelForm):
    class Meta:
        model = models.Quote
        fields = ('organization',)


class QuoteUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Quote
        fields = '__all__'


class QuoteItemForm(forms.ModelForm):
    class Meta:
        model = models.QuoteItem
        exclude = ['quote', 'price']


QuoteItemFormSet = forms.inlineformset_factory(models.Quote, models.QuoteItem,
                                               fields=['product', 'qty', 'discount'],
                                               exclude=[], can_delete=True, )
