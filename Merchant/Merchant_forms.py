from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from .models import Product
from django.contrib.auth.models import User


class SignupForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "class": "form-control"}
        ),
        min_length=8,
        error_messages={"min_length": "Password must be at least 8 characters long."},
    )
    retype_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Retype Password", "class": "form-control"}
        )
    )

    class Meta:
        model = User
        fields = ["username", "email", "password"]
        widgets = {
            "username": forms.TextInput(
                attrs={"placeholder": "Name", "class": "form-control"}
            ),
            "email": forms.EmailInput(
                attrs={"placeholder": "Email", "class": "form-control"}
            ),
        }

    GST = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "GST no..", "class": "form-control"}
        ),
        required=True,
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email is already in use.")
        return email

    def clean_GST(self):
        GST = self.cleaned_data.get("GST")
        if not GST.isalnum() or len(GST) != 15:
            raise ValidationError(
                "Invalid GST number. It should be 15 characters long and alphanumeric."
            )
        return GST

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        retype_password = cleaned_data.get("retype_password")

        if password and retype_password and password != retype_password:
            self.add_error("retype_password", "Passwords do not match.")

        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Username", "class": "form-control"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "class": "form-control"}
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Invalid username or password")
        return cleaned_data


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = [
            "product_rating",
            "product_discount_percent",
            "product_long_description",
            "review_count",
        ]
        fields = "__all__"
        widgets = {
            "product_description": forms.Textarea(
                attrs={
                    "style": " resize: none;",
                    "class": "form-control",
                }
            )
        }
