import uuid
from django.db import models
from django.contrib.auth.models import User
from Merchant.models import Product


class FavoriteProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=25)
    product_id = models.IntegerField()

    def __str__(self):
        return f"{self.user.username}'s favorite - {self.product_name}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(
        upload_to="User_profile_images/", null=True, blank=True
    )
    address = models.CharField(max_length=255, null=True, blank=True)
    contact_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.user.username


class BillingDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email_address = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.product_name}"


from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from Merchant.models import Product


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email_address = models.EmailField()
    payment_mode = models.CharField(max_length=50)
    product_price = models.FloatField()
    quantity = models.IntegerField(default=1)
    total_price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50, default="Pending"
    )  # Default status is 'Pending'

    def __str__(self):
        return f"{self.user.username} - {self.product.product_name}"

    def save(self, *args, **kwargs):
        if not self.pk:  # If the instance is being created (not updated)
            # Calculate the delivery time (2 days from now)
            delivery_time = timezone.now() + timezone.timedelta(days=2)
            # Set the initial status based on the current day
            current_day = timezone.now().weekday()
            if current_day < 5:
                status = f'Arriving on {delivery_time.strftime("%A")}'
            else:
                status = f"Out for Delivery"
            self.status = status

        super().save(*args, **kwargs)

        # Check if the order status is 'Out for Delivery'
        if self.status == "Out for Delivery":
            # Calculate the time after 3 hours from the order creation time
            three_hours_later = self.created_at + timezone.timedelta(hours=3)
            # Check if the current time is greater than 3 hours after the order creation time
            if timezone.now() >= three_hours_later:
                # Update the order status to 'Order Delivered'
                self.status = "Order Delivered"
                self.save(update_fields=["status"])


class CartList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField()  # Use IntegerField for price
    quantity = models.PositiveIntegerField(default=1)  # Default quantity is 1

    def __str__(self):
        return f"{self.user.username} - {self.product}"

    def save(self, *args, **kwargs):
        # Set the price based on the discount price if it exists, otherwise use the regular price
        if self.product.product_discount_price:
            self.price = self.product.product_discount_price
        else:
            self.price = self.product.product_price
        super().save(*args, **kwargs)


# models.py
from django.contrib.auth.models import User
from django.db import models


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=100)
    items = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50, default="Pending"
    )  # Default status is 'Pending'

    def __str__(self):
        return f"Cart - {self.user.username} - {self.timestamp}"

    def save(self, *args, **kwargs):
        if not self.pk:  # If the instance is being created (not updated)
            # Calculate the delivery time (2 days from now)
            delivery_time = timezone.now() + timezone.timedelta(days=2)
            # Set the initial status based on the current day
            current_day = timezone.now().weekday()
            if current_day < 5:
                status = f'Arriving on {delivery_time.strftime("%A")}'
            else:
                status = f"Out for Delivery"
            self.status = status

        super().save(*args, **kwargs)

        # Check if the order status is 'Out for Delivery'
        if self.status == "Out for Delivery":
            # Calculate the time after 3 hours from the order creation time
            three_hours_later = self.timestamp + timezone.timedelta(hours=3)
            # Check if the current time is greater than 3 hours after the order creation time
            if timezone.now() >= three_hours_later:
                # Update the order status to 'Order Delivered'
                self.status = "Order Delivered"
                self.save(update_fields=["status"])
