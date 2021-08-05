from django.contrib import admin
from . import models
# Register your models here.


@admin.register(models.Organization)
class OrganizationAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        return False


@admin.register(models.FollowUp)
class FollowUpAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        return False
