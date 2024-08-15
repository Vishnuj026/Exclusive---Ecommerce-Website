from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'placeholder': 'What are you looking for?', 'class': 'form-control'}))
