from django.urls import path
from .import Merchant_views

urlpatterns = [
    # Merchant urls
    path('create product', Merchant_views.create_product, name='create product'),
    path('Merchant Signup page', Merchant_views.signup_page, name='Merchant Signup page'),
    path('Merchant Login page', Merchant_views.login_page, name='Merchant Login page'),
    path('Merchant Products Lists', Merchant_views.merchant_products_lists, name='Merchant Products Lists'),
    path('edit_product/<int:product_id>/<str:product_name>/', Merchant_views.edit_product, name='edit_product'),
]





