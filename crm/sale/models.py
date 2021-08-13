from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _


# Create your models here.


class Quote(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name=_("کاربر ثبت کننده"))
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE, verbose_name=_("سازمان"))
    data = models.DateField(auto_now_add=True, verbose_name=_("تاریخ سفارش"))

    def total_all_product_price(self):
        sum = 0
        for item in self.quoteitem_set.all():
            sum += item.finished_price()
        return sum

    def formated_date(self):
        return self.data.strftime('%Y-%m-%d')

    def __str__(self):
        return f"{self.organization.company_name} شرکت " \
               f"پیش فاتور{self.id} "


class QuoteItem(models.Model):
    quote = models.ForeignKey('sale.Quote', on_delete=models.CASCADE)
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, verbose_name=_("محصول"))
    qty = models.PositiveIntegerField(verbose_name=_("تعداد"))
    discount = models.PositiveIntegerField(verbose_name=_("تخفیف"))
    price = models.PositiveBigIntegerField(verbose_name=_("قیمت"))

    def price_with_taxation(self):
        if self.product.is_taxation:
            return self.price + round(self.price * 0.09, 2)
        return self.price

    def get_name_product(self):
        return self.product.name

    def total_price(self):
        return self.qty * self.price

    def total_price_with_taxation(self):
        return self.qty * self.price_with_taxation()

    def finished_price(self):
        if self.discount > 0:
            return self.total_price_with_taxation() - (self.total_price_with_taxation() * round(self.discount / 100, 2))
        return self.total_price_with_taxation()

    def get_discount(self):
        return self.total_price_with_taxation() * round(self.discount / 100, 2)


class EmailHistory(models.Model):
    date_send = models.DateField(verbose_name=_("تاریخ ارسال"), auto_now_add=True)
    creator = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, verbose_name=_("فرستنده"))
    success = models.BooleanField(verbose_name=_("نتیجه"))
    email = models.EmailField(verbose_name=_("پست الکترونیک"))
