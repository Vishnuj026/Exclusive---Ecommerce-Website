# Generated by Django 5.0.6 on 2024-06-26 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Merchant', '0003_remove_product_currency_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='currency',
            field=models.CharField(blank=True, choices=[('₹', 'INR'), ('$', 'USD'), ('€', 'EUR')], default='INR', max_length=3),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_discount_percent',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
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
