from django.contrib import admin
from .models import FavoriteProduct, UserProfile, BillingDetail, Order, CartList, Cart


admin.site.register(FavoriteProduct)
admin.site.register(UserProfile)
admin.site.register(BillingDetail)
admin.site.register(Order)
admin.site.register(CartList)
admin.site.register(Cart)