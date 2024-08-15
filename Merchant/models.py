from django.db import models
from django.contrib.auth.models import User


class Merchantgtsdetail(models.Model):
    MerchantName = models.OneToOneField(User, on_delete=models.CASCADE)
    GST = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.MerchantName.username


class Category(models.Model):
    Category_idno = models.CharField(max_length=10)
    Category_title = models.CharField(max_length=255)

    def __str__(self):
        return self.Category_title


class SubCategory(models.Model):
    SubCategory_idno = models.CharField(max_length=10)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    SubCategory_title = models.CharField(max_length=255)

    def __str__(self):
        return self.SubCategory_title


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=25)
    MerchantName = models.CharField(max_length=255, default="Merchant")
    brand = models.CharField(max_length=255)
    product_rating = models.PositiveIntegerField(
        choices=[(i, i) for i in range(1, 6)], null=True, blank=True
    )
    review_count = models.PositiveIntegerField(default=0)
    product_image = models.ImageField(upload_to="products/")
    product_price = models.FloatField()  # Changed to FloatField for calculations
    product_discount_price = models.FloatField(null=True, blank=True)  # Changed to FloatField
    product_discount_percent = models.PositiveIntegerField(
        null=True, blank=True, default=0
    )
    product_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    in_stock = models.BooleanField(default=False)
    free_delivery = models.BooleanField(default=False)
    return_delivery = models.BooleanField(default=False)

    def __str__(self):
        return self.product_name






class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=25)
    product_id = models.IntegerField()
    review_text = models.TextField()
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} - {self.rating} stars"
