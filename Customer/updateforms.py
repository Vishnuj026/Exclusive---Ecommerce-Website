from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    user_name = forms.CharField(
        required=True, widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True, widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=False
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=False
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=False
    )
    profile_image = forms.ImageField(
        required=False, widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = UserProfile
        fields = ['profile_image', 'address', 'contact_number']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields['user_name'].initial = user.username
        self.fields['email'].initial = user.email
        self.fields['address'].initial = user.userprofile.address
        self.fields['contact_number'].initial = user.userprofile.contact_number

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get('current_password')
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if current_password or new_password or confirm_password:
            if not self.user.check_password(current_password):
                self.add_error('current_password', 'Current password is incorrect.')
            if new_password and new_password != confirm_password:
                self.add_error('confirm_password', 'New passwords do not match.')

        return cleaned_data

    def save(self, commit=True):
        user = self.user
        user.username = self.cleaned_data['user_name']
        user.email = self.cleaned_data['email']

        if self.cleaned_data.get('new_password'):
            user.set_password(self.cleaned_data['new_password'])

        user.userprofile.address = self.cleaned_data['address']
        user.userprofile.contact_number = self.cleaned_data['contact_number']
        user.userprofile.profile_image = self.cleaned_data['profile_image']

        if commit:
            user.save()
            user.userprofile.save()

        return user
