# Generated by Django 5.0.6 on 2024-06-26 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Merchant', '0005_alter_product_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='currency',
            field=models.CharField(blank=True, choices=[('₹', 'INR'), ('$', 'USD'), ('€', 'EUR')], default='INR', max_length=3),
        ),
    ]
