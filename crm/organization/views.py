from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied
from . import models, forms, serializer
from sale import models as sale_model
# Create your views here.
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from rest_framework import viewsets
from rest_framework import status
from rest_framework import permissions

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

    def get_queryset(self):
        qs = super().get_queryset()
        search_name = self.request.GET.get("name", None)
        if search_name:
            qs = qs.filter(company_name__contains=search_name)
        return qs


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

    def get(self, request, *args, **kwargs):
        if not models.Organization.objects.get(pk=kwargs['pk']).user == request.user:
            raise PermissionDenied
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('organization:detail-organ', kwargs={'pk': self.kwargs["pk"]})


class OrganizationQuoteListView(LoginRequiredMixin, ListView):
    model = sale_model.Quote
    context_object_name = 'object'
    paginate_by = 12
    template_name = 'organization/organization_quote_list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(organization=models.Organization.objects.get(pk=self.kwargs["pk"]))
        return qs


# <---------------------------------------------------------------------------------------->
""" Follow Up Views"""


@method_decorator(csrf_exempt, name='dispatch')
class FollowUpCreateView(LoginRequiredMixin, CreateView):
    """ create follow up """
    model = models.FollowUp
    form_class = forms.FollowUpForm

    def get_success_url(self):
        return reverse('organization:detail-organ', kwargs={'pk': self.kwargs["pk"]})

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.organization = models.Organization.objects.get(pk=self.kwargs["pk"])
        super().form_valid(form)
        return JsonResponse(data={"success": True}, status=status.HTTP_201_CREATED)

    def form_invalid(self, form):
        super().form_invalid(form)
        return JsonResponse(data={"error": False}, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class FollowUpUpdateView(LoginRequiredMixin, UpdateView):
    """ change single follow up object """

    model = models.FollowUp
    form_class = forms.FollowUpForm

    def get_success_url(self):
        return reverse_lazy('organization:update-followup', kwargs={'pk': self.kwargs["pk"]})

    def form_valid(self, form):
        super().form_valid(form)
        return JsonResponse(data={"success": True}, status=status.HTTP_202_ACCEPTED)

    def form_invalid(self, form):
        super().form_invalid(form)
        return JsonResponse(data={"success": False}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


def home(request):
    return render(request, template_name='bases/base.html')


# <----------------------------------------------------------------------->
""" API View """


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = models.Organization.objects.all()
    serializer_class = serializer.OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs
