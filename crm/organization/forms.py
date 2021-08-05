from django import forms
from . import models


class OrganizationForm(forms.ModelForm):
    """ organization form """

    class Meta:
        model = models.Organization
        exclude = ['user', 'company_registration_date', 'follow_up']
        

class FollowUpForm(forms.ModelForm):
    class Meta:
        model = models.FollowUp
        exclude = ['user', 'organization']
