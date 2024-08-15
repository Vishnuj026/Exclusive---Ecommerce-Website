from django.urls import path
from Customer import views,Authentication_views
from Merchant import Merchant_views

urlpatterns = [
    # Authentication urls
    path("Signup page", Authentication_views.Signup_page, name="Signup page"),
    path("Login page", Authentication_views.Login_page, name="Login page"),
    path('logout', Authentication_views.handelLogout, name="handleLogout"),
    path('My Account',views.My_Account, name='My Account'),
    #index page urls
    path("", views.home, name="Home"),
    path('search/', views.search, name='search'),
    path('billing', views.billing_view, name='billing'),
    path('apply_coupon/', views.apply_coupon, name='apply_coupon'),
    path('My Order', views.My_Order, name='My Order'),
    path('My Order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('cart', views.cart, name='cart'),
    path('cart/<int:cart_id>/', views.cart_detail, name='cart_detail'),
    path('proceed_to_checkout', views.proceed_to_checkout, name='proceed_to_checkout'),

    path('toggle_cart_item/', views.toggle_cart_item, name='toggle_cart_item'),
    path("<str:category>/<str:product_name>/<int:product_id>/", views.ProductPage, name="ProductPage"),
    path('review',views.review_view, name='review'),
    path('store_favorite_product', views.store_favorite_product, name='store_favorite_product'),


    path("Favorate products", views.Favorate_products, name="Favorate products"),     # Favorate product page urls
    path("Flash_Sales_Product", views.Flash_Sales_Product, name="Flash_Sales_Product"),  # Flash sales page urls
    path("top rated", views.top_rated, name="top rated"),  # Flash sales page urls

    path("<str:category>/", views.CategoryPage, name="CategoryPage"),# Category page urls
    path("<str:category>/<str:subcategory>/", views.SubCategoryPage, name="SubCategoryPage"),# SubCategory page urls

]





