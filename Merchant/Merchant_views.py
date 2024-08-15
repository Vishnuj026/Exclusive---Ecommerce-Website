from django.shortcuts import render, redirect
from .Merchant_forms import ProductForm, SignupForm, LoginForm
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User, Group
from .models import Merchantgtsdetail, Product
from django.contrib.auth.decorators import login_required


def signup_page(request):
    if request.method == "POST":
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            # Extract form data
            username = signup_form.cleaned_data["username"]
            GST = signup_form.cleaned_data["GST"]
            email = signup_form.cleaned_data["email"]
            password = signup_form.cleaned_data["password"]

            # Create custom user
            user = User.objects.create_user(
                username=username, email=email, password=password
            )

            # Add user to the Merchants group
            merchants_group = Group.objects.get(name="Merchants")
            user.groups.add(merchants_group)

            # Create and associate GST details with the user
            merchant_gst = Merchantgtsdetail.objects.create(MerchantName=user, GST=GST)

            # Log the user in
            login(request, user)
            messages.success(request, "Successfully registered and logged in")
            return redirect("Home")
        else:
            for field, errors in signup_form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        signup_form = SignupForm()

    return render(
        request,
        "Merchant_Login_Signup/Signup_page.html",
        {"signup_form": signup_form},
    )


def login_page(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Successfully logged in")
                return redirect(
                    "Home"
                )  # Replace 'home' with your actual home page URL name
            else:
                messages.error(request, "Invalid username or password")
    else:
        form = LoginForm()

    return render(request, "Merchant_Login_Signup/Login_page.html", {"form": form})


@login_required
def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            return redirect("Merchant Products Lists")
    else:
        form = ProductForm()
    return render(request, "Merchant/create_product.html", {"form": form})



def merchant_products_lists(request):
    if request.user.is_authenticated:
        merchant_products = Product.objects.filter(MerchantName=request.user)
    else:
        merchant_products = Product.objects.none()

    return render(
        request, "Merchant/merchant_product_lists.html", {"model_name": merchant_products}
    )





from django.shortcuts import render, get_object_or_404, redirect
from .models import Product

def edit_product(request, product_id, product_name):
    product = get_object_or_404(Product, id=product_id, product_name=product_name)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)  # Pass request.FILES for handling image
        if form.is_valid():
            form.save()
            return redirect('Merchant Products Lists')  # Redirect to product detail page
    else:
        form = ProductForm(instance=product)
    return render(request, 'Merchant/edit_product.html', {'form': form, 'product': product})
