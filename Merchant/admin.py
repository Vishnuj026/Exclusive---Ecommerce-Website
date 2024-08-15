from django.contrib import admin
from .models import Product, Category, SubCategory, Review,Merchantgtsdetail

# Register your models here.


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Review)
admin.site.register(Merchantgtsdetail)
