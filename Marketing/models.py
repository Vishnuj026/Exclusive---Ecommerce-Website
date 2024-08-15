from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Logo(models.Model):
    name=models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Homepageslideshowbanner(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='Homepageslideshowbanner/')
    link = models.URLField()

    def __str__(self):
        return self.name


class SocialMedia(models.Model):
    PLATFORM_CHOICES = [
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        # Add more social media platforms if needed
    ]
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, unique=True)
    url = models.URLField()

    def __str__(self):
        return self.platform
    

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    expiration_date = models.DateTimeField()
    active = models.BooleanField(default=True)
    usage_limit = models.PositiveIntegerField(null=True, blank=True)
    used_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.code

    def is_valid(self):
        if self.expiration_date < timezone.now():
            return False
        if self.usage_limit is not None and self.used_count >= self.usage_limit:
            return False
        return self.active

    def use_coupon(self):
        if self.is_valid():
            self.used_count += 1
            if self.usage_limit is not None and self.used_count >= self.usage_limit:
                self.active = False
            self.save(update_fields=['used_count', 'active'])  # Save only the updated fields
            return True
        return False
