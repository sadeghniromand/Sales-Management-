# Generated by Django 3.2.5 on 2021-08-01 10:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='نام محصولات خروجی سازمان ها')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='نام محصول')),
                ('price', models.PositiveBigIntegerField(verbose_name='قیمت محصول')),
                ('is_taxation', models.BooleanField(help_text='آیا شامل مالیات است؟', verbose_name='مالیات')),
                ('pdf_catalog', models.FileField(upload_to='<django.db.models.fields.CharField>/pdf/', validators=[django.core.validators.FileExtensionValidator(['pdf'])], verbose_name='فایل کاتالوگ pdf')),
                ('img_catalog', models.ImageField(upload_to='<django.db.models.fields.CharField>/img/', verbose_name='فایل کاتالوگ img')),
                ('description', models.TextField(verbose_name='ویژگی های دستگاه')),
                ('can_be_used_for', models.ManyToManyField(blank=True, to='product.OrganizationProduct', verbose_name='محصولات قابل استفاده')),
            ],
        ),
    ]