# Generated by Django 5.0.6 on 2024-06-23 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Merchant', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_discount_price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_price',
            field=models.FloatField(),
        ),
    ]
