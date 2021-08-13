import weasyprint
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory, TextInput, ChoiceField
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from organization import models as org_model
from . import models, forms
from crm import settings
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string, get_template
from django.template import Context
from django.forms import inlineformset_factory, modelformset_factory

# Create your views here.


# def quote_create(request):
""" create quote model and quote item with function base"""
#     """ create quote with quote item"""
#     list_organization = org_model.Organization.objects.filter(user=request.user)
#     QuoteFormSet = inlineformset_factory(models.Quote, models.QuoteItem, fields=('product', 'qty', 'discount'), extra=1,
#                                          widgets={
#                                              'qty': TextInput(attrs={'required': 'true'}),
#                                              'discount': TextInput(attrs={'required': 'true'})})
#     formset = QuoteFormSet()
#
#     form_instance = forms.QuoteItemForm()
#
#     if request.method == "POST":
#         formset = QuoteFormSet(data=request.POST)
#         organization = org_model.Organization.objects.get(pk=request.POST['organization'])
#
#         create_quote_instance = models.Quote.objects.create(user=request.user, organization=organization)
#
#         if formset.is_valid():
#             formset.save(commit=False)
#             for form in formset:
#                 if form.has_changed():
#                     form.instance.quote = create_quote_instance
#                     form.instance.price = form.instance.product.price
#                     form.save()
#         return redirect('sale:create-quote')
#
#     return render(request, template_name='sale/quote_create.html',
#                   context={'oragn': list_organization, 'formset': formset, 'form': form_instance})


# <----------------------------------------------------------------------------->
""" quote model view """


class QuoteCreateView(LoginRequiredMixin, CreateView):
    """ create quote model and quote item with class based view"""
    model = models.Quote
    form_class = forms.QuoteForm
    template_name = 'sale/quote_create.html'

    def get_success_url(self):
        return reverse_lazy('sale:list-quote')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            # create formset with instance
            context['formset'] = forms.QuoteItemFormSet(self.request.POST)
        else:
            # create formset for template
            context['formset'] = forms.QuoteItemFormSet()
        return context

    def form_valid(self, form):
        # add user in quote instance
        form.instance.user = self.request.user
        # get formset with instance
        context = self.get_context_data(form=form)
        formset = context['formset']
        # check valid for formset
        if formset.is_valid():
            # save quote instance for use instance in formset
            response = super().form_valid(form)
            for instance_form in formset:
                # check which row add
                if instance_form.has_changed():
                    # give price from product
                    instance_form.instance.price = instance_form.instance.product.price
            formset.instance = self.object
            formset.save()
            return response
        else:
            return super().form_invalid(form)


class QuoteUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Quote
    form_class = forms.QuoteForm
    template_name = 'sale/quote_create.html'

    def get_success_url(self):
        return reverse_lazy('sale:list-quote')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = forms.QuoteItemFormSet(self.request.POST, instance=self.object)
            context['formset'].full_clean()
        else:
            context['formset'] = forms.QuoteItemFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context['formset']
        for forminstance in formset:
            if forminstance.has_changed():
                forminstance.instance.price = forminstance.instance.product.price
        formset.save()
        return super().form_valid(form)


class QuoteListView(LoginRequiredMixin, ListView):
    """ list quote """
    model = models.Quote
    context_object_name = 'object'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.GET.get('name', None)
        if search:
            qs = qs.filter(organization__company_name__contains=search)
        return qs


class QuoteDetailView(LoginRequiredMixin, DetailView):
    model = models.Quote


class QuoteDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Quote

    def get_success_url(self):
        return reverse_lazy('sale:list-quote')


class PrintQuoteDetailView(LoginRequiredMixin, DetailView):
    """ create pdf of quote"""
    model = models.Quote
    template_name = 'sale/quote_pdf.html'

    def get(self, request, *args, **kwargs):
        get_html = super().get(request, *args, **kwargs)
        rendered_content = get_html.rendered_content
        pdf = weasyprint.HTML(string=rendered_content).write_pdf()
        response = HttpResponse(pdf, content_type='application/pdf')
        return response


@require_http_methods(["GET"])
@login_required
def send_email_view(request, pk):
    """ send quote email """
    quote = models.Quote.objects.get(pk=pk, user=request.user)
    # check quote owner send email
    if quote:
        body = render_to_string(template_name='sale/quote_email.html', context={'object': quote})
        email = quote.organization.email
        sender = request.user.username
        try:
            send_mail(_('فاکتور سفارش شما'), body, settings.EMAIL_HOST_USER, [email], fail_silently=False)
            models.EmailHistory.objects.create(creator=get_user_model().objects.get(username=sender), email=email,
                                               success=True)
            messages.success(request, _('ایمل با موفقیت ارسال شد'))
        except:
            models.EmailHistory.objects.create(creator=get_user_model().objects.get(username=sender), email=email,
                                               success=False)
            messages.success(request, _('ارسال ایمل با خطا مواجه شد'))
        return redirect(reverse_lazy('sale:list-quote'))
    else:
        messages.error(request, _('Permission denied.'))
        return redirect(reverse_lazy('sale:list-quote'))
