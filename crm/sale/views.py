import weasyprint
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, DetailView
from organization import models as org_model
from . import models, forms
from crm import settings
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.forms import inlineformset_factory, modelformset_factory


# Create your views here.


def quote_create(request):
    list_organization = org_model.Organization.objects.filter(user=request.user)
    QuoteFormSet = inlineformset_factory(models.Quote, models.QuoteItem, fields=('product', 'qty', 'discount'),
                                         max_num=1)
    formset = QuoteFormSet()

    form_instance = forms.QuoteItemForm()

    if request.method == "POST":
        organization = org_model.Organization.objects.get(pk=request.POST['organization'])
        create_quote_instance = models.Quote.objects.create(user=request.user, organization=organization)
        formset = QuoteFormSet(data=request.POST)
        # for form in formset:
            # models.QuoteItem.objects.create(
            #     quote=create_quote_instance,
            #     product=form.cleaned_data['product'],
            #     qty=form.cleaned_data['qty'],
            #     discount=form.cleaned_data['discount'],
            #     price=form.cleaned_data['product'].price
            # )
            # a = 2
            # price = form.instance.product
            # form.instance.quote = create_quote_instance
            # form.instance.price = price.price
            # form.save()

        quote_item_instance = forms.QuoteItemForm(data=request.POST)
        organization = org_model.Organization.objects.get(pk=request.POST.get('organization'))
        quote_instance = models.Quote.objects.create(user=request.user, organization=organization)
        models.QuoteItem.objects.create(
            quote=quote_instance,
            product=quote_item_instance.cleaned_data["product"],
            qty=quote_item_instance.cleaned_data['qty'],
            discount=quote_item_instance.cleaned_data['discount'],
            price=quote_item_instance.cleaned_data["product"].price
        )
        return redirect('sale:create-quote')

    return render(request, template_name='sale/quote_create.html',
                  context={'oragn': list_organization, 'formset': formset, 'form': form_instance})


class QuoteListView(LoginRequiredMixin, ListView):
    model = models.Quote
    context_object_name = 'object'

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.GET.get('name', None)
        if search:
            qs = qs.filter(organization__name__contains=search)
        return qs


class QuoteDetailView(LoginRequiredMixin, DetailView):
    model = models.Quote


class PrintQuoteDetailView(LoginRequiredMixin, DetailView):
    model = models.Quote

    def get(self, request, *args, **kwargs):
        get_html = super().get(request, *args, **kwargs)
        rendered_content = get_html.rendered_content
        pdf = weasyprint.HTML(string=rendered_content).write_pdf()
        response = HttpResponse(pdf, content_type='application/pdf')
        return response


def send_email(body, sender, email):
    """
    task for send email
    """
    try:
        send_mail(_('فاکتور سفارش شما'), body, settings.EMAIL_HOST_USER, [email], fail_silently=False)
        models.EmailHistory.objects.create(creator=get_user_model().objects.get(username=sender), email=email,
                                           success=True)
        return 'Email send successfully.'
    except:
        models.EmailHistory.objects.create(creator=get_user_model().objects.get(username=sender), email=email,
                                           success=False)
        return 'Email send failed.'


@require_http_methods(["GET"])
@login_required
def send_email_view(request, pk):
    quote = models.Quote.objects.get(pk=pk, user=request.user)
    if quote:
        body = render_to_string('sale/email_quote.txt', {'object': quote})
        # body = 'test'
        email = quote.organization.email
        sender = request.user.username
        send_email(body, sender, email)
        messages.success(request, _('Send email request saved successfully.'))
        return redirect(reverse_lazy('sale:list-quote'))
    else:
        messages.error(request, _('Permission denied.'))
        return redirect(reverse_lazy('sale:list-quote'))


