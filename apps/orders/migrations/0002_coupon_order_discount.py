# Generated by Django 4.2.6 on 2023-11-17 22:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=30, unique=True, verbose_name='code')),
                ('valid_from', models.DateTimeField(verbose_name='valid from')),
                ('valid_to', models.DateTimeField(verbose_name='valid to')),
                ('active', models.BooleanField(default=False, verbose_name='active')),
                ('discount', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(90)], verbose_name='discount')),
            ],
            options={
                'verbose_name': 'Coupon',
                'verbose_name_plural': 'Coupons',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='discount',
            field=models.IntegerField(blank=True, default=None, null=True, verbose_name='discount'),
        ),
    ]
