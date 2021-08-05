from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models, forms

# Create your views here.

# <------------------------------------------------------------------------------------>
""" Company Product Views """


class ProductCreateView(LoginRequiredMixin, CreateView):
    """ create Product """
    model = models.Product
    form_class = forms.ProductForm
    success_url = reverse_lazy('product:list-product')


class ProductListView(LoginRequiredMixin, ListView):
    """ list product """
    model = models.Product
    context_object_name = 'object'


# <------------------------------------------------------------------------------------>
""" Organization Product Views """


class OrganizationProductCreateView(LoginRequiredMixin, CreateView):
    """ create Organization Product """
    model = models.OrganizationProduct
    fields = '__all__'
    success_url = reverse_lazy('product:list-org-product')


class OrganizationProductListView(LoginRequiredMixin, ListView):
    """ list organization product """
    model = models.OrganizationProduct
    context_object_name = 'object'
