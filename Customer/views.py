import json
from django.http import Http404, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from Merchant.models import Category, SubCategory, Product, Review
from .models import UserProfile, FavoriteProduct


def home(request):
    flash_sales_products = Product.objects.exclude(
        Q(product_discount_percent__isnull=True)
        | Q(product_discount_price__exact=None)
        | Q(product_discount_price__exact=0)
    ).order_by("-id")[:5]
    if request.user.is_authenticated:
        favorite_products = FavoriteProduct.objects.filter(user=request.user)
    else:
        favorite_products = None

    # Filter top rated products
    top_rated = Product.objects.filter(
        product_rating__gte=4, product_rating__lte=5
    ).order_by("-id")[:5]

    return render(
        request,
        "index.html",
        {
            "model_name": flash_sales_products,
            "favorite_products": favorite_products,
            "top_rated": top_rated,
        },
    )


def top_rated(request):
    # Filter top rated products
    top_rated = Product.objects.filter(
        product_rating__gte=4, product_rating__lte=5
    ).order_by("-id")
    title_name = "Top Rated"

    return render(
        request,
        "top_rated.html",
        {
            "title_name": title_name,
            "model_name": top_rated,
        },
    )


def Flash_Sales_Product(request):
    flash_sales_products = Product.objects.exclude(
        Q(product_discount_percent__isnull=True)
        | Q(product_discount_price__exact=None)
        | Q(product_discount_price__exact=0)
    ).order_by("-id")
    title_name = "Flash Sales"

    return render(
        request,
        "flash_sales.html",
        {
            "title_name": title_name,
            "model_name": flash_sales_products,
        },
    )


def ProductPage(request, product_name, product_id, category):
    category_obj = Category.objects.get(Category_title=category)
    related_items = Product.objects.filter(category=category_obj).order_by("-id")[:5]
    product_details = Product.objects.get(product_name=product_name, id=product_id)
    product_review_count = Review.objects.filter(
        product_name=product_name, product_id=product_id
    ).count()
    review_lists = Review.objects.filter(
        product_name=product_name, product_id=product_id
    ).order_by("-id")
    favorite_products = None
    profile_image_url = None

    if request.user.is_authenticated:
        # Ensure the user has a UserProfile
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        profile_image_url = (
            user_profile.profile_image.url if user_profile.profile_image else None
        )
        favorite_products = FavoriteProduct.objects.filter(user=request.user)

    # Fetch user's profile image for the logged-in user
    user_profile_image = None
    if request.user.is_authenticated:
        user_profile = request.user.userprofile
        user_profile_image = (
            user_profile.profile_image.url if user_profile.profile_image else None
        )

    context = {
        "product_review_count": product_review_count,
        "username": request.user.username,
        "profile_image_url": profile_image_url,
        "user_profile_image": user_profile_image,  # Adding user profile image to context
        "product_details": product_details,
        "model_name": related_items,
        "product": related_items,
        "favorite_products": favorite_products,
        "review_lists": review_lists,
        "product_in_cart": (
            CartList.objects.filter(user=request.user, product=product_details).exists()
            if request.user.is_authenticated
            else False
        ),
    }

    return render(request, "product_page.html", context)


from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import CartList, Product
import json


@require_POST
def toggle_cart_item(request):
    if request.user.is_authenticated:
        try:
            data = json.loads(request.body)
            product_id = data.get("product_id")
            quantity = int(data.get("quantity", 1))
            product = Product.objects.get(id=product_id)

            cart_item, created = CartList.objects.get_or_create(
                user=request.user, product=product
            )
            if created:
                cart_item.quantity = quantity
                cart_item.save()
                return JsonResponse(
                    {"success": True, "message": "Product added to cart"}
                )
            else:
                cart_item.delete()
                return JsonResponse(
                    {"success": True, "message": "Product removed from cart"}
                )
        except Product.DoesNotExist:
            return JsonResponse({"success": False, "message": "Product not found"})
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid request data"})
    return JsonResponse({"success": False, "message": "User not authenticated"})


def CategoryPage(request, category):

    try:
        category_obj = Category.objects.get(Category_title=category)
        title_name = category
        products_category_name = Product.objects.filter(category=category_obj).order_by(
            "-id"
        )
    except Category.DoesNotExist:
        # Handle the case where the category does not exist
        raise Http404("Category does not exist")
    return render(
        request,
        "products_lists.html",
        {
            "title_name": title_name,
            "category_name": category_obj,
            "model_name": products_category_name,
        },
    )


def SubCategoryPage(request, category, subcategory):
    subcategory_obj = SubCategory.objects.get(SubCategory_title=subcategory)
    products_subcategory_name = Product.objects.filter(
        sub_category=subcategory_obj
    ).order_by("-id")
    return render(
        request,
        "products_lists.html",
        {
            "title_name": subcategory_obj,
            "model_name": products_subcategory_name,
        },
    )


@login_required
def Favorate_products(request):
    # Filter products by the logged-in user's favorite products
    favorite_products = FavoriteProduct.objects.filter(user=request.user)
    favorite_product_ids = favorite_products.values_list("product_id", flat=True)

    # Adjust the exclude clause to properly handle null or zero values for discount percent and price
    flash_sales_products = (
        Product.objects.filter(id__in=favorite_product_ids)
        .exclude(
            Q(product_discount_percent__isnull=True)
            | Q(product_discount_percent=0)
            | Q(product_discount_price__isnull=True)
            | Q(product_discount_price=0)
        )
        .order_by("-id")
    )

    return render(
        request,
        "products_lists.html",
        {
            "model_name": flash_sales_products,
        },
    )


@login_required
def store_favorite_product(request):
    if request.method == "POST":
        product_name = request.POST.get("product_name")
        product_id = request.POST.get("product_id")
        user = request.user

        # Check if the favorite product already exists for the user
        existing_favorite_product = FavoriteProduct.objects.filter(
            user=user, product_name=product_name, product_id=product_id
        ).first()

        if existing_favorite_product:
            # If the favorite product already exists, delete it
            existing_favorite_product.delete()
        else:
            # Create a new favorite product
            FavoriteProduct.objects.create(
                user=user, product_name=product_name, product_id=product_id
            )
        # Redirect back to the current page
        return redirect(request.META.get("HTTP_REFERER", ""))

    return HttpResponseBadRequest("Invalid request")


@login_required
@csrf_exempt
def review_view(request):
    if request.method == "POST":
        user_profile = UserProfile.objects.get(user=request.user)
        review_text = request.POST.get("review")
        rating = request.POST.get("rate")
        product_name = request.POST.get("product_name")
        product_id = request.POST.get("product_id")

        Review.objects.create(
            user=request.user,
            product_name=product_name,
            product_id=product_id,
            review_text=review_text,
            rating=rating,
        )

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse(
                {"success": True, "message": "Review submitted successfully"}
            )

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .updateforms import UserProfileForm


@login_required
def My_Account(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("Home")  # Redirect to a success page
    else:
        form = UserProfileForm(user=request.user)

    return render(request, "My_Account.html", {"form": form})


from django.shortcuts import render
from .searchengine import SearchForm


def search(request):
    query = request.GET.get("query")
    products = []
    if query:
        products = Product.objects.filter(
            Q(product_name__icontains=query)
            | Q(category__Category_title__icontains=query)
            | Q(sub_category__SubCategory_title__icontains=query)
            | Q(brand__icontains=query)
        ).distinct()
    context = {"query": query, "products": products}
    return render(request, "search_results.html", context)


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
from .models import BillingDetail, Order
from Merchant.models import Product
from decimal import Decimal


@csrf_protect
@login_required
def billing_view(request):
    user = request.user
    billing_info = BillingDetail.objects.filter(user=user).first()
    coupon_error = ""
    discount_amount = 0
    total_price = Decimal("0")  # Define total_price with a default value

    if request.method == "POST":
        product_id = request.POST.get("product_id")
        product = get_object_or_404(Product, id=product_id)

        # Use the posted data if available
        address = request.POST.get("address")
        city = request.POST.get("city")
        phone_number = request.POST.get("phone_number")
        email_address = request.POST.get("email_address")
        save_info = request.POST.get("save_info", False)
        coupon_code = request.POST.get("coupon_code", "").strip()
        product_price = request.POST.get("product_price")
        total_price = request.POST.get("total_price")
        quantity = request.POST.get("quantity", 1)

        # Retrieve payment method
        payment_mode = request.POST.get("payment_mode")

        if not product_price:
            product_price = product.product_discount_price or product.product_price
            print(f"Fetched Product Price: {product_price}")

        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code)
                if not coupon.is_valid():
                    coupon_error = "Coupon has expired or reached its usage limit."
                else:
                    discount_amount = coupon.discount_amount
                    coupon.use_coupon()
            except Coupon.DoesNotExist:
                coupon_error = "Enter a valid coupon code."

        if save_info:
            if billing_info:
                # Update existing billing info
                billing_info.user = user
                billing_info.address = address
                billing_info.city = city
                billing_info.phone_number = phone_number
                billing_info.email_address = email_address
                billing_info.save()
            else:
                # Create new billing info
                billing_info = BillingDetail.objects.create(
                    user=user,
                    address=address,
                    city=city,
                    phone_number=phone_number,
                    email_address=email_address,
                )

        # Save order details
        Order.objects.create(
            user=user,
            product=product,
            address=address,
            city=city,
            phone_number=phone_number,
            email_address=email_address,
            payment_mode=payment_mode,
            quantity=quantity,
            total_price=total_price,
            product_price=product_price,
        )

        return redirect("My Order")  # Redirect to a success page

    # GET request handling
    product_id = request.GET.get("product_id")
    product_quantity = request.GET.get("quantity", 1)
    product = get_object_or_404(Product, id=product_id)

    product_price = float(product.product_discount_price or product.product_price)
    subtotal = product_price * int(product_quantity)
    shipping = (
        0
        if product.free_delivery
        else (0.1 * subtotal if subtotal < 1000 else 0.3 * subtotal)
    )
    total_price = subtotal + shipping

    context = {
        "product": product,
        "quantity": int(product_quantity),
        "subtotal": subtotal,
        "shipping": shipping,
        "total_price": total_price,
        "billing_info": billing_info,
        "coupon_error": coupon_error,
    }
    return render(request, "billing.html", context)


from django.http import JsonResponse
from Marketing.models import Coupon
from decimal import Decimal


@csrf_protect
@login_required
def apply_coupon(request):
    if request.method == "POST":
        data = json.loads(request.body)
        coupon_code = data.get("coupon_code", "").strip()

        try:
            coupon = Coupon.objects.get(code=coupon_code)
            if not coupon.is_valid():
                return JsonResponse(
                    {
                        "success": False,
                        "error": "Coupon has expired or reached its usage limit.",
                    }
                )
            else:
                discount_amount = coupon.discount_amount
                # Convert discount_amount to Decimal if it's not already
                if not isinstance(discount_amount, Decimal):
                    discount_amount = Decimal(str(discount_amount))
                return JsonResponse(
                    {"success": True, "discount_amount": str(discount_amount)}
                )
        except Coupon.DoesNotExist:
            return JsonResponse(
                {"success": False, "error": "Enter a valid coupon code."}
            )

    return JsonResponse({"success": False, "error": "Invalid request method."})


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Order, Cart  # Ensure Order model is also imported
import json


@login_required
def My_Order(request):
    orders = (
        Order.objects.filter(user=request.user)
        .select_related("product")
        .order_by("-id")
    )
    Cartorders = Cart.objects.filter(user=request.user).order_by("-id")
    for cart in Cartorders:
        cart.items = json.loads(cart.items)

    return render(request, "orders.html", {"orders": orders, "Cartorders": Cartorders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "order_detail.html", {"order": order})


from django.shortcuts import render, redirect
from .models import CartList
from django.contrib.auth.decorators import login_required


# views.py
from django.shortcuts import render, redirect
from .models import Cart
import json


@login_required
def cart(request):
    cart_items = CartList.objects.filter(user=request.user)
    total_price = sum(item.price * item.quantity for item in cart_items)
    for item in cart_items:
        item.subtotal = item.price * item.quantity

    context = {
        "cart_items": cart_items,
        "total_price": total_price,
    }
    return render(request, "cart.html", context)


@login_required
def proceed_to_checkout(request):
    cart_items = CartList.objects.filter(user=request.user)
    # Prepare items data as JSON
    items_data = []
    for item in cart_items:
        items_data.append(
            {
                "product_name": item.product.product_name,
                "price": item.price,
                "quantity": item.quantity,
                "subtotal": item.price * item.quantity,
            }
        )

    # Retrieve selected payment and shipping methods
    payment_method = request.POST.get("payment_method", "")
    total_price = request.POST.get("total_value", "")

    # Create a new Cart instance
    new_cart = Cart.objects.create(
        user=request.user,
        total_price=total_price,
        payment_method=payment_method,
        items=json.dumps(items_data),
    )

    # Clear the user's current cart items after checkout
    CartList.objects.filter(user=request.user).delete()

    # Optionally, redirect to a success page or wherever needed
    return redirect("My Order")


@login_required
def cart_detail(request, cart_id):
    order = get_object_or_404(Cart, id=cart_id, user=request.user)
    items = json.loads(order.items)
    for item in items:
        product = get_object_or_404(Product, product_name=item["product_name"])
        item["currency"] = product.currency  # Assign currency from Product model
        item["product_image"] = product.product_image.url

    order.items = items
    return render(request, "cart_detail.html", {"order": order})
