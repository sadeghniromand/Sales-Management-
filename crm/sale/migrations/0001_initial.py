# Generated by Django 3.2.5 on 2021-08-01 12:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0002_auto_20210801_1519'),
        ('organization', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(verbose_name='تاریخ سفارش')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.organization', verbose_name='سازمان')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر ثبت کننده')),
            ],
        ),
        migrations.CreateModel(
            name='QuoteItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.PositiveIntegerField(verbose_name='تعداد')),
                ('discount', models.PositiveIntegerField(verbose_name='تخفیف')),
                ('price', models.PositiveBigIntegerField(verbose_name='قیمت')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product', verbose_name='محصول')),
                ('quote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sale.quote')),
            ],
        ),
    ]
