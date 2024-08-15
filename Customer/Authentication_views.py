from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .Authentication_forms import CustomSignupForm, CustomLoginForm


def Signup_page(request):
    if request.method == "POST":
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            # Check form data (including usertype)
            user = form.save()
            login(request, user)
            messages.success(request, "Successfully registered and logged in")
            return redirect("Home")
        else:
            for msg in form.error_messages:
                messages.warning(request, f"{msg}: {form.error_messages[msg]}")
    else:
        form = CustomSignupForm()
    return render(request, "User_Login_Signup/Signup_page.html", {"form": form})


def Login_page(request):
    if request.method == "POST":
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("Home")  # Replace with your home page URL name
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomLoginForm()
    return render(request, "User_Login_Signup/login_page.html", {"form": form})



def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect("Home")
