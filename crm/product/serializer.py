from rest_framework import serializers
from . import models


class OrganizationProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrganizationProduct
        fields = ("name",)
