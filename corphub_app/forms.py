from django import forms
from . import models

class SearchForm(forms.ModelForm):
    search = forms.CharField(label="", widget=forms.TextInput(attrs={"class": "search-bar", "placeholder": "Search Here"}))

    class Meta:
        model = models.SearchModel
        fields = ('search',)
