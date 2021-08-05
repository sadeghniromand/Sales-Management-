from rest_framework import serializers
from . import models


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.QuoteItem
        fields = ['quote', 'product', 'qty', 'discount', 'price']
        read_only_fields = ['quote', 'product', 'price']
