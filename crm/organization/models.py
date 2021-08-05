from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator, FileExtensionValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from .enums import StatusFollowUp

# Create your models here.


mobile_phone_regex = RegexValidator(regex='^09[0-9]{9}$',
                                    message="شماره موبایل باید یازده رقم باشد.مثال:09999999999")

company_phone_regex = RegexValidator(regex='^0[1-9]{2}[1-9][0-9]{7}$',
                                     message=_('تلفن باید باکد استان باشد.مثال:08622222222'))


class Organization(models.Model):
    company_name = models.CharField(max_length=150, verbose_name=_('نام شرکت'))
    company_phone = models.CharField(validators=[company_phone_regex], max_length=11, verbose_name=_("تلفن شرکت"))
    number_of_worker = models.IntegerField(verbose_name=_("تعداد کارگر"), )
    product = models.ManyToManyField('product.OrganizationProduct', verbose_name=_("محصولات تولیدی"), )
    province = models.CharField(max_length=100, verbose_name=_("استان"))
    company_address = models.TextField(verbose_name=_("ادرس شرکت"))

    name = models.CharField(max_length=100, verbose_name=_('نام و نام خانوادگی'))
    mobile_phone = models.CharField(validators=[mobile_phone_regex], max_length=11, verbose_name=_("شماره موبایل"))
    email = models.EmailField(verbose_name=_("پست الکترونیک"))

    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, verbose_name=_("کاربر ثبت کننده"), )
    company_registration_date = models.DateTimeField(auto_now_add=True, verbose_name=_("تاریخ ثبت شرکت"))

    def __str__(self):
        return f'company {self.company_name}'


class FollowUp(models.Model):
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, verbose_name=_('کاربر ثبت کننده'))
    date = models.DateField(auto_now_add=True, verbose_name=_('تاریخ شروع گزارش کار'))
    last_data = models.DateField(auto_now=True, verbose_name=_(' تاریخ اخرین تغییرات'))
    title = models.CharField(max_length=150, verbose_name=_('موضوع گزارش کار'))
    status = models.CharField(max_length=5, choices=StatusFollowUp.choices, default=StatusFollowUp.start,
                              verbose_name=_('وضعیت پیگیری'))
    description = models.TextField(verbose_name=_('گزارش کار'))
