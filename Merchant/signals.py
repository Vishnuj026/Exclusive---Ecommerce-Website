from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.db.models import Count
from .models import Review, Product


@receiver(pre_save, sender=Product)
def calculate_discount_percent(sender, instance, **kwargs):
    if instance.product_discount_price and instance.product_price:
        try:
            discount_price = float(instance.product_discount_price)
            original_price = float(instance.product_price)
            discount_percent = ((original_price - discount_price) / original_price) * 100
            instance.product_discount_percent = round(discount_percent)
        except ValueError:
            # Handle the case where product_discount_price or product_price cannot be converted to float
            pass



@receiver(post_save, sender=Review)
@receiver(post_delete, sender=Review)
def update_product_rating(sender, instance, **kwargs):
    # Get all reviews for the product
    reviews = Review.objects.filter(product_id=instance.product_id)
    
    if reviews.exists():
        # Aggregate to find the most common rating
        most_common_rating = reviews.values('rating').annotate(count=Count('rating')).order_by('-count', '-rating').first()
        
        if most_common_rating:
            rating = most_common_rating['rating']
            # Update the product rating
            product = Product.objects.get(id=instance.product_id)
            product.product_rating = rating
            product.save()
    else:
        # If no reviews exist, set the product rating to None
        product = Product.objects.get(id=instance.product_id)
        product.product_rating = None
        product.save()



@receiver(post_save, sender=Review)
@receiver(post_delete, sender=Review)
def update_review_count(sender, instance, **kwargs):
    try:
        product = Product.objects.get(id=instance.product_id)
        review_count = Review.objects.filter(product_id=instance.product_id).count()
        product.review_count = review_count
        product.save()
    except Product.DoesNotExist:
        pass
