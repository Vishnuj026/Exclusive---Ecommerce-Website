# Generated by Django 5.0.6 on 2024-06-26 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Merchant', '0002_alter_product_product_discount_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='currency',
        ),
        migrations.AlterField(
            model_name='product',
            name='product_discount_percent',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_discount_price',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_price',
            field=models.CharField(max_length=255),
        ),
    ]
