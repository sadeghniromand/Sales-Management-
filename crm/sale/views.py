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
from django.views.generic import ListView, DetailView, UpdateView
from organization import models as org_model
from . import models, forms
from crm import settings
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.forms import inlineformset_factory, modelformset_factory


# Create your views here.


def quote_create(request):
    """ create quote with quote item"""
    list_organization = org_model.Organization.objects.filter(user=request.user)
    QuoteFormSet = inlineformset_factory(models.Quote, models.QuoteItem, fields=('product', 'qty', 'discount'), )
    formset = QuoteFormSet()

    form_instance = forms.QuoteItemForm()

    if request.method == "POST":
        organization = org_model.Organization.objects.get(pk=request.POST['organization'])
        create_quote_instance = models.Quote.objects.create(user=request.user, organization=organization)
        formset = QuoteFormSet(data=request.POST)
        if formset.is_valid():
            for form in formset:
                if form.has_changed():
                    form.save(commit=False)
                    form.instance.quote = create_quote_instance
                    form.instance.price = form.instance.product.price
                    form.save()
        return redirect('sale:create-quote')

    return render(request, template_name='sale/quote_create.html',
                  context={'oragn': list_organization, 'formset': formset, 'form': form_instance})


class QuoteListView(LoginRequiredMixin, ListView):
    """ list quote """
    model = models.Quote
    context_object_name = 'object'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.GET.get('name', None)
        if search:
            qs = qs.filter(organization__name__contains=search)
        return qs


class QuoteDetailView(LoginRequiredMixin, DetailView):
    model = models.Quote


class QuoteUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Quote


class PrintQuoteDetailView(LoginRequiredMixin, DetailView):
    """ create pdf of quote"""
    model = models.Quote

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
        body = render_to_string('sale/email_quote.txt', {'object': quote})
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
