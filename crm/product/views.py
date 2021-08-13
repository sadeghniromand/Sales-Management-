from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models, forms, serializer
from rest_framework import viewsets

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


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = models.Product


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Product
    form_class = forms.ProductUpdateForm

    def get_success_url(self):
        return reverse('product:detail-product', kwargs={'pk': self.kwargs['pk']})


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


# <------------------------------------------------------------------------------->
""" API View """


class OrganizationProductAPIView(viewsets.ModelViewSet):
    queryset = models.OrganizationProduct.objects.all()
    serializer_class = serializer.OrganizationProductSerializer

