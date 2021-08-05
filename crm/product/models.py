from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils.translation import ugettext_lazy as _


# Create your models here.


class OrganizationProduct(models.Model):
    name = models.CharField(max_length=150, verbose_name=_("نام محصولات خروجی سازمان ها"))

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("نام محصول"))
    price = models.PositiveBigIntegerField(verbose_name=_('قیمت محصول'))
    is_taxation = models.BooleanField(verbose_name=_("مالیات"), help_text=_("آیا شامل مالیات است؟"))
    pdf_catalog = models.FileField(verbose_name=_("فایل کاتالوگ pdf"), validators=[FileExtensionValidator(['pdf'])],
                                   upload_to='pdf/')
    img_catalog = models.ImageField(verbose_name=_("فایل کاتالوگ img"), upload_to='img/')
    description = models.TextField(verbose_name=_("ویژگی های دستگاه"))
    can_be_used_for = models.ManyToManyField('product.OrganizationProduct', verbose_name=_("محصولات قابل استفاده"),
                                             blank=True)

    def __str__(self):
        return self.name
