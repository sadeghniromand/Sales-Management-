from django.shortcuts import render
from . import models, forms
# Create your views here.
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse

# <------------------------------------------------------------------->
""" Organization Views """


class OrganizationCreateView(LoginRequiredMixin, CreateView):
    """ create organization """
    model = models.Organization
    form_class = forms.OrganizationForm

    def get_success_url(self):
        return reverse_lazy('organization:list-organ')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form=form)


class OrganizationListView(LoginRequiredMixin, ListView):
    """ list organization """
    model = models.Organization
    context_object_name = 'object'


class OrganizationDetailView(LoginRequiredMixin, DetailView):
    model = models.Organization

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        list_name = []
        qs_organization_product = context['object'].product.all()
        for organization_product in qs_organization_product:
            qs_related_product = organization_product.product_set.all()
            for product in qs_related_product:
                list_name.append(product.name)
        # remove repeated name
        list_name = set(list_name)
        context['product'] = list_name
        return context


class OrganizationUpdateView(LoginRequiredMixin, UpdateView):
    """ change single organization object """

    model = models.Organization
    form_class = forms.OrganizationForm

    def get_success_url(self):
        return reverse('organization:detail-organ', kwargs={'pk': self.kwargs["pk"]})


# <---------------------------------------------------------------------------------------->
""" Follow Up Views"""


class FollowUpCreateView(LoginRequiredMixin, CreateView):
    """ create follow up """
    model = models.FollowUp
    form_class = forms.FollowUpForm

    def get_success_url(self):
        return reverse('organization:detail-organ', kwargs={'pk': self.kwargs["pk"]})

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.organization = models.Organization.objects.filter(pk=self.kwargs["pk"])[0]
        return super().form_valid(form)


class FollowUpUpdateView(LoginRequiredMixin, UpdateView):
    """ change single follow up object """

    model = models.FollowUp
    form_class = forms.FollowUpForm

    def get_success_url(self):
        return reverse_lazy('organization:update-followup', kwargs={'pk': self.kwargs["pk"]})


def home(request):
    return render(request, template_name='bases/base.html')
